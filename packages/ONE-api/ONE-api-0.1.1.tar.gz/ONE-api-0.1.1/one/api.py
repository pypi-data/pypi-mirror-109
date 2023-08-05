"""
TODO Document
TODO Add sig to ONE Light uuids
TODO Save changes to cache
TODO Fix update cache in AlyxONE - save parquet table
TODO save parquet in update_filesystem
TODO store cache matadata in meta map
TODO Figure out why limit arg doesn't work in Alyx

Points of discussion:
    - Module structure: oneibl is too restrictive, naming module `one` means obj should have
    different name
    - NB: Wildcards will behave differently between REST and pandas
    - How to deal with load? Just remove it? Keep it in OneAlyx as legacy? How to release ONE2.0
    - Dealing with lists must be consistent.  Three options:
        - two methods each, e.g. load_dataset and load_datasets (con: a lot of overhead)
        - allow list inputs, recursive calls (con: function logic slightly more complex)
        - no list inputs; rely on list comprehensions (con: makes accessing meta data complex)
    - Need to check performance of 1. (re)setting index, 2. converting object array to 2D int array
    - NB: Sessions table date ordered.  Indexing by eid is therefore O(N) but not done in code.
    Datasets table has sorted index.
    - Conceivably you could have a subclass for Figshare, etc., not just Alyx
"""
import abc
import concurrent.futures
import warnings
import logging
import os
import fnmatch
import re
from datetime import datetime, timedelta
from functools import wraps, lru_cache
from inspect import unwrap
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Sequence, Union, Optional, List
from uuid import UUID

import tqdm
import pandas as pd
import numpy as np
import requests.exceptions

import one.params
import one.webclient as wc
import one.alf.io as alfio
import one.alf.exceptions as alferr
from .alf.onepqt import make_parquet_db
from .alf.files import alf_parts, rel_path_parts
from .alf.spec import is_valid, COLLECTION_SPEC, FILE_SPEC, regex as alf_regex
from pprint import pprint
from iblutil.io import parquet, hashfile
from iblutil.util import Bunch
from iblutil.numerical import ismember2d, find_first_2d
from one.converters import ConversionMixin

_logger = logging.getLogger(__name__)  # TODO Refactor log


def Listable(t): return Union[t, Sequence[t]]  # noqa


N_THREADS = 4  # number of download threads


def _ses2records(ses: dict) -> [pd.Series, pd.DataFrame]:
    """Extract session cache record and datasets cache from a remote session data record
    TODO Fix for new tables; use to update caches from remote queries
    :param ses: session dictionary from rest endpoint
    :return: session record, datasets frame
    """
    # Extract session record
    eid = parquet.str2np(ses['url'][-36:])
    session_keys = ('subject', 'start_time', 'lab', 'number', 'task_protocol', 'project')
    session_data = {k: v for k, v in ses.items() if k in session_keys}
    # session_data['id_0'], session_data['id_1'] = eid.flatten().tolist()
    session = (
        (pd.Series(data=session_data, name=tuple(eid.flatten()))
            .rename({'start_time': 'date'}, axis=1))
    )
    session['date'] = session['date'][:10]

    # Extract datasets table
    def _to_record(d):
        rec = dict(file_size=d['file_size'], hash=d['hash'], exists=True)
        rec['id_0'], rec['id_1'] = parquet.str2np(d['id']).flatten().tolist()
        rec['eid_0'], rec['eid_1'] = session.name
        file_path = alfio.get_alf_path(d['data_url'])
        rec['session_path'] = alfio.get_session_path(file_path).as_posix()
        rec['rel_path'] = file_path[len(rec['session_path']):].strip('/')
        return rec

    records = map(_to_record, ses['data_dataset_session_related'])
    datasets = pd.DataFrame(records).set_index(['id_0', 'id_1'])
    return session, datasets


def parse_id(method):
    """
    Ensures the input experiment identifier is an experiment UUID string
    :param method: An ONE method whose second arg is an experiment id
    :return: A wrapper function that parses the id to the expected string
    TODO Move to converters.py
    """

    @wraps(method)
    def wrapper(self, id, *args, **kwargs):
        id = self.to_eid(id)
        return method(self, id, *args, **kwargs)

    return wrapper


