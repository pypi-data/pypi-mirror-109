from argparse import Namespace

import requests
from owl_client.utils import read_config, get_auth


success_msg = """
Job ID %d submitted.
"""


def submit_pipeline(args: Namespace) -> None:
    """Add pipeline to queue.

    Parameters
    ----------
    arg
        Argparse namespace containing command line flags.
    """
    conf = read_config(args.conf)
    schema = {True: "http", False: "https"}[args.insecure]
    headers = get_auth()
    url = "{}://{}/api/v1/pipeline/add".format(schema, args.api)
    data = {"config": conf}

    try:
        r = requests.post(url, json=data, headers=headers)
        job_id = int(r.text)
        print(success_msg % job_id)
    except ValueError as err:
        print("Failed to submit pipeline. Authentication failed. %s " % err)
    except Exception as err:
        print("Failed to submit pipeline: %s" % err)
