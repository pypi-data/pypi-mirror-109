from argparse import Namespace

import requests
from owl_client.utils import get_auth


def get_pipedef(args: Namespace) -> None:
    """Get pipeline defition file

    Parameters
    ----------
    arg
        Argparse namespace containing command line flags.
    """
    schema = {True: "http", False: "https"}[args.insecure]
    headers = get_auth()

    url = "{}://{}/api/v1/pdef/get".format(schema, args.api)
    try:
        r = requests.get(url, params={"name": args.name}, headers=headers)
        res = r.json()
    except Exception as err:
        print("Failed to get pipeline definitions: %s" % err)

    if "error" in res:
        print("not found")
    else:
        print(res["config"])