def refresh(method):
    """
    Refresh cache depending of query_type kwarg
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        mode = kwargs.get('query_type', None)
        if not mode or mode == 'auto':
            mode = self.mode
        self.refresh_cache(mode=mode)
        return method(self, *args, **kwargs)

    return wrapper


class One(ConversionMixin):
    search_terms = (
        'dataset', 'date_range', 'laboratory', 'number', 'project', 'subject', 'task_protocol'
    )

    def __init__(self, cache_dir=None, mode='auto'):
        # get parameters override if inputs provided
        super().__init__()
        if not getattr(self, '_cache_dir', None):  # May already be set by subclass
            self._cache_dir = cache_dir or one.params.get_cache_dir()
        self.cache_expiry = timedelta(hours=24)
        self.mode = mode
        # init the cache file
        self._load_cache()

    @property
    def offline(self):
        return self.mode == 'local' or not getattr(self, '_web_client', False)

    def _load_cache(self, cache_dir=None, **kwargs):
        self._cache = Bunch({'expired': False, 'created_time': None})
        INDEX_KEY = 'id'
        for table in ('sessions', 'datasets'):
            cache_file = Path(cache_dir or self._cache_dir).joinpath(table + '.pqt')
            if cache_file.exists():
                # we need to keep this part fast enough for transient objects
                cache, info = parquet.load(cache_file)
                created = datetime.fromisoformat(info['date_created'])
                if self._cache['created_time']:
                    self._cache['created_time'] = min([self._cache['created_time'], created])
                else:
                    self._cache['created_time'] = created
                self._cache['loaded_time'] = datetime.now()
                self._cache['expired'] |= datetime.now() - created > self.cache_expiry
            else:
                self._cache['expired'] = True
                self._cache[table] = pd.DataFrame()
                continue

            # Set the appropriate index if none already set
            if isinstance(cache.index, pd.RangeIndex):
                num_index = [f'{INDEX_KEY}_{n}' for n in range(2)]
                try:
                    int_eids = cache[num_index].any(axis=None)
                except KeyError:
                    int_eids = False
                cache.set_index(num_index if int_eids else INDEX_KEY, inplace=True)

            # Check sorted
            is_sorted = (cache.index.is_lexsorted()
                         if isinstance(cache.index, pd.MultiIndex)
                         else True)
            # Sorting makes MultiIndex indexing O(N) -> O(1)
            if table == 'datasets' and not is_sorted:
                cache.sort_index(inplace=True)

            self._cache[table] = cache
        return self._cache.get('loaded_time', None)

    def refresh_cache(self, mode='auto'):
        """Check and reload cache tables

        :param mode:
        :return: Loaded time
        """
        if mode in ('local', 'remote'):  # TODO maybe rename mode
            pass
        elif mode == 'auto':
            if datetime.now() - self._cache['loaded_time'] > self.cache_expiry:
                _logger.info('Cache expired, refreshing')
                self._load_cache()
        elif mode == 'refresh':
            _logger.debug('Forcing reload of cache')
            self._load_cache(clobber=True)
        else:
            raise ValueError(f'Unknown refresh type "{mode}"')
        return self._cache.get('loaded_time', None)

    def download_datasets(self, dsets, **kwargs) -> List[Path]:
        """
        TODO Support slice, dicts and URLs?
        Download several datasets given a slice of the datasets table
        :param dsets: list of dataset dictionaries from an Alyx REST query OR list of URL strings
        :return: local file path list
        """
        out_files = []
        if hasattr(dsets, 'iterrows'):
            dsets = map(lambda x: x[1], dsets.iterrows())
        # FIXME Thread timeout?
        with concurrent.futures.ThreadPoolExecutor(max_workers=N_THREADS) as executor:
            # TODO Subclass can just call web client method directly, no need to pass hash, etc.
            futures = [executor.submit(self.download_dataset, dset, file_size=dset['file_size'],
                                       hash=dset['hash'], **kwargs) for dset in dsets]
            concurrent.futures.wait(futures)
            for future in futures:
                out_files.append(future.result())
        return out_files

    def download_dataset(self, dset, cache_dir=None, **kwargs) -> Path:
        """
        Download a dataset from an alyx REST dictionary
        :param dset: single dataset dictionary from an Alyx REST query OR URL string
        :param cache_dir (optional): root directory to save the data in (home/downloads by default)
        :return: local file path
        """
        pass

    def search(self, details=False, exists_only=False, query_type='auto', **kwargs):
        """
        Searches sessions matching the given criteria and returns a list of matching eids

        For a list of search terms, use the methods

         one.search_terms

        For all of the search parameters, a single value or list may be provided.  For dataset,
        the sessions returned will contain all listed datasets.  For any other parameter,
        the session must contain at least one of the entries

        :param dataset: list of dataset names. Returns sessions containing all these datasets
        :param date_range: list of 2 strings or list of 2 dates that define the range (inclusive)
        :param details: if true also returns a dict of dataset details
        :param lab: a str or list of lab names
        :param number: number of session to be returned; will take the first n sessions found
        :param subjects: a list of subjects nickname
        :param task_protocol: task protocol name (can be partial, i.e. any task protocol
                              containing that str will be found)
        :param project: project name (can be partial, i.e. any task protocol containing
                        that str will be found)

        :return: list of eids, if details is True, also returns a list of dictionaries,
         each entry corresponding to a matching session
        TODO Describe which are AND vs OR ops
        """

        def validate_input(inarg):
            """Ensure input is a list"""
            return [inarg] if isinstance(inarg, str) or not isinstance(inarg, Iterable) else inarg

        def all_present(x, dsets, exists=True):
            """Returns true if all datasets present in Series"""
            return all(any(x.str.contains(y) & exists) for y in dsets)

        def autocomplete(term):
            """
            Validate search term and return complete name, e.g. autocomplete('subj') == 'subject'
            """
            full_key = (x for x in self.search_terms if x.lower().startswith(term))
            key_ = next(full_key, None)
            if not key_:
                raise ValueError(f'Invalid search term "{term}"\n'
                                 'Note: remote search terms may differ')
            elif next(full_key, None):
                raise ValueError(f'Ambiguous search term "{term}"')
            return key_

        # Iterate over search filters, reducing the sessions table
        sessions = self._cache['sessions']

        # Ensure sessions filtered in a particular order, with datasets last
        search_order = ('date_range', 'number', 'dataset')

        def sort_fcn(itm):
            return -1 if itm[0] not in search_order else search_order.index(itm[0])
        queries = {autocomplete(k): v for k, v in kwargs.items()}  # Validate and get full name
        for key, value in sorted(queries.items(), key=sort_fcn):
            # key = autocomplete(key)  # Validate and get full name
            # No matches; short circuit
            if sessions.size == 0:
                return ([], None) if details else []
            # String fields
            elif key in ('subject', 'task_protocol', 'laboratory', 'project'):
                query = '|'.join(validate_input(value))
                mask = sessions['lab' if key == 'laboratory' else key].str.contains(query)
                sessions = sessions[mask.astype(bool, copy=False)]
            elif key == 'date_range':
                start, end = _validate_date_range(value)
                session_date = pd.to_datetime(sessions['date'])
                sessions = sessions[(session_date >= start) & (session_date <= end)]
            elif key == 'number':
                query = validate_input(value)
                sessions = sessions[sessions[key].isin(map(int, query))]
            # Dataset check is biggest so this should be done last
            elif key == 'dataset':
                index = ['eid_0', 'eid_1'] if self._index_type('datasets') is int else 'eid'
                query = validate_input(value)
                datasets = self._cache['datasets']
                if self._index_type() is int:
                    isin, _ = ismember2d(datasets[['eid_0', 'eid_1']].values,
                                         np.array(sessions.index.values.tolist()))
                else:
                    isin = datasets['eid'].isin(sessions.index.values)
                if exists_only:
                    # For each session check any dataset both contains query and exists
                    mask = (
                        (datasets[isin]
                            .groupby(index, sort=False)
                            .apply(lambda x: all_present(x['rel_path'], query, x['exists'])))
                    )
                else:
                    # For each session check any dataset contains query
                    mask = (
                        (datasets[isin]
                            .groupby(index, sort=False)['rel_path']
                            .aggregate(lambda x: all_present(x, query)))
                    )
                # eids of matching dataset records
                idx = mask[mask].index

                # Reduce sessions table by datasets mask
                sessions = sessions.loc[idx]

        # Return results
        if sessions.size == 0:
            return ([], None) if details else []
        eids = sessions.index.to_list()
        if self._index_type() is int:
            eids = parquet.np2str(np.array(eids))

        if details:
            return eids, sessions.reset_index().iloc[:, 2:].to_dict('records', Bunch)
        else:
            return eids

    def _update_filesystem(self, datasets, offline=None, update_exists=True, clobber=False):
        """Update the local filesystem for the given datasets
        Given a set of datasets, check whether records correctly reflect the filesystem.
        Called by load methods, this returns a list of file paths to load and return.
        TODO This needs changing; overlaod for downloading?
        TODO change name to check_files, check_present, present_datasets, check_local_files?
         check_filesystem?
         This changes datasets frame, calls _update_cache(sessions=None, datasets=None) to
         update and save tables.  Download_datasets can also call this function.

        :param datasets: A list or DataFrame of dataset records
        :param offline: If false and Web client present, downloads the missing datasets from a
        remote repository
        :param update_exists: If true, the cache is updated to reflect the filesystem
        :param clobber: If true and not offline, datasets are re-downloaded regardless of local
        filesystem
        :return: A list of file paths for the datasets (None elements for non-existent datasets)
        """
        if offline is None:
            offline = self.mode == 'local' or not getattr(self, '_web_client', None)
        if offline:
            files = []
            if isinstance(datasets, pd.Series):
                datasets = pd.DataFrame([datasets])
            elif not isinstance(datasets, pd.DataFrame):
                # Cast set of dicts (i.e. from REST datasets endpoint)
                datasets = pd.DataFrame(list(datasets))
            for i, rec in datasets.iterrows():
                file = Path(self._cache_dir, *rec[['session_path', 'rel_path']])
                if file.exists():
                    # TODO Factor out; hash & file size also checked in _download_file;
                    #  see _update_cache - we need to save changed cache
                    files.append(file)
                    new_hash = hashfile.md5(file)
                    new_size = file.stat().st_size
                    hash_mismatch = rec['hash'] and new_hash != rec['hash']
                    size_mismatch = rec['file_size'] and new_size != rec['file_size']
                    if hash_mismatch or size_mismatch:
                        # the local file hash doesn't match the dataset table cached hash
                        # datasets.at[i, ['hash', 'file_size']] = new_hash, new_size
                        # Raise warning if size changed or hash changed and wasn't empty
                        if size_mismatch or (hash_mismatch and rec['hash']):
                            _logger.warning('local md5 or size mismatch')
                else:
                    files.append(None)
                if rec['exists'] != file.exists():
                    datasets.at[i, 'exists'] = not rec['exists']
                    if update_exists:
                        self._cache['datasets'].loc[i, 'exists'] = rec['exists']
        else:
            # TODO deal with clobber and exists here?
            files = self.download_datasets(datasets, update_cache=update_exists, clobber=clobber)
        return files

    def _index_type(self, table='sessions'):
        idx_0 = self._cache[table].index.values[0]
        if len(self._cache[table].index.names) == 2 and all(isinstance(x, int) for x in idx_0):
            return int
        elif len(self._cache[table].index.names) == 1 and isinstance(idx_0, str):
            return str
        else:
            raise IndexError

    @parse_id
    def get_details(self, eid: Union[str, Path, UUID], full: bool = False):
        int_ids = self._index_type() is int
        if int_ids:
            eid = parquet.str2np(eid).tolist()
        det = self._cache['sessions'].loc[eid]
        if full:
            # to_drop = 'eid' if int_ids else ['eid_0', 'eid_1']
            # det = det.drop(to_drop, axis=1)
            det = self._cache['datasets'].join(det, on=det.index.names, how='right')
        return det

    @refresh
    def list_subjects(self) -> List[str]:
        """
        List all subjects in database
        :return: Sorted list of subject names
        """
        return self._cache['sessions']['subject'].sort_values().unique()

    @refresh
    def list_datasets(self, eid=None, details=True) -> Union[np.ndarray, pd.DataFrame]:
        """
        Given one or more eids, return the datasets for those sessions.  If no eid is provided,
        a list of all datasets is returned.  When details is false, a sorted array of unique
        datasets is returned (their relative paths).
        TODO Change default to False

        :param eid: Experiment session identifier; may be a UUID, URL, experiment reference string
        details dict or Path
        :param details: When true, a pandas DataFrame is returned, otherwise a numpy array of
        relative paths (collection/revision/filename) - see one.alf.spec.describe for details.
        :return: Slice of datasets table or numpy array if details is False
        """
        datasets = self._cache['datasets']
        if not eid:
            return datasets.copy() if details else datasets['rel_path'].unique()
        eid = self.to_eid(eid)  # Ensure we have a UUID str list
        if not eid:
            return datasets.iloc[0:0]  # Return empty
        if self._index_type() is int:
            eid_num = parquet.str2np(eid)
            index = ['eid_0', 'eid_1']
            isin, _ = ismember2d(datasets[index].to_numpy(), eid_num)
            datasets = datasets[isin]
        else:
            session_match = datasets['eid'].isin(eid)
            datasets = datasets[session_match]
        # Return only the relative path
        return datasets if details else datasets['rel_path'].sort_values().values

    def list_revisions(self, eid, dataset):
        pass

    @refresh
    @parse_id
    def load_object(self,
                    eid: Union[str, Path, UUID],
                    obj: str,
                    collection: Optional[str] = 'alf',
                    revision: Optional[str] = None,
                    query_type: str = 'auto',
                    **kwargs) -> Union[alfio.AlfBunch, List[Path]]:
        """
        Load all attributes of an ALF object from a Session ID and an object name.  Any datasets
        with matching object name will be loaded.

        :param eid: Experiment session identifier; may be a UUID, URL, experiment reference string
        details dict or Path
        :param obj: The ALF object to load.  Supports asterisks as wildcards.
        :param collection:  The collection to which the object belongs, e.g. 'alf/probe01'.
        Supports asterisks as wildcards.
        :param download_only: When true the data are downloaded and the file paths are returned
        :param kwargs: Additional filters for datasets, including namespace and timescale
        :return: An ALF bunch or if download_only is True, a list of Paths objects

        Examples:
        load_object(eid, 'moves')
        load_object(eid, 'trials')
        load_object(eid, 'spikes', collection='.*probe01')
        load_object(eid, 'spikes', namespace='ibl')
        load_object(eid, 'spikes', timescale='ephysClock')
        """
        datasets = self.list_datasets(eid)

        if len(datasets) == 0:
            raise alferr.ALFObjectNotFound(f'ALF object "{obj}" not found in cache')

        REGEX = True
        if not REGEX:
            import fnmatch
            obj = re.compile(fnmatch.translate(obj))

        expression = alf_regex(f'{COLLECTION_SPEC}/{FILE_SPEC}',
                               object=obj, collection=collection, revision=revision)
        table = datasets['rel_path'].str.extract(expression)
        match = ~table[['collection', 'object', 'revision']].isna().all(axis=1)

        # Validate result before loading
        if table['object'][match].unique().size > 1:
            raise alferr.ALFMultipleObjectsFound('The following matching objects were found: ' +
                                                 ', '.join(table['object'][match].unique()))
        elif not match.any():
            raise alferr.ALFObjectNotFound(f'ALF object "{obj}" not found on Alyx')
        if table['collection'][match].unique().size > 1:
            raise alferr.ALFMultipleCollectionsFound(
                'Matching object belongs to multiple collections:' +
                ', '.join(table['collection'][match].unique())
            )

        datasets = datasets[match]

        # parquet.np2str(np.array(datasets.index.values.tolist()))
        # For those that don't exist, download them
        # return alfio.load_object(path, table[match]['object'].values[0])
        download_only = kwargs.pop('download_only', False)
        offline = None if query_type == 'auto' else self.mode == 'local'
        files = self._update_filesystem(datasets, offline=offline)
        files = [x for x in files if x]
        if not files:
            raise alferr.ALFObjectNotFound(f'ALF object "{obj}" not found on Alyx')

        if download_only:
            return files

        # self._check_exists(datasets[~datasets['exists']])
        return alfio.load_object(files[0].parent, table[match]['object'].values[0], **kwargs)

    @refresh
    @parse_id
    def load_dataset(self,
                     eid: Union[str, Path, UUID],
                     dataset: str,
                     collection: Optional[str] = 'alf',
                     revision: Optional[str] = None,
                     query_type: str = 'auto',
                     **kwargs) -> Any:
        """
        TODO Document
        Load a dataset for a given session id and dataset name
        :param eid: an
        :param dataset:
        :param collection:
        :param revision:
        :param kwargs:
        :return:
        """
        datasets = self.list_datasets(eid)

        if len(datasets) == 0:
            raise alferr.ALFObjectNotFound(f'ALF dataset "{dataset}" not found in cache')

        # Split path into
        # TODO This could maybe be an ALF function
        expression = alf_regex(f'^{COLLECTION_SPEC}$', revision=revision, collection=collection)
        table = datasets['rel_path'].str.rsplit('/', 1, expand=True)
        if table.columns.stop == 1:
            match = table[0].str.contains(dataset)
        else:
            match = table[1].str.contains(dataset)
            # Check collection and revision matches
            table = table[0].str.extract(expression)
            # TODO Revision should be dealt with as sorted string
            match &= ~table['collection'].isna() & (~table['revision'].isna() if revision else True)
        if not match.any():
            raise alferr.ALFObjectNotFound(f'Dataset "{dataset}" not found')
        elif sum(match) != 1:
            raise alferr.ALFMultipleCollectionsFound('Multiple datasets returned')

        download_only = kwargs.pop('download_only', False)
        # Check files exist / download remote files
        file, = self._update_filesystem(datasets[match], **kwargs)

        if not file:
            raise alferr.ALFObjectNotFound('Dataset not found')
        elif download_only:
            return file
        return alfio.load_file_content(file)

    @refresh
    @parse_id
    def load_datasets(self,
                      eid: Union[str, Path, UUID],
                      datasets: str,
                      collections: Optional[str] = 'alf',
                      revisions: Optional[str] = None,
                      query_type: str = 'auto',
                      assert_present=True,
                      **kwargs) -> Any:
        """
        TODO Document
        Load a dataset for a given session id and dataset name
        :param eid: an
        :param dataset:
        :param collection:
        :param revision:
        :param kwargs:
        :return:
        """
        # Check input args
        def _verify_specifiers(specifiers):
            out = []
            for spec in specifiers:
                if not spec or isinstance(spec, str):
                    out.append([spec] * len(datasets))
                elif len(spec) != len(datasets):
                    raise ValueError(
                        'Collection and revision specifiers must match number of datasets')
                else:
                    out.append(spec)
            return out

        if isinstance(datasets, str):
            raise TypeError('`datasets` must be a non-string iterable')
        collections, revisions = _verify_specifiers([collections, revisions])

        # Short circuit
        all_datasets = self.list_datasets(eid, details=True)
        if len(all_datasets) == 0:
            if assert_present:
                raise alferr.ALFObjectNotFound(f'No datasets found for session {eid}')
            else:
                _logger.warning(f'No datasets found for session {eid}')
                return None, all_datasets
        if len(datasets) == 0:
            return None, all_datasets.iloc[0:0]  # Return empty

        # Filter and load missing
        indices = []
        for dset, collec, rev in zip(datasets, collections, revisions):
            # FIXME: Do we want the searching to be fuzzy here, or leave up to the user?
            pattern = alf_regex(f'^{COLLECTION_SPEC}/.*{dset}.*$', collection=collec)
            match = all_datasets[all_datasets['rel_path'].str.match(pattern)]
            if len(match) == 0:
                indices.append(None)
                continue
            elif rev is None:  # If no revision is specified for this dataset...
                if 'default_revision' in match.columns:
                    match = match[match.default_revision]
                else:
                    # FIXME Return latest revision instead
                    raise NotImplementedError()
                if len(match) > 1:
                    revisions = [rel_path_parts(x)[1] for x in match.rel_path.values]
                    rev_list = '"' + '", "'.join(revisions) + '"'
                    raise alferr.ALFMultipleRevisionsFound(
                        f'Multiple revisions for dataset "{dset}": {rev_list}')
                indices.extend(match.index.tolist() or [None])
                continue
            else:  # Deal with revisions
                revisions = [rel_path_parts(x)[1] for x in match.rel_path.values]
                revisions_sorted = sorted(revisions, reverse=True)
                try:
                    last = revisions_sorted[(np.array(revisions_sorted) < rev[1:]).argmax()]
                    indices.append(match.index.values[revisions.index(last)])
                except ValueError:
                    indices.append(None)

        if any(x is None for x in indices):
            missing_list = ', '.join(x for x, y in zip(datasets, indices) if not y)
            message = f'The following datasets are not in the cache: {missing_list}'
            if assert_present:
                raise alferr.ALFObjectNotFound(message)
            else:
                _logger.warning(message)

        present = [x for x in indices if x]
        download_only = kwargs.pop('download_only', False)
        # Check files exist / download remote files
        files = self._update_filesystem(all_datasets.loc[present, :], **kwargs)

        present_dsets = [x for x, y in zip(datasets, indices) if y]
        if any(x is None for x in files):
            missing_list = ', '.join(x for x, y in zip(present_dsets, files) if not y)
            message = f'The following datasets were not downloaded: {missing_list}'
            raise alferr.ALFObjectNotFound(message) if assert_present else _logger.warning(message)

        records = (all_datasets
                   .loc[present, :]
                   .reset_index()
                   .drop(['eid_0', 'eid_1'], axis=1)
                   .to_dict('records', Bunch))
        records = [x for x, y in zip(records, files) if y]
        if download_only:
            return files, records
        return [alfio.load_file_content(x) for x in files], records

    @refresh
    def load_dataset_from_id(self,
                             dset_id: Union[str, UUID],
                             download_only: bool = False,
                             details: bool = False,
                             **kwargs) -> Any:
        if isinstance(dset_id, str):
            dset_id = parquet.str2np(dset_id)
        elif isinstance(dset_id, UUID):
            dset_id = parquet.uuid2np([dset_id])
        # else:
        #     dset_id = np.asarray(dset_id)
        if self._index_type('datasets') is int:
            try:
                dataset = self._cache['datasets'].loc[dset_id.tolist()]
                assert len(dataset) == 1
                dataset = dataset.iloc[0]
            except KeyError:
                raise alferr.ALFObjectNotFound('Dataset not found')
            except AssertionError:
                raise alferr.ALFMultipleObjectsFound('Duplicate dataset IDs')
        else:
            ids = self._cache['datasets'][['id_0', 'id_1']].to_numpy()
            try:
                dataset = self._cache['datasets'].iloc[find_first_2d(ids, dset_id)]
                assert len(dataset) == 1
            except TypeError:
                raise alferr.ALFObjectNotFound('Dataset not found')
            except AssertionError:
                raise alferr.ALFMultipleObjectsFound('Duplicate dataset IDs')

        filepath, = self._update_filesystem(dataset)
        if not filepath:
            raise alferr.ALFObjectNotFound('Dataset not found')
        output = filepath if download_only else alfio.load_file_content(filepath)
        if details:
            return output, dataset
        else:
            return output

    @abc.abstractmethod
    def list(self, **kwargs):
        pass

    @staticmethod
    def setup(cache_dir, **kwargs):
        """
        Interactive command tool that populates parameter file for ONE IBL.
        FIXME See subclass
        """
        make_parquet_db(cache_dir, **kwargs)
        return One(cache_dir, mode='local')


@lru_cache(maxsize=1)
def ONE(mode='auto', **kwargs):
    """ONE API factory
    Determine which class to instantiate depending on parameters passed.
    """
    if kwargs.pop('offline', False):
        _logger.warning('the offline kwarg will probably be removed. '
                        'ONE is now offline by default anyway')
        warnings.warn('"offline" param will be removed; use mode="local"', DeprecationWarning)

    if (any(x in kwargs for x in ('base_url', 'username', 'password')) or
            not kwargs.get('cache_dir', False)):
        return OneAlyx(mode=mode, **kwargs)

    # TODO This feels hacky
    # If cache dir was provided and corresponds to one configured with an Alyx client, use OneAlyx
    try:
        one.params._check_cache_conflict(kwargs.get('cache_dir'))
        return One(mode=mode, **kwargs)
    except AssertionError:
        # Cache dir corresponds to a Alyx repo, call OneAlyx
        return OneAlyx(mode=mode, **kwargs)


class OneAlyx(One):
    def __init__(self, username=None, password=None, base_url=None, mode='auto', **kwargs):
        # Load Alyx Web client
        self._web_client = wc.AlyxClient(username=username,
                                         password=password,
                                         base_url=base_url,
                                         silent=kwargs.pop('silent', False),
                                         cache_dir=kwargs.get('cache_dir', None))
        # get parameters override if inputs provided
        super(OneAlyx, self).__init__(mode=mode, **kwargs)

    def _load_cache(self, cache_dir=None, clobber=False):
        if not clobber:
            super(OneAlyx, self)._load_cache(self._cache_dir)  # Load any present cache
            if (self._cache and not self._cache['expired']) or self.mode == 'local':
                return

        # Warn user if expired
        if (
            self._cache['expired'] and
            self._cache.get('created_time', False) and
            not self.alyx.silent
        ):
            age = datetime.now() - self._cache['created_time']
            t_str = (f'{age.days} days(s)'
                     if age.days >= 1
                     else f'{np.floor(age.seconds / (60 * 2))} hour(s)')
            _logger.info(f'cache over {t_str} old')

        try:
            # Determine whether a newer cache is available
            cache_info = self.alyx.get('cache/info', expires=True)
            remote_created = datetime.fromisoformat(cache_info['date_created'])
            local_created = self._cache.get('created_time', None)
            if local_created and (remote_created - local_created) < timedelta(minutes=1):
                _logger.info('No newer cache available')
                return

            # Download the remote cache files
            _logger.info('Downloading remote caches...')
            files = self.alyx.download_cache_tables()
            assert any(files)
            super(OneAlyx, self)._load_cache(self._cache_dir)  # Reload cache after download
        except requests.exceptions.HTTPError:
            _logger.error('Failed to load the remote cache file')
            self.mode = 'remote'
        except (ConnectionError, requests.exceptions.ConnectionError):
            _logger.error('Failed to connect to Alyx')
            self.mode = 'local'

    @property
    def alyx(self):
        return self._web_client

    @property
    def _cache_dir(self):
        return self._web_client.cache_dir

    def describe_dataset(self, dataset_type=None):
        # TODO Move the AlyxClient; add to rest examples; rename to describe?
        if not dataset_type:
            return self.alyx.rest('dataset-types', 'list')
        # if not isinstance(dataset_type, str):
        #     print('No dataset_type provided or wrong type. Should be str')
        #     return
        try:
            assert isinstance(dataset_type, str) and not alfio.is_uuid_string(dataset_type)
            out = self.alyx.rest('dataset-types', 'read', dataset_type)
        except (AssertionError, requests.exceptions.HTTPError):
            # Try to get dataset type from dataset name
            out = self.alyx.rest('dataset-types', 'read', self.dataset2type(dataset_type))
        print(out['description'])

    # def list(self, eid: Optional[Union[str, Path, UUID]] = None, details=False
    #          ) -> Union[List, Dict[str, str]]:
    #     """
    #     From a Session ID, queries Alyx database for datasets related to a session.
    #
    #     :param eid: Experiment session uuid str
    #     :type eid: str
    #
    #     :param details: If false returns a list of path, otherwise returns the REST dictionary
    #     :type eid: bool
    #
    #     :return: list of strings or dict of lists if details is True
    #     :rtype:  list, dict
    #     """
    #     if not eid:
    #         return [x['name'] for x in self.alyx.rest('dataset-types', 'list')]
    #
    #     # Session specific list
    #     dsets = self.alyx.rest('datasets', 'list', session=eid, exists=True)
    #     if not details:
    #         dsets = sorted([Path(dset['collection']).joinpath(dset['name']) for dset in dsets])
    #     return dsets

    @refresh
    @parse_id
    def load(self, eid, dataset_types=None, dclass_output=False, dry_run=False, cache_dir=None,
             download_only=False, clobber=False, offline=False, keep_uuid=False):
        """
        From a Session ID and dataset types, queries Alyx database, downloads the data
        from Globus, and loads into numpy array.

        :param eid: Experiment ID, for IBL this is the UUID of the Session as per Alyx
         database. Could be a full Alyx URL:
         'http://localhost:8000/sessions/698361f6-b7d0-447d-a25d-42afdef7a0da' or only the UUID:
         '698361f6-b7d0-447d-a25d-42afdef7a0da'. Can also be a list of the above for multiple eids.
        :type eid: str
        :param dataset_types: [None]: Alyx dataset types to be returned.
        :type dataset_types: list
        :param dclass_output: [False]: forces the output as dataclass to provide context.
        :type dclass_output: bool
         If None or an empty dataset_type is specified, the output will be a dictionary by default.
        :param cache_dir: temporarly overrides the cache_dir from the parameter file
        :type cache_dir: str
        :param download_only: do not attempt to load data in memory, just download the files
        :type download_only: bool
        :param clobber: force downloading even if files exists locally
        :type clobber: bool
        :param keep_uuid: keeps the UUID at the end of the filename (defaults to False)
        :type keep_uuid: bool

        :return: List of numpy arrays matching the size of dataset_types parameter, OR
         a dataclass containing arrays and context data.
        :rtype: list, dict, dataclass SessionDataInfo
        """
        # this is a wrapping function to keep signature and docstring accessible for IDE's
        return self._load_recursive(eid, dataset_types=dataset_types, dclass_output=dclass_output,
                                    dry_run=dry_run, cache_dir=cache_dir, keep_uuid=keep_uuid,
                                    download_only=download_only, clobber=clobber, offline=offline)

    @refresh
    @parse_id
    def load_dataset(self,
                     eid: Union[str, Path, UUID],
                     dataset: str,
                     collection: str = None,
                     revision: str = None,
                     query_type: str = None,
                     download_only: bool = False) -> Any:
        """
        Load a single dataset from a Session ID and a dataset type.

        :param eid: Experiment session identifier; may be a UUID, URL, experiment reference string
        details dict or Path
        :param dataset: The ALF dataset to load.  Supports asterisks as wildcards.
        :param collection:  The collection to which the object belongs, e.g. 'alf/probe01'.
        For IBL this is the relative path of the file from the session root.
        Supports asterisks as wildcards.
        :param download_only: When true the data are downloaded and the file path is returned
        :return: dataset or a Path object if download_only is true

        Examples:
        TODO Update examples
            intervals = one.load_dataset(eid, '_ibl_trials.intervals.npy')
            intervals = one.load_dataset(eid, '*trials.intervals*')
            filepath = one.load_dataset(eid '_ibl_trials.intervals.npy', download_only=True)
            spikes = one.load_dataset(eid 'spikes.times.npy', collection='alf/probe01')
        """
        query_type = query_type or self.mode
        if query_type != 'remote':
            load_dataset_offline = unwrap(super().load_dataset)  # Skip parse_id decorator
            return load_dataset_offline(self, eid, dataset,
                                        collection=collection,
                                        revision=revision,
                                        download_only=download_only,
                                        query_type=query_type)
        search_str = 'name__regex,' + dataset.replace('.', r'\.').replace('*', '.*')
        if collection:
            search_str += ',collection__regex,' + collection.replace('*', '.*')
        results = self.alyx.rest('datasets', 'list', session=eid, django=search_str, exists=True)

        # Get filenames of returned ALF files
        collection_set = {x['collection'] for x in results}
        if len(collection_set) > 1:
            raise alferr.ALFMultipleCollectionsFound(
                'Matching dataset belongs to multiple collections:' + ', '.join(collection_set))
        if len(results) > 1:
            raise alferr.ALFMultipleObjectsFound('The following matching datasets were found: ' +
                                                 ', '.join(x['name'] for x in results))
        if len(results) == 0:
            raise alferr.ALFObjectNotFound(f'Dataset "{dataset}" not found on Alyx')

        filename = self.download_dataset(results[0])
        assert filename is not None, 'failed to download dataset'

        return filename if download_only else alfio.load_file_content(filename)

    @refresh
    def load_collection(self):
        raise NotImplementedError()

    @refresh
    @parse_id
    def load_object(self,
                    eid: Union[str, Path, UUID],
                    obj: str,
                    collection: Optional[str] = 'alf',
                    download_only: bool = False,
                    query_type: str = None,
                    clobber: bool = False,
                    **kwargs) -> Union[alfio.AlfBunch, List[Path]]:
        """
        Load all attributes of an ALF object from a Session ID and an object name.

        :param eid: Experiment session identifier; may be a UUID, URL, experiment reference string
        details dict or Path
        :param obj: The ALF object to load.  Supports asterisks as wildcards.
        :param collection: The collection to which the object belongs, e.g. 'alf/probe01'.
        Supports asterisks as wildcards.
        :param download_only: When true the data are downloaded and the file paths are returned
        :param query_type: Query cache ('local') or Alyx database ('remote')
        :param clobber: If true, local data are re-downloaded
        :param kwargs: Optional filters for the ALF objects, including namespace and timescale
        :return: An ALF bunch or if download_only is True, a list of Paths objects

        Examples:
        load_object(eid, '*moves')
        load_object(eid, 'trials')
        load_object(eid, 'spikes', collection='*probe01')
        """
        query_type = query_type or self.mode
        if query_type != 'remote':
            load_object_offline = unwrap(super().load_object)  # Skip parse_id decorator
            return load_object_offline(self, eid, obj,
                                       collection=collection, download_only=download_only,
                                       query_type=query_type, **kwargs)
        # Filter server-side by collection and dataset name
        search_str = 'name__regex,' + obj.replace('*', '.*')
        if collection and collection != 'all':
            search_str += ',collection__regex,' + collection.replace('*', '.*')
        results = self.alyx.rest('datasets', 'list', exists=True, session=eid, django=search_str)
        pattern = re.compile(fnmatch.translate(obj))

        # Further refine by matching object part of ALF datasets
        def match(r):
            return is_valid(r['name']) and pattern.match(alf_parts(r['name'])[1])

        # Get filenames of returned ALF files
        returned_obj = {alf_parts(x['name'])[1] for x in results if match(x)}

        # Validate result before loading
        if len(returned_obj) > 1:
            raise alferr.ALFMultipleObjectsFound('The following matching objects were found: ' +
                                                 ', '.join(returned_obj))
        elif len(returned_obj) == 0:
            raise alferr.ALFObjectNotFound(f'ALF object "{obj}" not found on Alyx')
        collection_set = {x['collection'] for x in results if match(x)}
        if len(collection_set) > 1:
            raise alferr.ALFMultipleCollectionsFound(
                'Matching object belongs to multiple collections:' + ', '.join(collection_set))

        # Download and optionally load the datasets
        out_files = self._update_filesystem((x for x in results if match(x)), clobber=clobber)
        # out_files = self.download_datasets(x for x in results if match(x))
        assert not any(x is None for x in out_files), 'failed to download object'
        if download_only:
            return out_files
        else:
            return alfio.load_object(out_files[0].parent, obj, **kwargs)

    def _load_recursive(self, eid, **kwargs):
        """
        From a Session ID and dataset types, queries Alyx database, downloads the data
        from Globus, and loads into numpy array. Supports multiple sessions
        """
        if isinstance(eid, str):
            return self._load(eid, **kwargs)
        if isinstance(eid, list):
            # dataclass output requested
            if kwargs.get('dclass_output', False):
                for i, e in enumerate(eid):
                    if i == 0:
                        out = self._load(e, **kwargs)
                    else:
                        out.append(self._load(e, **kwargs))
            else:  # list output requested
                out = []
                for e in eid:
                    out.append(self._load(e, **kwargs)[0])
            return out

    @refresh
    def pid2eid(self, pid: str, query_type='auto') -> (str, str):
        """
        Given an Alyx probe UUID string, returns the session id string and the probe label
        (i.e. the ALF collection)

        :param pid: A probe UUID
        :param query_type: Query mode, options include 'auto', 'remote' and 'refresh'
        :return: (experiment ID, probe label)
        """
        if query_type != 'remote':
            self.refresh_cache(query_type)
        if query_type == 'local' and 'insertions' not in self._cache.keys():
            raise NotImplementedError('Converting probe IDs required remote connection')
        rec = self.alyx.rest('insertions', 'read', id=pid)
        return rec['session'], rec['name']

    def _ls(self, table, verbose=False):
        """
        Queries the database for a list of 'users' and/or 'dataset-types' and/or 'subjects' fields

        :param table: the table (s) to query among: 'dataset-types','users'
         and 'subjects'; if empty or None assumes all tables
        :type table: str
        :param verbose: [False] prints the list in the current window
        :type verbose: bool

        :return: list of names to query, list of full raw output in json serialized format
        :rtype: list, list
        """
        assert isinstance(table, str)
        table = self.autocomplete(table)
        table_field_names = {
            'dataset-types': 'name',
            'datasets': 'name',
            'users': 'username',
            'subjects': 'nickname',
            'labs': 'name'}

        field_name = table_field_names[table]
        full_out = self.alyx.get('/' + table)
        list_out = [f[field_name] for f in full_out]
        if verbose:
            pprint(list_out)
        return list_out, full_out

    def autocomplete(self, term):
        """ TODO Move to super class
        Validate search term and return complete name, e.g. autocomplete('subj') == 'subject'
        """
        full_key = (x for x in self.search_terms if x.lower().startswith(term))
        key_ = next(full_key, None)
        if not key_:
            if term.lower() in ('dtype', 'dtypes', 'dataset_types', 'dataset_type'):
                _logger.warning('Searching by dataset type is deprecated')
                return 'dataset_type'
            raise ValueError(f'Invalid search term "{term}"')
        elif next(full_key, None):
            raise ValueError(f'Ambiguous search term "{term}"')
        return key_

    # def search(self, dataset_types=None, users=None, subjects=None, date_range=None,
    #            lab=None, number=None, task_protocol=None, details=False):
    def search(self, details=False, query_type=None, **kwargs):
        """
        Applies a filter to the sessions (eid) table and returns a list of json dictionaries
         corresponding to sessions.

        For a list of search terms, use the methods

        >>> one.search_terms

        :param dataset_types: list of dataset_types
        :param date_range: list of 2 strings or list of 2 dates that define the range
        :param details: default False, returns also the session details as per the REST response
        :param lab: a str or list of lab names
        :param location: a str or list of lab location (as per Alyx definition) name
                         Note: this corresponds to the specific rig, not the lab geographical
                         location per se
        :param number: number of session to be returned; will take the first n sessions found
        :param performance_lte / performance_gte: search only for sessions whose performance is
        less equal or greater equal than a pre-defined threshold as a percentage (0-100)
        :param subjects: a list of subjects nickname
        :param task_protocol: a str or list of task protocol name (can be partial, i.e.
                              any task protocol containing that str will be found)
        :param users: a list of Alyx usernames
        :return: list of eids, if details is True, also returns a list of json dictionaries,
         each entry corresponding to a matching session
        """
        query_type = query_type or self.mode
        if query_type != 'remote':
            return super(OneAlyx, self).search(details=details, query_type=query_type, **kwargs)

        # small function to make sure string inputs are interpreted as lists
        def validate_input(inarg):
            if isinstance(inarg, str):
                return [inarg]
            elif isinstance(inarg, int):
                return [str(inarg)]
            else:
                return inarg

        # loop over input arguments and build the url
        url = '/sessions?'
        for key, value in kwargs.items():
            field = self.autocomplete(key)  # Validate and get full name
            # check that the input matches one of the defined filters
            if field == 'date_range':
                query = _validate_date_range(value)
                url += f'&{field}=' + ','.join(x.date().isoformat() for x in query)
            elif field == 'dataset_type':  # legacy
                url += '&dataset_type=' + ','.join(validate_input(value))
            elif field == 'dataset':
                url += ('&django=data_dataset_session_related__dataset_type__name__icontains,' +
                        ','.join(validate_input(value)))
            else:  # TODO Overload search terms (users, etc.)
                url += f'&{field}=' + ','.join(validate_input(value))
        # implements the loading itself
        ses = self.alyx.get(url)
        if len(ses) > 2500:
            eids = [s['url'] for s in tqdm.tqdm(ses)]  # flattens session info
        else:
            eids = [s['url'] for s in ses]
        eids = [e.split('/')[-1] for e in eids]  # remove url to make it portable

        if details:
            for s in ses:
                if all([s.get('lab'), s.get('subject'), s.get('start_time')]):
                    s['local_path'] = str(Path(self._cache_dir, s['lab'], 'Subjects',
                                               s['subject'], s['start_time'][:10],
                                               str(s['number']).zfill(3)))
                else:
                    s['local_path'] = None
            return eids, ses
        else:
            return eids

    def download_dataset(self, dset, cache_dir=None, update_cache=True, **kwargs):
        """
        Download a dataset from an alyx REST dictionary
        :param dset: single dataset dictionary from an Alyx REST query OR URL string
        :param cache_dir: root directory to save the data in (home/downloads by default)
        :return: local file path
        """
        if isinstance(dset, str):
            url = dset
            id = self.path2record(url).index
        else:
            if 'file_records' not in dset:  # Convert dataset Series to alyx dataset dict
                url = self.record2url(dset)
                id = dset.index
            else:
                url = next((fr['data_url'] for fr in dset['file_records']
                            if fr['data_url'] and fr['exists']), None)
                id = dset['id']

        if not url:
            # str_dset = Path(dset['collection']).joinpath(dset['name'])
            # str_dset = dset['rel_path']
            _logger.warning("Dataset not found")
            if update_cache:
                if isinstance(id, str) and self._index_type('datasets') is int:
                    id = parquet.str2np(id)
                elif self._index_type('datasets') is str and not isinstance(id, str):
                    id = parquet.np2str(id)
                self._cache['datasets'].at[id, 'exists'] = False
            return
        target_dir = Path(cache_dir or self._cache_dir, alfio.get_alf_path(url)).parent
        return self._download_file(url=url, target_dir=target_dir, **kwargs)

    def _tag_mismatched_file_record(self, url):
        fr = self.alyx.rest('files', 'list', django=f'dataset,{Path(url).name.split(".")[-2]},'
                                                    f'data_repository__globus_is_personal,False')
        if len(fr) > 0:
            json_field = fr[0]['json']
            if json_field is None:
                json_field = {'mismatch_hash': True}
            else:
                json_field.update({'mismatch_hash': True})
            self.alyx.rest('files', 'partial_update',
                           id=fr[0]['url'][-36:], data={'json': json_field})

    def _download_file(self, url, target_dir,
                       clobber=False, offline=None, keep_uuid=False, file_size=None, hash=None):
        """
        Downloads a single file from an HTTP webserver
        :param url:
        :param clobber: (bool: False) overwrites local dataset if any
        :param offline:
        :param keep_uuid:
        :param file_size:
        :param hash:
        :return:
        """
        if offline is None:
            offline = self.mode == 'local'
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        local_path = target_dir / os.path.basename(url)
        if not keep_uuid:
            local_path = alfio.remove_uuid_file(local_path, dry=True)
        if Path(local_path).exists():
            # the local file hash doesn't match the dataset table cached hash
            hash_mismatch = hash and hashfile.md5(Path(local_path)) != hash
            file_size_mismatch = file_size and Path(local_path).stat().st_size != file_size
            if (hash_mismatch or file_size_mismatch) and not offline:
                clobber = True
                if not self.alyx.silent:
                    _logger.warning(f'local md5 or size mismatch, re-downloading {local_path}')
        # if there is no cached file, download
        else:
            clobber = True
        if clobber and not offline:
            local_path, md5 = self.alyx.download_file(
                url, cache_dir=str(target_dir), clobber=clobber, return_md5=True)
            # post download, if there is a mismatch between Alyx and the newly downloaded file size
            # or hash flag the offending file record in Alyx for database maintenance
            hash_mismatch = hash and md5 != hash
            file_size_mismatch = file_size and Path(local_path).stat().st_size != file_size
            if hash_mismatch or file_size_mismatch:
                self._tag_mismatched_file_record(url)
                # TODO Update cache here
        if keep_uuid:
            return local_path
        else:
            return alfio.remove_uuid_file(local_path)

    @staticmethod
    def setup(**kwargs):
        """
        TODO Interactive command tool that sets up cache for ONE.
        """
        root_dir = input('Select a directory from which to build cache')
        if root_dir:
            import alf.onepqt
            print('Building ONE cache from filesystem...')
            alf.onepqt.make_parquet_db(root_dir, **kwargs)

    def eid2path(self, eid: str, query_type=None) -> Listable(Path):
        """
        From an experiment id or a list of experiment ids, gets the local cache path
        :param eid: eid (UUID) or list of UUIDs
        :param query_type: if set to 'remote', will force database connection TODO rename to query_type
        :return: eid or list of eids
        """
        # If eid is a list of eIDs recurse through list and return the results
        if isinstance(eid, list):
            path_list = []
            for p in eid:
                path_list.append(self.eid2path(p))  # TODO unwrap before call
            return path_list
        # If not valid return None
        if not alfio.is_uuid_string(eid):
            print(eid, " is not a valid eID/UUID string")
            return

        # first try avoid hitting the database
        mode = query_type or self.mode
        if mode != 'remote':
            cache_path = super().eid2path(eid)
            if cache_path or mode == 'local':
                return cache_path

        # if it wasn't successful, query Alyx
        ses = self.alyx.rest('sessions', 'list', django=f'pk,{eid}')
        if len(ses) == 0:
            return None
        else:
            return Path(self._cache_dir).joinpath(
                ses[0]['lab'], 'Subjects', ses[0]['subject'], ses[0]['start_time'][:10],
                str(ses[0]['number']).zfill(3))

    @refresh
    def path2eid(self, path_obj: Union[str, Path], query_type=None) -> Listable(Path):
        """
        From a local path, gets the experiment id
        :param path_obj: local path or list of local paths
        :param query_type: if set to 'remote', will force database connection
        :return: eid or list of eids
        """
        # If path_obj is a list recurse through it and return a list
        if isinstance(path_obj, list):
            path_obj = [Path(x) for x in path_obj]
            eid_list = []
            for p in path_obj:
                eid_list.append(self.path2eid(p))  # TODO Unwrap before call
            return eid_list
        # else ensure the path ends with mouse,date, number
        path_obj = Path(path_obj)
        session_path = alfio.get_session_path(path_obj)
        # if path does not have a date and a number return None
        if session_path is None:
            return None

        # try the cached info to possibly avoid hitting database
        mode = query_type or self.mode
        if mode != 'remote':
            cache_eid = super().path2eid(path_obj)
            if cache_eid or mode == 'local':
                return cache_eid

        # if not search for subj, date, number XXX: hits the DB TODO unwrap before call
        uuid = self.search(subject=session_path.parts[-3],
                           date_range=session_path.parts[-2],
                           number=session_path.parts[-1],
                           query_type='remote')

        # Return the uuid if any
        return uuid[0] if uuid else None

    @refresh
    def path2url(self, filepath, query_type='auto'):
        """
        Given a local file path, returns the URL of the remote file.
        :param filepath: A local file path
        :return: A URL string
        TODO add query_type to docstring
        """
        if query_type != 'remote':
            return super(OneAlyx, self).path2url(filepath)
        eid = self.path2eid(filepath)
        try:
            dataset, = self.alyx.rest('datasets', 'list', session=eid, name=Path(filepath).name)
            return next(
                r['data_url'] for r in dataset['file_records'] if r['data_url'] and r['exists'])
        except (ValueError, StopIteration):
            raise alferr.ALFObjectNotFound(f'File record for {filepath} not found on Alyx')

    @parse_id
    def datasets_from_type(self, eid, dataset_type, full=False):
        """
        Get list of datasets belonging to a given dataset type for a given session
        :param eid: Experiment session identifier; may be a UUID, URL, experiment reference string
        details dict or Path
        :param dataset_type: A dataset type, e.g. camera.times
        :param full: If True, a dictionary of details is returned for each dataset
        :return: A list of datasets belonging to that session's dataset type
        """
        restriction = f'session__id,{eid},dataset_type__name,{dataset_type}'
        datasets = self.alyx.rest('datasets', 'list', django=restriction)
        return datasets if full else [d['name'] for d in datasets]

    def dataset2type(self, dset):
        """Return dataset type from dataset"""
        # Ensure dset is a str uuid
        if isinstance(dset, str) and not alfio.is_uuid_string(dset):
            dset = self._dataset_name2id(dset)
        if isinstance(dset, np.ndarray):
            dset = parquet.np2str(dset)[0]
        if isinstance(dset, tuple) and all(isinstance(x, int) for x in dset):
            dset = parquet.np2str(np.array(dset))
        if not alfio.is_uuid_string(dset):
            raise ValueError('Unrecognized name or UUID')
        return self.alyx.rest('datasets', 'read', id=dset)['dataset_type']

    def describe_revision(self, revision):
        raise NotImplementedError('Requires changes to revisions endpoint')
        if rec := self.alyx.rest('revisions', 'list', name=revision):
            print(rec[0]['description'])
        else:
            print(f'Revision "{revision}" not found')

    def _dataset_name2id(self, dset_name, eid=None):
        # TODO finish function
        datasets = self.list_datasets(eid) if eid else self._cache['datasets']
        # Get ID of fist matching dset
        for idx, rel_path in datasets['rel_path'].items():
            if dset_name in rel_path:
                return idx

    def get_details(self, eid: str, full: bool = False):
        """ Returns details of eid like from one.search, optional return full
        session details.
        """
        # If eid is a list of eIDs recurse through list and return the results
        if isinstance(eid, list):
            details_list = []
            for p in eid:
                details_list.append(self.get_details(p, full=full))
            return details_list
        # If not valid return None
        if not alfio.is_uuid_string(eid):
            print(eid, " is not a valid eID/UUID string")
            return
        # load all details
        dets = self.alyx.rest("sessions", "read", eid)
        if full:
            return dets
        # If it's not full return the normal output like from a one.search
        det_fields = ["subject", "start_time", "number", "lab", "project",
                      "url", "task_protocol", "local_path"]
        out = {k: v for k, v in dets.items() if k in det_fields}
        out.update({'local_path': self.eid2path(eid)})
        return out

    # def _update_cache(self, ses, dataset_types):
    #     """
    #     TODO move to One; currently unused
    #     :param ses: session details dictionary as per Alyx response
    #     :param dataset_types:
    #     :return: is_updated (bool): if the cache was updated or not
    #     """
    #     save = False
    #     pqt_dsets = _ses2pandas(ses, dtypes=dataset_types)
    #     # if the dataframe is empty, return
    #     if pqt_dsets.size == 0:
    #         return
    #     # if the cache is empty create the cache variable
    #     elif self._cache.size == 0:
    #         self._cache = pqt_dsets
    #         save = True
    #     # the cache is not empty and there are datasets in the query
    #     else:
    #         isin, icache = ismember2d(pqt_dsets[['id_0', 'id_1']].to_numpy(),
    #                                   self._cache[['id_0', 'id_1']].to_numpy())
    #         # check if the hash / filesize fields have changed on patching
    #         heq = (self._cache['hash'].iloc[icache].to_numpy() ==
    #                pqt_dsets['hash'].iloc[isin].to_numpy())
    #         feq = np.isclose(self._cache['file_size'].iloc[icache].to_numpy(),
    #                          pqt_dsets['file_size'].iloc[isin].to_numpy(),
    #                          rtol=0, atol=0, equal_nan=True)
    #         eq = np.logical_and(heq, feq)
    #         # update new hash / filesizes
    #         if not np.all(eq):
    #             self._cache.iloc[icache, 4:6] = pqt_dsets.iloc[np.where(isin)[0], 4:6].to_numpy()
    #             save = True
    #         # append datasets that haven't been found
    #         if not np.all(isin):
    #             self._cache = self._cache.append(pqt_dsets.iloc[np.where(~isin)[0]])
    #             self._cache = self._cache.reindex()
    #             save = True
    #     if save:
    #         # before saving makes sure pandas did not cast uuids in float
    #         typs = [t for t, k in zip(self._cache.dtypes, self._cache.keys()) if 'id_' in k]
    #         assert (all(map(lambda t: t == np.int64, typs)))
    #         # if this gets too big, look into saving only when destroying the ONE object
    #         parquet.save(self._cache_file, self._cache)


