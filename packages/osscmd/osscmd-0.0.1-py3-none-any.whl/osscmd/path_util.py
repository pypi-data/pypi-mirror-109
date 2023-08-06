"""
Path related utility
"""

from osscmd.log_util import default_logger as logger

OSS_SCHEME = "oss://"


def is_oss_path(path: str) -> bool:
    """Test whether it is a valid oss path"""
    return path.startswith(OSS_SCHEME)


def parse_oss_bucket(path: str):
    """parse an oss path
    Args:
        path: an oss path
    Returns:
        tuple(bucket, path without bucket)
    """
    if not path.startswith(OSS_SCHEME):
        raise ValueError(f"{path} not startswith with {OSS_SCHEME}")
    remain = path[len(OSS_SCHEME):]
    parts = remain.split("/")
    key = "/".join(parts[1:])
    logger.info(f"bucket: {parts[0]}, key: {key}")
    return parts[0], key
