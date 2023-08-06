"""
Model class for MyTardis API v1's DataFileResource.
"""
from __future__ import print_function

import mimetypes
import json
import os
import cgi
import hashlib
import logging
from datetime import datetime

import requests
from six.moves import urllib

from ..conf import config
from ..utils import extend_url, add_filters
from ..utils.exceptions import DuplicateKey
from .model import Model
from .resultset import ResultSet
from .schema import Schema
from .schema import ParameterName

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def md5_sum(file_path, blocksize=65536):
    """
    Calculate MD5 checksum without reading the whole file into memory.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as datafile:
        buf = datafile.read(blocksize)
        while buf:
            hasher.update(buf)
            buf = datafile.read(blocksize)
        return hasher.hexdigest()


class DataFile(Model):
    """
    Model class for MyTardis API v1's DataFileResource.
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, response_dict, include_metadata=False):
        from .replica import Replica

        self.response_dict = response_dict
        self.id = response_dict['id']  # pylint: disable=invalid-name
        self.dataset = response_dict['dataset']
        self.directory = response_dict['directory'] or ""
        self.filename = response_dict['filename']
        self.size = response_dict['size']
        self.md5sum = response_dict['md5sum']
        self.replicas = []
        for replica_json in response_dict['replicas']:
            self.replicas.append(Replica(replica_json))
        self.parameter_sets = []
        if include_metadata:
            for datafile_param_set_json in response_dict['parameter_sets']:
                self.parameter_sets.append(
                    DataFileParameterSet(datafile_param_set_json))

    def __str__(self):
        """
        Return a string representation of a datafile
        """
        return "<%s: %s>" % (
            type(self).__name__, os.path.join(self.directory, self.filename))

    @property
    def verified(self):
        """
        All replicas (DFOs) must be verified and there must be
        at least one replica (DFO).
        """
        if not self.replicas:
            return False
        for replica in self.replicas:
            if not replica.verified:
                return False
        return True

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of datafiles.

        :param filters: Filters, e.g. "dataset__id=123&filename=file1.txt"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`DataFile` records.
        """
        url = "%s/api/v1/dataset_file/?format=json" % config.url
        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(DataFile, url, response.json())

    @staticmethod
    def get(**kwargs):
        r"""
        Retrieve a single datafile record

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the DataFile to retrieve

        :return: A :class:`DataFile` record.

        :raises requests.exceptions.HTTPError:
        """
        datafile_id = kwargs.get("id")
        if not datafile_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for DataFile get "
                "at this stage.")
        include_metadata = kwargs.get("include_metadata", False)
        url = "%s/api/v1/dataset_file/%s/?format=json" % \
            (config.url, datafile_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return DataFile(response.json(), include_metadata=include_metadata)

    @staticmethod
    def create(dataset_id, storagebox, dataset_path, path,
               check_local_paths=True, create_dataset_symlink=True):
        """
        Create one or more DataFile records, depending on whether the
        supplied path is a single file or a directory.

        :param dataset_id: The ID of the dataset to create the datafile
            record(s) in.
        :param storagebox: The storage box containing the datafile(s).
        :param dataset_path:
            The path to the directory which is to be mapped to a MyTardis
            dataset, meaning that files immediately inside this directory
            will have DataFile records created with the "directory" field
            set to "", and files within dataset_path/subdir1/ will have
            DataFile records creatd with the "directory" field set to "subdir1"
            etc.
            The MyTardis Client will create a symlink to dataset_path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file if the
            filesystem running mytardisclient is accessible to MyTardis,
            e.g. by SSHFS.
        :param path: The path to a file to be represented in the DataFile
            record or to a directory containing the files to create records
            for.  The subdirectory ('subdir1') to be
            recorded in the DataFile record(s) will be determined
            automatically by compareing the dataset_path with the path.
        """
        if not dataset_path:
            raise Exception("The dataset_path argument is required.")
        if check_local_paths and not os.path.exists(path):
            raise Exception("The path doesn't exist: %s" % path)
        if os.path.isdir(path):
            return DataFile.create_datafiles(dataset_id, storagebox,
                                             dataset_path, path)
        return DataFile.create_datafile(
            dataset_id, storagebox, dataset_path, path,
            check_local_paths=check_local_paths,
            create_dataset_symlink=create_dataset_symlink)

    @staticmethod
    def create_datafiles(dataset_id, storagebox, dataset_path, dir_path):
        """
        Create a DataFile record for each file within the dir_path directory.

        :param dataset_id: The ID of the dataset to create the datafile
            record(s) in.
        :param storagebox: The storage box containing the datafile(s).
        :param dataset_path:
            The path to the directory which is to be mapped to a MyTardis
            dataset, meaning that files immediately inside this directory
            will have DataFile records created with the "directory" field
            set to "", and files within dataset_path/subdir1/ will have
            DataFile records creatd with the "directory" field set to "subdir1"
            etc.
            The MyTardis Client will create a symlink to dataset_path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file if the
            filesystem running mytardisclient is accessible to MyTardis,
            e.g. by SSHFS.
        :param dir_path: The path to a directory containing file(s) to
            create DataFile records for.  If the dir_path is relative (not
            absolute) path, e.g. 'dataset1/subdir1', then the MyTardis Client
            will assume that the first component of the path (e.g. 'dataset1/')
            is the local dataset path, and create a symlink to this path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/
            which will enable MyTardis to verify and ingest its file(s).
            If dir_path is an absolute path, e.g.
            '/home/james/dataset1/subdir1/', then the dataset_path
            argument must be used to specified the dataset path, e.g.
            '/home/james/dataset1'.
        """
        num_datafiles_created = 0

        def log_error(err):
            """
            Log an error if os.listdir(...) fails during os.walk(...)
            """
            logger.error(str(err))

        for root, _, files in os.walk(dir_path, onerror=log_error):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    DataFile.create_datafile(dataset_id, storagebox,
                                             dataset_path, file_path,
                                             return_new_datafile=False)
                    num_datafiles_created += 1
                except DuplicateKey:
                    logger.warning("A DataFile record already exists for %s",
                                   file_path)
        return num_datafiles_created

    @staticmethod
    def create_datafile(dataset_id, storagebox, dataset_path, file_path,
                        return_new_datafile=True, check_local_paths=True,
                        create_dataset_symlink=True,
                        size=None, md5sum=None, mimetype=None):
        """
        Create a DataFile record.

        :param dataset_id: The ID of the dataset to create the datafile in.
        :param storagebox: The storage box containing the datafile.
        :param dataset_path:
            The path to the directory which is to be mapped to a MyTardis
            dataset, meaning that files immediately inside this directory
            will have DataFile records created with the "directory" field
            set to "", and files within dataset_path/subdir1/ will have
            DataFile records creatd with the "directory" field set to "subdir1"
            etc.
            The MyTardis Client will create a symlink to dataset_path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file if the
            filesystem running mytardisclient is accessible to MyTardis,
            e.g. by SSHFS.
        :param file_path: The local path to the file to be represented in
            the DataFile record.  The subdirectory ('subdir1') to be
            recorded in the DataFile record(s) will be determined
            automatically by compareing the dataset_path with the file_path.

        :return: A new :class:`DataFile` record.

        See also: :func:`mtclient.models.datafile.DataFile.upload`

        Suppose someone with username james generates a file called
        "results.dat" on a data analysis server called analyzer.example.com
        in the directory ~james/analysis/dataset1/.  User james could grant
        the MyTardis server temporary access to his account on
        analyzer.example.com and then have MyTardis copy the file(s) into
        a more permanent location.

        If james agrees to allow the MyTardis server to do so, it could
        SSHFS-mount james@analyzer.example.com:/home/james/analysis/,
        e.g. at /mnt/sshfs/james-anaylzer/

        Then user james doesn't need to upload results.dat, he just needs to
        tell MyTardis how to access it, and tell MyTardis that it is not yet
        in a permanent location.

        MyTardis's default storage box model generates datafile object
        identifiers which include a dataset description (e.g. 'dataset1')
        and a unique ID, resulting in path like 'dataset1-123/results.dat'
        for the datafile object.  Because user james doesn't want to have
        to create the 'dataset1-123' folder himself, he could entrust the
        MyTardis Client to do it for him.

        The MyTardis administrator can create a storage box for james called
        "james-analyzer" which is of type "receiving", meaning that it is a
        temporary location.  The storage box record (which only needs to be
        accessed by the MyTardis administrator) would include a StorageBoxOption
        with key 'location' and value '/mnt/sshfs/james-analyzer'.

        Once james knows the dataset ID of the dataset he wants to upload to
        (123 in this case), he can create a DataFile record as follows:

        mytardis datafile create 123 --storagebox=james-analyzer ~/analysis/dataset1/results.dat

        The file_path argument (set to ~/analysis/dataset1/results.dat)
        specifies the location of 'results.dat' on the analysis server.

        To enable the MyTardis server to access (and verify) the file via
        SSHFS / SFTP, a symbolic link can be created in
        ~james/.mytardisclient/servers/[mytardis_hostname]/, named "dataset1-123" pointing to
        the location of 'results.dat', i.e. ~james/analysis/dataset1/.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        from .dataset import Dataset

        if not dataset_path:
            raise Exception("The dataset_path argument is required.")
        if check_local_paths and not os.path.exists(file_path):
            raise Exception("Path doesn't exist: %s" % file_path)
        if check_local_paths and os.path.isdir(file_path):
            raise Exception("The path should be a single file: %s" % file_path)
        dataset = Dataset.objects.get(id=dataset_id)
        local_dataset_path = dataset_path
        file_path_without_dataset = os.path.relpath(file_path,
                                                    dataset_path)
        (directory, filename) = os.path.split(file_path_without_dataset)

        uri = os.path.join("%s-%s" % (dataset.description, dataset_id),
                           directory, filename)
        if create_dataset_symlink:
            dataset_symlink_path = \
                os.path.join(config.datasets_path,
                             "%s-%s" % (dataset.description, dataset_id))
            if not os.path.exists(dataset_symlink_path):
                print("Creating symlink to: %s in "
                      "~/.config/mytardisclient/servers/%s/ called %s"
                      % (local_dataset_path, config.hostname,
                         "%s-%s" % (dataset.description, dataset_id)))
                os.symlink(os.path.abspath(local_dataset_path),
                           os.path.join(config.datasets_path,
                                        "%s-%s" % (dataset.description,
                                                   dataset_id)))
        if DataFile.exists(dataset_id, directory, filename):
            if directory and directory != "":
                _file_path = os.path.join(directory, filename)
            else:
                _file_path = filename
            raise DuplicateKey("A DataFile record already exists for file "
                               "'%s' in dataset ID %s." % (_file_path,
                                                           dataset_id))
        if not size:
            size = str(os.stat(file_path).st_size)
        if not md5sum:
            md5sum = md5_sum(file_path)
        if not mimetype:
            mimetype = mimetypes.guess_type(file_path)[0]
        replicas = [{
            "url": uri,
            "location": storagebox,
            "protocol": "file",
            "verified": False
        }]
        new_datafile_json = {
            'dataset': "/api/v1/dataset/%s/" % dataset_id,
            'filename': filename,
            'directory': directory or "",
            'md5sum': md5sum,
            'size': size,
            'mimetype': mimetype,
            'replicas': replicas,
            'parameter_sets': []
        }
        url = "%s/api/v1/dataset_file/" % config.url
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_datafile_json))
        response.raise_for_status()
        logger.info("Created a DataFile record for %s", file_path)
        if return_new_datafile:
            datafile_id = response.headers['location'].split("/")[-2]
            new_datafile = DataFile.objects.get(id=datafile_id)
            return new_datafile
        return None

    @staticmethod
    def download(datafile_id, basedir=None, overwrite=False,
                 force_overwrite=False):
        """
        Download datafile with id datafile_id

        :param datafile_id: The ID of a datafile to download.
        :param basedir: If specified, the datafile will be downloaded to
                        the path obtained by joining basedir with the
                        DataFile's directory field.
        :param overwrite: If set to True, existing files will be re-downloaded
                          and overwritten without asking for confirmation if
                          their file size is wrong.
        :param force_overwrite: If set to True, existing files will be
                                re-downloaded and overwritten without asking
                                for confirmation, even if their file size is
                                correct.
        """
        from clint.textui import progress  # pylint: disable=import-error

        url = "%s/api/v1/dataset_file/%s/download/" \
            % (config.url, datafile_id)
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.apikey)}
        response = requests.get(url=url, headers=headers, stream=True)
        response.raise_for_status()
        datafile = DataFile.objects.get(id=datafile_id)
        try:
            _, params = cgi.parse_header(
                response.headers.get('Content-Disposition', ''))
            try:
                filename = params['filename']
            except KeyError:
                # If the download request is redirected to S3,
                # we may not have a filename header in the response,
                # so we can look up the datafile's filename instead:
                filename = datafile.filename
        except KeyError:
            print("response.headers: %s" % response.headers)
            raise
        filepath = filename
        if basedir:
            path = os.path.join(basedir, datafile.directory)
            if not os.path.exists(path):
                os.makedirs(path)
            filepath = os.path.join(path, datafile.filename)
        if os.path.exists(filepath) and not force_overwrite:
            if os.path.getsize(filepath) == datafile.size:
                logger.warning(
                    "Not re-downloading %s because its size is correct.",
                    filepath)
                return
            if not overwrite:
                from ..utils.confirmation import query_yes_no
                if not query_yes_no("Overwrite '%s'?" % filepath):
                    return
        with open(filepath, 'wb') as fileobj:
            total_length = int(response.headers.get('content-length'))
            # Hide progress bar for small files:
            if total_length < 10000000:  # 10 MB
                hide = True
            else:
                hide = None  # Leave it up to client.textui.progress
            chunk_size = 1000000
            for chunk in progress.bar(
                    response.iter_content(chunk_size=chunk_size),
                    hide=hide,
                    label="Downloading: %s " % filepath,
                    expected_size=(total_length / chunk_size) + 1):
                # filter out keep-alive new chunks:
                if chunk:
                    fileobj.write(chunk)
                    fileobj.flush()
            if hide:
                print("Downloaded: %s" % filepath)

    @staticmethod
    def upload(dataset_id, storagebox, dataset_path, file_path):
        """
        Upload datafile to dataset with ID dataset_id,
        using HTTP POST.

        :param dataset_id: The ID of the dataset to create the datafile in.
        :param dataset_path:
            The path to the directory which is to be mapped to a MyTardis
            dataset, meaning that files immediately inside this directory
            will have DataFile records created with the "directory" field
            set to "", and files within dataset_path/subdir1/ will have
            DataFile records creatd with the "directory" field set to "subdir1"
            etc.
            The MyTardis Client will create a symlink to dataset_path in
            ~/.config/mytardisclient/servers/[mytardis_hostname]/ which
            will enable MyTardis to verify and ingest the file if the
            filesystem running mytardisclient is accessible to MyTardis,
            e.g. by SSHFS.
        :param file_path: The local path to the file to be represented in
            the DataFile record.  If dataset_path is not specified,
            file_path must be a relative (not absolute) path, e.g.
            'dataset1/subdir1/datafile1.txt'.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        if not dataset_path:
            raise Exception("The dataset_path argument is required.")
        if not os.path.exists(file_path):
            raise Exception("Path doesn't exist: %s" % file_path)
        url = "%s/api/v1/dataset_file/" % config.url
        created_time = datetime.fromtimestamp(
            os.stat(file_path).st_ctime).isoformat()
        file_path_without_dataset = os.path.relpath(file_path,
                                                    dataset_path)
        directory, filename = os.path.split(file_path_without_dataset)
        if DataFile.exists(dataset_id, directory, filename):
            if directory and directory != "":
                _file_path = os.path.join(directory, filename)
            else:
                _file_path = filename
            raise DuplicateKey("A DataFile record already exists for file "
                               "'%s' in dataset ID %s." % (_file_path,
                                                           dataset_id))
        md5sum = md5_sum(file_path)
        file_data = {"dataset": "/api/v1/dataset/%s/" % dataset_id,
                     "filename": filename,
                     "directory": directory,
                     "md5sum": md5sum,
                     "size": str(os.stat(file_path).st_size),
                     "mimetype": mimetypes.guess_type(file_path)[0],
                     "created_time": created_time}
        if storagebox:
            file_data['replicas'] = [
                {
                    "url": "",
                    "protocol": "file",
                    "location": storagebox
                }
            ]
        file_obj = open(file_path, 'rb')
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.apikey)}
        response = requests.post(url, headers=headers,
                                 data={"json_data": json.dumps(file_data)},
                                 files={'attached_file': file_obj})
        file_obj.close()
        response.raise_for_status()
        if directory:
            print("Uploaded: %s/%s" % (directory, file_path))
        else:
            print("Uploaded: %s" % file_path)

    @staticmethod
    def update(datafile_id, md5sum):
        """
        Update a DataFile record.

        :param datafile_id: The ID of a datafile to be updated.
        :param md5sum: The new MD5 sum value.

        This method is not usable yet, because the MyTardis API doesn't yet
        allow update_detail to be performed on DataFile records.

        For a large file, its upload can commence before the local MD5 sum
        calculation is complete, i.e.  the DataFile record can be initially
        created with a bogus checksum which is later updated using this
        method.
        """
        updated_fields_json = {'md5sum': md5sum}
        url = "%s/api/v1/dataset_file/%s/" % \
            (config.url, datafile_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        response.raise_for_status()
        datafile_json = response.json()
        return DataFile(datafile_json)

    @staticmethod
    def verify(datafile_id):
        """
        Ask MyTardis to verify a datafile with id datafile_id

        :param datafile_id: The ID of a datafile to be verified.
        """
        url = "%s/api/v1/dataset_file/%s/verify/" \
            % (config.url, datafile_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        print("Requested verification of datafile ID %s." % datafile_id)

    @staticmethod
    def exists(dataset_id, directory, filename):
        """
        If MyTardis is running with DEBUG=False, then we won't
        be able detect duplicate key errors easily, we will just
        receive a generic HTTP 500 from the MyTardis API. This
        method checks whether a DataFile record already exists
        for the supplied dataset_id, directory and filename.

        :param dataset_id: The ID of the dataset to check existence in.
        :param directory: The directory within the dataset to check existence in.
        :param filename: The filename to check for existence.

        :return: True if a matching DataFile record already exists.
        """

        url = "%s/api/v1/dataset_file/?format=json" % config.url
        url += "&dataset__id=%s" % dataset_id
        url += "&filename=%s" % urllib.parse.quote(filename)
        if directory and directory != "":
            url += "&directory=%s" % urllib.parse.quote(directory)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code < 200 or response.status_code >= 300:
            raise Exception("Failed to check for existing file '%s' "
                            "in dataset ID %s." % (filename, dataset_id))
        return response.json()['meta']['total_count'] > 0


class DataFileParameterSet(object):
    """
    Model class for MyTardis API v1's DataFileParameterSetResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, response_dict):
        self.response_dict = response_dict
        self.id = response_dict['id']  # pylint: disable=invalid-name
        self.datafile = response_dict['datafile']
        self.schema = Schema(response_dict['schema'])
        self.parameters = []
        for datafile_param_json in response_dict['parameters']:
            self.parameters.append(DataFileParameter(datafile_param_json))

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of datafile parameter sets

        :param filters: Filters, e.g. "datafiles__id=12345"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`DatasetParameterSet` records,
            encapsulated in a `ResultSet` object`.
        """
        url = "%s/api/v1/datafileparameterset/?format=json" % config.url
        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(DataFileParameterSet, url, response.json())


class DataFileParameter(object):
    """
    Model class for MyTardis API v1's DataFileParameterResource.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, response_dict):
        self.response_dict = response_dict
        self.id = response_dict['id']  # pylint: disable=invalid-name
        pname_id = response_dict['name'].split('/')[-2]
        self.name = ParameterName.objects.get(id=pname_id)
        self.string_value = response_dict['string_value']
        self.numerical_value = response_dict['numerical_value']
        self.datetime_value = response_dict['datetime_value']
        self.link_id = response_dict['link_id']
        self.value = response_dict['value']

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        List datafile parameter records in parameter set.

        :param datafile_param_set: The datafile parameter set to
            list parameters for.
        """
