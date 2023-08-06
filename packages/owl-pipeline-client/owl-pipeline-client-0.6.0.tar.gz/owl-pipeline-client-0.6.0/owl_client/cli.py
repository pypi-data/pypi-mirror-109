import logging
import logging.config
import os
import sys
from argparse import ArgumentParser, FileType, Namespace
from typing import List

from owl_client.scripts import (
    cancel_pipeline,
    login_api,
    logs_pipeline,
    run_standalone,
    status_pipeline,
    submit_pipeline,
    add_pipedef,
    list_pipedef,
    get_pipedef,
)

log = logging.getLogger(__name__)

OWL_API_URL = os.environ.get("OWL_API_URL", "imaxt.ast.cam.ac.uk")


def parse_args(input: List[str]) -> Namespace:
    """Parse command line arguments.

    Parameters
    ----------
    input
        list of command line arguments

    Returns
    -------
    parsed arguments
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    # Login
    login = subparsers.add_parser("login")
    login.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    login.add_argument("--insecure", action="store_true")
    login.set_defaults(func=login_api)

    # Submit
    submit = subparsers.add_parser("submit")
    submit.add_argument("conf", type=FileType("r"))
    submit.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    submit.add_argument("--insecure", action="store_true")
    submit.set_defaults(func=submit_pipeline)

    # Execute
    execute = subparsers.add_parser("execute")
    execute.add_argument("conf", type=FileType("r"))
    execute.add_argument("--debug", action="store_true")
    execute.set_defaults(func=run_standalone)

    # Cancel
    cancel = subparsers.add_parser("cancel")
    cancel.add_argument("jobid")
    cancel.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    cancel.add_argument("--insecure", action="store_true")
    cancel.set_defaults(func=cancel_pipeline)

    # Status
    status = subparsers.add_parser("status")
    status.add_argument("jobid")
    status.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    status.add_argument("--insecure", action="store_true")
    status.set_defaults(func=status_pipeline)

    # Logs
    logs = subparsers.add_parser("logs")
    logs.add_argument("jobid")
    logs.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    logs.add_argument("--insecure", action="store_true")
    logs.set_defaults(func=logs_pipeline)

    # PDeF
    pdef = subparsers.add_parser("pdef")
    subparsers_pdef = pdef.add_subparsers()
    pdef_add = subparsers_pdef.add_parser("add")
    pdef_add.add_argument("name", type=FileType("r"))
    pdef_add.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    pdef_add.add_argument("--insecure", action="store_true")
    pdef_add.add_argument("--version", required=False, type=str, default="0.1.0")
    pdef_add.set_defaults(func=add_pipedef)

    pdef_list = subparsers_pdef.add_parser("list")
    pdef_list.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    pdef_list.add_argument("--insecure", action="store_true")
    pdef_list.set_defaults(func=list_pipedef)

    pdef_get = subparsers_pdef.add_parser("get")
    pdef_get.add_argument("name")
    pdef_get.add_argument("--api", required=False, type=str, default=OWL_API_URL)
    pdef_get.add_argument("--insecure", action="store_true")
    pdef_get.set_defaults(func=get_pipedef)

    args = parser.parse_args(input)
    if not hasattr(args, "func"):
        parser.print_help()

    return args


def main():
    """Main entry point for owl.

    Invoke the command line help with::

        $ owl --help

    """
    args = parse_args(sys.argv[1:])

    if hasattr(args, "func"):
        args.func(args)
