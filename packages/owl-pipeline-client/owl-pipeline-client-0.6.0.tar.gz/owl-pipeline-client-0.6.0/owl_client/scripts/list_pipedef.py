from argparse import Namespace

import requests

from owl_client.utils import get_auth


def list_pipedef(args: Namespace) -> None:
    """List pipeline definitions in the server.

    Parameters
    ----------
    arg
        Argparse namespace containing command line flags.
    """
    schema = {True: "http", False: "https"}[args.insecure]
    headers = get_auth()

    url = "{}://{}/api/v1/pdef/list".format(schema, args.api)
    try:
        res = requests.get(url, headers=headers)
        res_json = res.json()
    except Exception as err:
        print("Failed to get pipeline definitions: %s" % err)

    print(
        "{name:20s} {version:12s} {packages}".format(
            name="Name", version="Version", packages="Packages"
        )
    )
    for r in res_json.values():  # type: dict
        print("{name:20s} {version:12s} {packages}".format(**r))
