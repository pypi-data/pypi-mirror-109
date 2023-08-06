import os
import configparser


def parse_config(file_path: str):
    """
    Args:
        file_path: configuration path

    Returns:
        oss section
    """
    if not os.path.exists(file_path):
        raise ValueError(f"file not existed: {file_path}")
    config = configparser.ConfigParser()
    config.read(file_path)
    return config["oss"]
