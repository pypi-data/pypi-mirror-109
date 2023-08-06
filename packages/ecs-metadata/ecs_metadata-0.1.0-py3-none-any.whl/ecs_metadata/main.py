import functools
import itertools
import logging
import os

import requests


FIVE_SECONDS = 5.0


@functools.lru_cache
def fetch_container_metadata():
    metadata = {}
    url = os.getenv("ECS_CONTAINER_METADATA_URI_V4")

    if url is None:
        logging.warning(
            "Not on ECS. The environment variable "
            "'ECS_CONTAINER_METADATA_URI_V4' does not exist."
        )
    else:
        try:
            response = requests.get(url, timeout=(FIVE_SECONDS, FIVE_SECONDS))
            response.raise_for_status()
            metadata = response.json()
        except Exception as e:
            logging.error(
                "Failed to fetch container meta data, "
                f"because of exception: {e}."
            )
    return metadata


def extract_ips_from_metadata(metadata: dict):
    networks = metadata.get("Networks", [])
    network_ips = [network.get("IPv4Addresses", []) for network in networks]
    ips_generator = itertools.chain(*network_ips)
    return list(ips_generator)


def fetch_container_ips():
    metadata = fetch_container_metadata()
    return extract_ips_from_metadata(metadata)
