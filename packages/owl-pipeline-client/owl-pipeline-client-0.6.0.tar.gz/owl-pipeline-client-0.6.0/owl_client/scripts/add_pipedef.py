from argparse import Namespace

import requests
from owl_client.utils import read_config, get_auth


def add_pipedef(args: Namespace) -> None:
    """Add pipeline definition file.

    Parameters
    ----------
    arg
        Argparse namespace containing command line flags.
    """
    schema = {True: "http", False: "https"}[args.insecure]
    headers = get_auth()

    url = "{}://{}/api/v1/pdef/add".format(schema, args.api)
    pdef = [line for line in args.name.readlines()]
    config = read_config("".join(pdef))
    name = config["name"]
    data = {
        "name": name,
        "pdef": "".join(
            [line for line in pdef if not line.startswith("extra_pip_packages")]
        ),
        "extra_packages": config["extra_pip_packages"],
        "version": args.version,
    }

    try:
        r = requests.post(url, json=data, headers=headers)
        res = r.json()
    except Exception as err:
        print("Failed to add pipeline definition: %s" % err)

    if "ERROR" in res:
        print(res)
        return
    else:
        uid = res["uid"]
        print(f"Pipeline {name!r} added ({uid})")
