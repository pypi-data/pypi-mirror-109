from osscmd.args import create_parser
from osscmd.conf import parse_config
from osscmd.log_util import default_logger as logger
from osscmd.oss_ops import OssOps
from osscmd import path_util


def execute_command(oss_ops: OssOps, args):
    """Execute related commands"""
    command_list = [args.ls, args.rm, args.cp]
    valid = [cmd is not None for cmd in command_list]
    if len(list(filter(lambda x: x, valid))) > 1:
        raise RuntimeError("You provide two commands")
    if args.ls:
        oss_ops.list(args.ls)
    if args.rm:
        oss_ops.delete(args.rm, is_directory=args.r)
    if args.cp:
        all_oss = [path_util.is_oss_path(p) for p in args.cp]
        if all(all_oss):
            raise ValueError("Not allowed to operate between oss paths")
        if all_oss[0]:
            oss_ops.download(args.cp[0], args.cp[1], is_directory=args.r)
        else:
            oss_ops.upload(args.cp[0], args.cp[1], is_directory=args.r)


def main():
    parser = create_parser()
    args, _ = parser.parse_known_args()
    if args.conf is not None:
        oss_conf = parse_config(args.conf)
        args.id = args.id or oss_conf["id"]
        args.key = args.key or oss_conf["key"]
        args.endpoint = args.endpoint or oss_conf["endpoint"]
    oss_ops = OssOps(args)
    execute_command(oss_ops, args)
