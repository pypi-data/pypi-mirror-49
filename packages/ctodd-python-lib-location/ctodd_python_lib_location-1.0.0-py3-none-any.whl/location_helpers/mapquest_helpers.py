"""
    Purpose:
        Mapquest Helpers

        This library is used to wrap mapquest API calls and handle authentication
"""

# Python Library Imports
import logging
import os
import re
import requests


###
# Properties
###


mapquest_api_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "http://www.mapquestapi.com/",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}


###
# Mapquest Helpers
###


def get_mapquest_api_key(public_key_file="~/.mapquest/public_key.txt"):
    """
    Purpose:
        Get the mapquest API from the environment
    Args:
        public_key_file (String): filename of the public key token file
    Return:
        mapquest_api_key (String): MapQuest public key
    """

    public_key_file = os.path.expanduser(public_key_file)

    try:
        with open(public_key_file, "r") as public_key_file_obj:
            mapquest_api_key = public_key_file_obj.read().strip("\n")
    except Exception as err:
        raise Exception(f"Failed to Get Public Key for Mapquest: {public_key_file}")

    return mapquest_api_key


def get_directions_between_two_addresses(mapquest_api_key, address_1, address_2):
    """
    Purpose:
        Get directions between two addresses

        Leverages Mapquest API:
            https://developer.mapquest.com/documentation/directions-api/route/get/
    Args:
        address_1 (String): Address to use as start point of travel
        address_2 (String): Address to use as end destination of travel
    Return:
        directions (Dict): Dict of the directions between the two locations
    """

    mapquest_direcions_url = (
        f"http://www.mapquestapi.com/directions/v2/route?key={mapquest_api_key}"
        f"&from={address_1}&to={address_2}"
    )

    logging.info(f"Fetching Directions: {mapquest_direcions_url}")
    mapquest_direcions_response = requests.get(
        mapquest_direcions_url, headers=mapquest_api_headers
    )

    if mapquest_direcions_response.status_code == 200:
        raw_mapquest_direcions = mapquest_direcions_response.json()
    else:
        logging.error(
            "Got Failure Response from Indeed.com: "
            f"{mapquest_direcions_response.status_code}"
        )
        raw_mapquest_direcions = {}

    return raw_mapquest_direcions
