import argparse

def add_bool_argument(parser, name, default, help):
    """Add a boolean argument"""
    parser.add_argument(
        name,
        nargs="?",
        const=not default,
        default=default,
        type=lambda x: x.lower() in ["true", "yes", "t", "y"],
        help=help,
    )



def create_parser():
    """Create parser for osscmd"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", help="configuration file")
    parser.add_argument("--id", help="access id")
    parser.add_argument("--key", help="access key")
    parser.add_argument("--endpoint", help="host of the oss storage")
    parser.add_argument("--ls", help="list the prefix")
    parser.add_argument("--rm", help="delete a file")
    parser.add_argument("--cp", help="copy file between local and oss", nargs=2)
    add_bool_argument(parser, "-r", False, "whether recursively execute")
    add_bool_argument(parser, "--d", False, "whether it is a directory")
    return parser
