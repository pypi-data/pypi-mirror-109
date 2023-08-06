"""
OSS bucket related operations
"""

import os
import oss2

from osscmd import path_util
from osscmd.log_util import default_logger as logger


class OssOps:

    def __init__(self, parsed_args):
        """
        Args:
            parsed_args: parsed arguments from sys.argv
        """
        if not all([parsed_args.id, parsed_args.key, parsed_args.endpoint]):
            raise RuntimeError("No valid credential provided through conf or cli")
        self._auth = oss2.Auth(parsed_args.id, parsed_args.key)
        self._endpoint = parsed_args.endpoint
        self._bucket = None

    def create_bucket(self, path: str):
        """Create a valid bucket with path"""
        if self._bucket is None:
            bucket_name, _ = path_util.parse_oss_bucket(path)
            self._bucket = oss2.Bucket(self._auth, self._endpoint, bucket_name)
        return self._bucket

    def upload(self, src: str, dst: str, is_directory=False):
        """Upload src to dst
        Args:
            src: source path
            dst: destination path
            is_directory: whether it is a directory
        """
        self.create_bucket(dst)
        if is_directory:
            contents = os.listdir(src)
            for file in contents:
                path = os.path.join(src, file)
                target = os.path.join(dst, file)
                logger.info(f"Upload {path} to {target}", path, target)
                _, target = path_util.parse_oss_bucket(target)
                self._bucket.put_object_from_file(target, path)
        else:
            logger.info(f"Upload {src} to {dst}")
            _, key = path_util.parse_oss_bucket(dst)
            self._bucket.put_object_from_file(key, src)

    def get_list_result(self, path, with_size=False):
        self.create_bucket(path)
        _, key = path_util.parse_oss_bucket(path)
        logger.info(f"List key: {key}")
        result = self._bucket.list_objects(key)
        object_list = result.object_list
        result = []
        for content in object_list:
            # content.is_prefix() does not return the correct result
            if not content.key.endswith("/"):
                if with_size:
                    result.append((content.key, content.size))
        return result

    def list(self, path: str):
        result = self.get_list_result(path, with_size=True)
        if not result:
            logger.info(f"No file found with prefix: {path}")

        def human_size(byte):
            if byte < 1024:
                return f"{byte} B"
            elif byte > 1024 and byte < 1024 * 1024:
                return f"{byte/1024.0:.2f} KB"
            elif byte > 1024 * 1024 and byte < 1024 * 1024 * 1024:
                return f"{byte/1024.0/1024:.2f} MB"
            else:
                return f"{byte/1024.0/1024/1024:.2f} GB"
        for content in result:
            logger.info(f"List result: {content[0]} {human_size(content[1])}")

    def download(self, src, dst, is_directory=False):
        """Download a file or directory from oss"""
        self.create_bucket(src)
        if is_directory:
            if not os.path.exists(dst):
                os.makedirs(dst)
            logger.info("Only download 100 files now")
            result = self.get_list_result(src)
            for key in result:
                name = os.path.basename(key)
                target = os.path.join(dst, name)
                logger.info(f"Download file {key} to {target}")
                self._bucket.get_object_to_file(key, target)
        else:
            _, key = path_util.parse_oss_bucket(src)
            logger.info(f"Downloading file from {src} to {dst}")
            self._bucket.get_object_to_file(key, dst)

    def delete(self, src, is_directory=False):
        """Delete files from oss whether it is a file or directory"""
        self.create_bucket(src)
        if is_directory:
            max_keys = 100
            result = self.get_list_result(src)
            for key in result:
                logger.info(f"Delete file: {key}")
                self._bucket.delete_object(key)
        else:
            _, key = path_util.parse_oss_bucket(src)
            logger.info(f"Delete objects: {key}")
            self._bucket.delete_object(key)
