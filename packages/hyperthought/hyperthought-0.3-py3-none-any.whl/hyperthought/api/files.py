import collections
from copy import deepcopy
from enum import Enum
import math
import os

import requests

from .base import GenericAPI, ERROR_THRESHOLD
from .. import utils


class FileTransferProgressHandler:
    """
    Invokes a callback when transfer size thresholds have been reached.

    Parameters
    ----------
    chunk_size : int
        The constant interval between size thresholds.
    total_size : int
        The total size of a file in bytes.
    callback : callable
        The callback to be invoked when a size threshold has been crossed.
    """

    def __init__(self, chunk_size, total_size, callback):
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer")
            
        if not isinstance(total_size, int) or total_size <= 0:
            raise ValueError("total_size must be a positive integer")
        
        if not callable(callback):
            raise ValueError("callback must be callable")
            
        # TODO:  Callback must accept an integer (number of chunks already added).
            
        self.chunk_size = chunk_size
        self.total_size = total_size
        self.callback = callback
        
        # Invoke callback when current size is >= threshold.
        self.current_size = 0
        self.callback_threshold = chunk_size
        
    def add(self, increment):
        """
        Update total size (number of bytes transferred) by increment.

        self.callback will be invoked if the addition of the new increment
        crosses a size threshold.

        Parameters
        ----------
        increment : int
            The number of bytes transferred since the last invocation.
        """
        if not increment:
            return

        self.current_size += increment
        
        if self.current_size >= self.total_size:
            # NOTE:  Do not use self.current_size as the numerator.
            #        It may be larger than self.total_size, for reasons unknown.
            self.callback(math.ceil(self.total_size / self.chunk_size))
            return
        
        if self.current_size >= self.callback_threshold:
            self.callback(math.floor(self.current_size / self.chunk_size))

            while self.callback_threshold <= self.current_size:
                self.callback_threshold = min(
                    self.callback_threshold + self.chunk_size,
                    self.total_size
                )