def _validate_date_range(date_range):
    """
    Validates and arrange date range in a 2 elements list

    Examples:
        _validate_date_range('2020-01-01')  # On this day
        _validate_date_range(datetime.date(2020, 1, 1))
        _validate_date_range(np.array(['2022-01-30', '2022-01-30'], dtype='datetime64[D]'))
        _validate_date_range(pd.Timestamp(2020, 1, 1))
        _validate_date_range(np.datetime64(2021, 3, 11))
        _validate_date_range(['2020-01-01'])  # from date
        _validate_date_range(['2020-01-01', None])  # from date
        _validate_date_range([None, '2020-01-01'])  # up to date
    """
    if date_range is None:
        return

    # Ensure we have exactly two values
    if isinstance(date_range, str) or not isinstance(date_range, Iterable):
        # date_range = (date_range, pd.Timestamp(date_range) + pd.Timedelta(days=1))
        dt = pd.Timedelta(days=1) - pd.Timedelta(milliseconds=1)
        date_range = (date_range, pd.Timestamp(date_range) + dt)
    elif len(date_range) == 1:
        date_range = [date_range[0], pd.Timestamp.max]
    elif len(date_range) != 2:
        raise ValueError

    # For comparisons, ensure both values are pd.Timestamp (datetime, date and datetime64
    # objects will be converted)
    start, end = date_range
    start = start or pd.Timestamp.min  # Convert None to lowest possible date
    end = end or pd.Timestamp.max  # Convert None to highest possible date

    # Convert to timestamp
    if not isinstance(start, pd.Timestamp):
        start = pd.Timestamp(start)
    if not isinstance(end, pd.Timestamp):
        end = pd.Timestamp(end)

    return start, end