class FilesAPI(GenericAPI):
    """
    Files API switchboard.

    Contains methods that (roughly) correspond to endpoints for the
    HyperThought files app.  The methods simplify some tasks, such as
    uploading and downloading files.

    Parameters
    ----------
    auth : auth.Authorization
        Authorization object used to get headers and cookies needed to call
        HyperThought endpoints.
    """

    class FileType(Enum):
        """
        Enum describing types of file documents to be returned from methods.
        
        See the get_from_location method for an example.
        """
        # FILES_ONLY = 0
        FOLDERS_ONLY = 1
        FILES_AND_FOLDERS = 2

    def __init__(self, auth):
        super().__init__(auth)
        self._backend = None
        
    def get_document(self, id):
        """
        Get a database document for a file, given its id.

        Parameters
        ----------
        id : str
            The database id for a file or folder.

        Returns
        -------
        A dict-like database document for the file with the given id.
        """
        r = requests.get(
            url='{}/api/files/'.format(self._base_url),
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            params={'id': id,},
            verify=False,
        )

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)
    
    def get_from_location(self, space=None, space_id=None, path=None,
                          file_type=None):
        """
        Get HyperThought files/folders from a specific location.

        Parameters
        ----------
        space : str or None
            The space of interest.  Must be 'group', 'project', or 'user'.
            If None, will default to 'user'.
        space_id : str or None
            The id of a group or project, or the username for a user.
            If None, will default to the user's username.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        file_type : FileType or None
            An enum value for the type of files to get.  A None value will
            default to FileType.FILES_AND_FOLDERS.

        Returns
        -------
        A list of documents (dicts) from the database corresponding to
        files/folders at the specified path in the specified space.
        """
        # Validate parameters.
        space = self._validate_space(space)
        space_id = self._validate_space_id(space, space_id)
        path = self._validate_path(path)
        file_type = self._validate_file_type(file_type)

        files_url = '{}/api/files/'.format(self._base_url)
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        params = {'path': path}

        if space == 'project':
            params['method'] = 'project_files'
            params['project'] = space_id
        elif space == 'group':
            params['method'] = 'group_files'
            params['group'] = space_id
        else:
            params['method'] = 'user_files'

        if file_type == self.FileType.FOLDERS_ONLY:
            params['type'] = utils.FOLDER_TYPE

        r = requests.get(files_url, headers=headers, cookies=cookies,
                         params=params, verify=False)
        
        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        output = r.json()
        
        # TODO:  Make sure this is necessary.
        if output is None:
            output = []

        # TODO:  Make sure this is necessary.
        if not isinstance(output, list):
            output = [output]

        return output

    def get_id(self, name, space=None, space_id=None, path=None):
        """
        Get an id for a file/folder with a given name at a given location.

        Parameters
        ----------
        name : str
            The name of the file system entry.
        space : str or None
            The space of interest.  Must be 'group', 'project', or 'user'.
            If None, will default to 'user'.
        space_id : str or None
            The id of a group or project, or the username for a user.
            If None, will default to the user's username.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'

        Returns
        -------
        An id, if the specified file/folder exists, else None.
        """
        # Validate parameters.
        name = self._validate_name(name)
        space = self._validate_space(space)
        space_id = self._validate_space_id(space, space_id)
        path = self._validate_path(path)

        files_url = '{}/api/files/'.format(self._base_url)
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        params = {
            'path': path,
            'search': name,
        }

        if space == 'project':
            params['method'] = 'project_files'
            params['project'] = space_id
        elif space == 'group':
            params['method'] = 'group_files'
            params['group'] = space_id
        else:
            params['method'] = 'user_files'

        r = requests.get(files_url, headers=headers, cookies=cookies,
                         params=params, verify=False)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        if not r.json():
            return None

        for document in r.json():
            if document['content']['name'] == name:
                # Return the first match found.
                # Ideally, there should be only one.
                return document['content']['pk']

        return None

    def get_id_at_path(self, path, space=None, space_id=None):
        """
        Get a file id given a human readable path.

        Parameters
        ----------
        space : str
            The type of space.  Must be 'group', 'project', or 'user'.
        space_id : str
            The id for a group or project, or a username.
        path : str
            A human-readable path, e.g. 'path/to/file.txt'

        Returns
        -------
        The id for the file corresponding to the given path if one exists,
        otherwise None. 
        """
        space = self._validate_space(space)
        space_id = self._validate_space_id(space, space_id)

        if not isinstance(path, str):
            raise ValueError("path must be a string")

        sep = utils.PATH_SEP
        id_sep = utils.ID_PATH_SEP
        tokens = path.strip(sep).split(sep)
        id_path = id_sep
        id_ = None

        for token in tokens:
            id_ = self.get_id(
                name=token,
                space=space,
                space_id=space_id,
                path=id_path,
            )
            
            if id_ is None:
                break
            
            id_path += id_ + id_sep

        return id_

    def get_object_link(self, space=None, space_id=None, id_=None, path=None):
        """
        Get an object link string to store a link as a metadata value.

        Parameters
        ----------
        space : str
            The type of space.  Must be 'group', 'project', or 'user'.
        space_id : str
            The id for a group or project, or a username.
        id_ : str or None
            The id for the file of interest.
        path : str
            A human-readable path to the file of interest,
            e.g. 'path/to/file.txt'

        If id_ is not provided, the other parameters must be.

        Returns
        -------
        An object link string.
        """
        if not id_ is None and not isinstance(id_, str):
            raise ValueError(f"string expected for id_, found {type(path)}")

        get_link = lambda id_: f"/files/filesystementry/{id_}"

        if id_ is None:
            id_ = self.get_id_at_path(
                space=space,
                space_id=space_id,
                path=path,
            )

        return get_link(id_)

    def create_folder(self, name, space=None, space_id=None, path=None,
                      metadata=None,):
        """
        Create a folder in HyperThought.

        Parameters
        ----------
        name : str
            The name of the folder to create.
        space : str or None
            The space of interest.  Must be 'group', 'project', or 'user'.
            If None, will default to 'user'.
        space_id : str or None
            The id of a group or project, or the username for a user.
            If None, will default to the user's username.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        metadata : list-like
            A list of metadata items in the internal format.
            TODO:  encapsulate the internal format with a stable API format.

        Returns
        -------
        The id of the new folder.
        """
        name = self._validate_name(name)
        space = self._validate_space(space)
        space_id = self._validate_space_id(space, space_id)
        path = self._validate_path(path)
        # TODO:     Validate metadata.

        url = '{}/api/files/create-folder/'.format(self._auth.get_base_url())
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        request_data = {
            'space': space,
            'space_id': space_id,
            'path': path,
            'name': name,
            'metadata': metadata,
        }

        r = requests.post(url, headers=headers, cookies=cookies,
                          json=request_data, verify=False)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        folder_id = r.json()['document']['content']['pk']
        return folder_id

    def move(self,
             from_space=None, from_space_id=None, from_paths=None,
             file_ids=None,
             to_space=None, to_space_id=None, to_directory=None,
             to_directory_id=None,
             ):
        """
        Move files from one file system location to another.

        Parameters
        ----------
        from_space : str or None
            Will only be used if file_ids is None.
            Type of space where files currently exist.
            Must be 'group', 'project', or 'user'.
        from_space_id : str or None
            Will only be used if file_ids is None.
            ID of space where files currently exist.
            Group or project id, or username.
        from_paths : (list of str) or None
            Will only be used if file_ids is None.
            List of human-readable paths where files currently exist.
        file_ids : (list of str) or None
            IDs of files to be moved.
            If None, from_space, from_space_id, and from_paths must be supplied.
        to_space : str or None
            Will only be used if to_directory_id is None.
            Type of space where files should be moved.
            Must be 'group', 'project', or 'user'.
        to_space_id : str or None
            Will only be used if to_directory_id is None.
            ID of space where files should be moved.
            Group or project id, or username.
        to_directory : str or None
            Will only be used if to_directory_id is None.
            Human-readable path to destination directory in destination space.
        to_directory_id : str or None
            ID of directory where files should be moved.
            If None, to_space, to_space_id, and to_directory must be supplied.
            Cannot be used if files are moved to the root directory of the
            destination space, since the root directory has no id.

        Returns
        -------
        Data on the enqueueing operation, including the number of items
        processed and queue status for each item.
        """
        if (
            file_ids is None
            and
            (
                from_space is None
                or
                from_space_id is None
                or
                from_paths is None
            )
        ):
            raise ValueError(
                "Either the from_ids parameter or all three of the "
                "from_space, from_space_id, and from_paths parameters "
                "must be supplied."
            )

        if (
            to_directory_id is None
            and
            (
                to_space is None
                or
                to_space_id is None
                or
                to_directory is None
            )
        ):
            raise ValueError(
                "Either the to_directory_id parameter or all three of the "
                "to_space, to_space_id, and to_directory parameters "
                "must be supplied."
            )

        if from_space is not None and from_space not in utils.VALID_SPACES:
            raise ValueError(
                "from_space must be None of one of "
                f"{','.join(utils.VALID_SPACES)}")

        if to_space is not None and to_space not in utils.VALID_SPACES:
            raise ValueError(
                "to_space must be None of one of "
                f"{','.join(utils.VALID_SPACES)}")

        if file_ids is not None and not isinstance(file_ids, list):
            raise ValueError("file_ids must be None or a list")

        if from_paths is not None and not isinstance(from_paths, list):
            raise ValueError("from_paths must be None or a list")

        common_data = {
            'type': 'move',
        }

        # Use directory id if present.
        if to_directory_id is not None:
            common_data['toUuid'] = to_directory_id
        else:
            common_data['toSpaceType'] = to_space
            common_data['toSpace'] = to_space_id
            common_data['toDir'] = to_directory

        data = []

        # Use file_ids if present.
        if file_ids is not None:
            for file_id in file_ids:
                item = deepcopy(common_data)
                item['fromUuid'] = file_id
                data.append(item)
        else:
            for from_path in from_paths:
                item = deepcopy(common_data)
                item['fromSpaceType'] = from_space
                item['fromSpace'] = from_space_id
                item['fromPath'] = from_path
                data.append(item)

        url = '{}/api/files/queue/'.format(self._auth.get_base_url())
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        r = requests.post(url, headers=headers, cookies=cookies,
                          json=data, verify=False)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)
            return {
                'processed': 0,
                'results': 'ERROR'
            }
        else:
            return r.json()

    def upload(self, local_path,
               space=None, space_id=None, path=None,
               metadata=None,
               progress_callback=None, n_chunks=100,):
        """
        Upload a file to HyperThought.

        Parameters
        ----------
        local_path : str
            The path to a file on the local system.
        space : str or None
            The space of interest.  Must be 'group', 'project', or 'user'.
            If None, will default to 'user'.
        space_id : str or None
            The id of a group or project, or the username for a user.
            If None, will default to the user's username.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        metadata : dict-like or None
            Metadata for the file.
        progress_callback : callable (int -> None) or None
            A callback for handling upload progress.  Will be called each time
            a given number of bytes (chunk) is uploaded.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.

        Returns
        -------
        A tuple containing the file id and the name of the file.  (The name is
        returned in case it is changed by HyperThought™ to ensure uniqueness.)
        """
        # Validate parameters.
        local_path = self._validate_local_path(local_path)
        space = self._validate_space(space)
        space_id = self._validate_space_id(space, space_id)
        path = self._validate_path(path)

        if metadata is None:
            metadata = []
            
        metadata = self._validate_metadata(metadata)

        # TODO:  Move this into a validation function.
        if progress_callback is not None and not callable(progress_callback):
            raise ValueError("progress_callback must be a callable or None")

        if not isinstance(n_chunks, int):
            raise ValueError("n_chunks must be an int")

        # Get file name and size using the local path.
        active_local_path = utils.get_active_path(local_path)
        name = active_local_path.split(os.path.sep)[-1]
        size = os.path.getsize(active_local_path)
        
        # Get an upload url.
        url, file_id = self._get_upload_url(
            space=space,
            space_id=space_id,
            name=name,
            size=size,
            path=path,
            metadata=metadata,
        )

        # Use the url to upload the file.
        self._upload_using_url(
            url,
            active_local_path,
            progress_callback,
            n_chunks,
        )

        # Move the file from the temporary to the permanent file collection.
        file_name = self._temp_to_perm(file_id)

        # Return the file id.
        return (file_id, file_name,)

    def download(self, file_id, directory, progress_callback=None, n_chunks=100):
        """
        Download a file from HyperThought to the local file system.

        Parameters
        ----------
        file_id : str
            The HyperThought id for a file to be downloaded.
        directory : str
            A local directory path to which the file will be downloaded.
        progress_callback : callable (int -> None) or None
            A callback for handling upload progress.  Will be called each time
            a given number of bytes (chunk) is uploaded.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.
        """
        # Validate parameters.
        self._validate_id(file_id)
        self._validate_local_path(directory)

        # Make sure the path is a directory.
        # TODO:  This was changed to get a release ready.
        # TODO:  Restore the ability to handle long paths in Windows.
        active_directory_path = directory #utils.get_active_path(directory)
        if not os.path.isdir(active_directory_path):
            print(f"{directory} is not a directory")
            raise ValueError(f"{directory} is not a directory")

        # Get the file name.
        file_document = self.get_document(id=file_id)
        file_size = file_document['content']['size']
        file_name = file_document['content']['name']
        file_path = os.path.join(active_directory_path, file_name)

        # Get a download url.
        url = self._get_download_url(file_id)

        # Use the url to download the file.
        self._download_using_url(
            download_url=url,
            local_path=file_path,
            file_size=file_size,
            progress_callback=progress_callback,
            n_chunks=n_chunks,
        )

    def delete(self, id):
        """
        Delete a file or folder.

        Parameters
        ----------
        id : str
            The id of the file/folder to be deleted.
        """
        # Validate parameters.
        id = self._validate_id(id)

        r = requests.delete(
            url='{}/api/files/'.format(self._base_url),
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            json={'id': id,},
            verify=False,
        )

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

    def update_metadata(self, file_id, new_metadata):
        """
        Update metadata for a file.

        Parameters
        ----------
        file_id : str
            The id (uuid) for the file of interest.
        new_metadata : list of dict
            New metadata for the file.
            This will replace any existing metadata.
            Merging will need to be done client-side.
        """
        # NOTE:  This method throws exceptions.
        new_metadata = self._validate_metadata(new_metadata)
        data = {
            'file_id': file_id,
            'updates': {
                'metadata': new_metadata,
            }
        }
        url = f"{self._base_url}/api/files/"
        r = requests.patch(
            url=url,
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            json=data,
            verify=False,
        )

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method throws exceptions.
            self._report_api_error(r)

    def get_backend(self):
        """
        Get the files backend.
        
        Returns
        -------
        A string describing the file backend, e.g. 's3' or 'default'.
        """
        if self._backend is not None:
            return self._backend
        
        url = f'{self._base_url}/api/files/backend/'
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        r = requests.get(url=url, headers=headers, cookies=cookies,
                         verify=False)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        self._backend = r.json()['backend']
        # TODO:  Replace assertion with proper error handling.
        assert self._backend in ('s3', 'default',)
        return self._backend

    def is_folder(self, document):
        """Determine whether a document represents a folder in the
        HyperThought file system."""
        if not isinstance(document, collections.Mapping):
            return False

        if 'content' not in document:
            return False

        if 'ftype' not in document['content']:
            return False

        return document['content']['ftype'] == utils.FOLDER_TYPE

    def _get_upload_url(self, name, size, space='user', space_id=None,
                        path=None, metadata=None):
        """
        Get presigned url to upload a file.

        Called from self.upload_file.

        Parameters
        ----------
        name : str
            The name of the file.
        size : int
            The size of the file in bytes.
        space : str
            The type of space.  Must be 'group', 'project', or 'user'.
            Wil be 'user' (the user's personal file space) by default.
        space_id : str or None
            The id for a group or project.  Irrelevant for user spaces.
        path : str or None
            The path to the directory that will contain the file.
            If None, will default to root path.
        metadata : dict-like or None
            Metadata for the file.
            TODO:  Change metadata to use the new structure.

        Returns
        -------
        A tuple containing the presigned url of interest as well as the file id
        for the file to be uploaded.
        """
        # TODO:  Validate parameters.

        if space_id is None:
            space_id = self._auth.get_username()

        if path is None:
            path = utils.ID_PATH_SEP

        request_data = {
            'space': space,
            'space_id': space_id,
            'path': path,
            'name': name,
            'size': size,
            'metadata': metadata,
        }
        generate_url = '{}/api/files/generate-upload-url/'.format(
            self._base_url)
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        r = requests.post(generate_url, headers=headers, cookies=cookies,
                          json=request_data, verify=False)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        url = r.json()['url']
        file_id = r.json()['fileId']

        # urls for locally stored files (default as opposed to s3 backend)
        # will be stripped of their protocol and hyperthought domain.
        # This is done to make presigned urls work with the DataTables
        # jQuery plugin in the HyperThought UI.
        if not url.startswith('http'):
            if not url.startswith('/'):
                url = f"/{url}"
            url = f"{self._base_url}{url}"

        return url, file_id

    def _upload_using_url(self, upload_url, local_path,
                          progress_callback, n_chunks):
        """
        Use a url to upload a file.

        Called from self.upload.

        Parameters
        ----------
        upload_url : str
            The url to which the file should be uploaded.
        local_path : str
            The local path to the file to be uploaded.
        progress_callback : callable(int -> None) or None
            A callable to provide progress on upload status.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.
        """
        upload_url = self._validate_url(upload_url)
        local_path = self._validate_local_path(local_path)
        
        file_size = os.path.getsize(local_path)
        file_handle = open(local_path, 'rb')

        if progress_callback is not None:
            chunk_size = math.ceil(file_size / n_chunks)
            progress_handler = FileTransferProgressHandler(
                chunk_size=chunk_size,
                total_size=file_size,
                callback=progress_callback,
            )
            original_read = file_handle.read
            
            def new_read(size):
                progress_handler.add(size)
                return original_read(size)
                
            file_handle.read = new_read
        
        kwargs = {
            'url': upload_url,
            'data': file_handle,
            'verify': False,
            'stream': True,
            'headers': {},
        }

        if self.get_backend() == 'default':
            kwargs['headers'].update(self._auth.get_headers())
            # Content-Disposition (with file name) is required by Django 2.2.
            file_name = local_path.strip(utils.PATH_SEP).split(utils.PATH_SEP)[-1]
            kwargs['headers']['Content-Disposition'] = f"inline;filename={file_name}"
            kwargs['cookies'] = self._auth.get_cookies()
        else:
            # TODO:  Why can't this be removed?
            kwargs['headers'].update({
                'Content-Type': 'application/octet-stream'
            })

        r = requests.put(**kwargs)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)
            
        file_handle.close()

    def _temp_to_perm(self, file_id):
        """
        Move a file from the temporary (invisible) to the permanent (visible)
        file collection after the file has been completely uploaded.

        Parameters
        ----------
        id : str
            The HyperThought id for the file.
        """
        update_url = '{}/api/files/temp-to-perm/'.format(self._base_url)
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        request_data = {'file_ids': [file_id]}
        r = requests.patch(update_url, headers=headers, cookies=cookies,
                           json=request_data, verify=False)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        updated_files = r.json()['updated']

        if file_id in updated_files:
            return updated_files[file_id]

        return None

    def _get_download_url(self, file_id):
        """
        Get a url that can be used to download a file.

        Parameters
        ----------
        id : str
            The HyperThought id for a file of interest.

        Returns
        -------
        A url that can be used to download the file.
        """
        file_id = self._validate_id(file_id)

        generate_url = '{}/api/files/generate-download-url/'.format(
            self._base_url)
        headers = self._auth.get_headers()
        cookies = self._auth.get_cookies()
        params = {'id': file_id}

        r = requests.get(url=generate_url, headers=headers, cookies=cookies,
                         params=params, verify=False)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        return r.json()['url']

    def _download_using_url(self, download_url, local_path, file_size,
                            progress_callback, n_chunks):
        """
        Use a generated url to download a file.

        Parameters
        ----------
        download_url : str
            The generated url for downloading the file of interest.
            See self._get_download_url. 
        local_path : str
            The local system path where the downloaded file will be saved.
        progress_callback : callable (int -> None) or None
            A callback for handling upload progress.  Will be called each time
            a given number of bytes (chunk) is uploaded.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.
        """
        kwargs = {
            'url': download_url,
            'stream': True,
            'verify': False,
        }

        if self.get_backend() == 'default':
            kwargs['headers'] = self._auth.get_headers()
            kwargs['cookies'] = self._auth.get_cookies()

        progress_handler = None

        if progress_callback is not None:
            progress_chunk_size = math.ceil(file_size / n_chunks)
            progress_handler = FileTransferProgressHandler(
                chunk_size=progress_chunk_size,
                total_size=file_size,
                callback=progress_callback,
            )

        DOWNLOAD_CHUNK_SIZE = 8192

        with requests.get(**kwargs) as r:
            r.raise_for_status()

            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                    if chunk:   # filter out keep-alive new chunks
                        f.write(chunk)

                        if progress_handler:
                            progress_handler.add(DOWNLOAD_CHUNK_SIZE)

    def _validate_id(self, id_):
        assert isinstance(id_, str), f"expected string as id, found {type(id_)}"
        return id_

    def _validate_space(self, space=None):
        if space is None:
            space = 'user'

        # TODO:  Call error-handling function instead of raising an AssertionError.
        #        Same goes for all assertions in validation methods.
        assert space in ('group', 'project', 'user',), f"Invalid space: {space}"

        return space

    def _validate_space_id(self, space=None, space_id=None):
        if space is None:
            space = self._validate_space(space)

        if space == 'user' and space_id is None:
            space_id = self._auth.get_username()

        assert isinstance(space_id, str), f"string expected, found {type(space_id)}"
        return space_id

    def _validate_path(self, path):
        if path is None:
            path = utils.ID_PATH_SEP

        assert isinstance(path, str)
        assert path.startswith(utils.ID_PATH_SEP)
        assert path.endswith(utils.ID_PATH_SEP)
        return path

    def _validate_name(self, name):
        assert isinstance(name, str)
        return name

    def _validate_size(self, size):
        assert isinstance(size, int) and size >= 0
        return size

    def _validate_metadata(self, metadata):
        # Validate metadata structure.
        # TODO:  Consider moving outside this class.  (Same method c/b used
        #        for workflow metadata.)

        try:
            metadata = list(metadata)
        except TypeError:
            raise TypeError("Metadata must be a list-like sequence.")

        for item in metadata:
            try:
                dict(item)
            except TypeError:
                raise TypeError("Metadata items must be dict-like.")

            if 'keyName' not in item:
                raise ValueError(
                    "A metadata item must contain a key called 'keyName'."
                )

            if 'value' not in item:
                raise ValueError(
                    "A metadata item must contain a key called 'keyName'."
                )

            if 'type' not in item['value']:
                raise ValueError(
                    "A metadata item must have a key 'value' with subkey "
                    "'type'."
                )

            VALID_TYPES = ('link', 'string')

            if item['value']['type'] not in VALID_TYPES:
                raise ValueError(
                    "item['value']['type'] must be one of "
                    f"{', '.join(VALID_TYPES)}."
                )

            if 'link' not in item['value']:
                raise ValueError(
                    "A metadata item must have a key 'value' with subkey "
                    "'link'."
                )

            VALID_KEYS = {'keyName', 'value', 'unit', 'annotation'}
            
            item_keys = set(item.keys())
            invalid_keys = item_keys - VALID_KEYS

            if invalid_keys:
                raise ValueError(
                    f"Invalid keys for metadata item: {', '.join(invalid_keys)}."
                )

            # TODO:  Add additional checks relating to atomic data types.

        return metadata

    def _validate_url(self, url):
        # TODO:  Use regex?
        assert isinstance(url, str)
        return url

    def _validate_local_path(self, local_path):
        assert isinstance(local_path, str)
        assert os.path.exists(local_path)
        return local_path

    def _validate_file_type(self, file_type):
        if file_type is None:
            file_type = self.FileType.FILES_AND_FOLDERS

        assert isinstance(file_type, self.FileType)

        return file_type
