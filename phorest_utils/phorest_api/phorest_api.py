"""Phorest API access module."""
import logging
import re

import requests

log = logging.getLogger(__name__)

# pylint: disable=R0903

class PhorestAPI:
    """
    Phorest API access class.
    """

    def __init__(self, phorest_api_key, phorest_business_id):
        """
        Initialize PhorestAPI with optional API key and business ID.

        Args:
          phorest_api_key (str): The API key for authenticating with the Phorest API.
            This key is used to authorize requests to Phorest's services and can be obtained
            from your Phorest account settings.
          phorest_business_id (str): The unique identifier for your Phorest business.
            This ID is used to specify which business account to interact with when making
            API requests.
        """
        self.phorest_api_key = phorest_api_key
        self.phorest_business_id = phorest_business_id
        self.headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.phorest_api_key}",
        }

    def _fix_phone_numbers(self, clients):
        phone_types = ["mobile", "landLine"]
        for client in clients:
            for phone_type in phone_types:
                if phone_type in client and client[phone_type] is not None:
                    phone_number = re.sub("^49", "0", client[phone_type])
                    phone_number = re.sub("^0049", "0", phone_number)
                    client[phone_type] = phone_number

    def _add_unique_ids(self, clients):
        for idx, client in enumerate(clients):
            client["clientId"] = idx

    def get_clients(self):
        """
        Get all clients from the Phorest API.
        Returns:
          list: A list of clients.
        """
        num_clients = None
        clients = []
        page = 0
        total_pages = None
        clients_per_page = 100
        while page != total_pages:
            url = f"http://api-gateway-eu.phorest.com/third-party-api-server/api/business/{self.phorest_business_id}/client?size={clients_per_page}&page={page}"  # pylint: disable=line-too-long
            response = requests.get(url, headers=self.headers , timeout=10)
            data_dict = response.json()

            total_pages_ = data_dict["page"]["totalPages"]
            assert total_pages is None or total_pages == total_pages_
            total_pages = total_pages_

            num_clients_ = data_dict["page"]["totalElements"]
            assert num_clients is None or num_clients == num_clients_
            num_clients = num_clients_

            page += 1

            clients.extend(data_dict["_embedded"]["clients"])

        self._fix_phone_numbers(clients)
        self._add_unique_ids(clients)

        assert len(clients) == num_clients
        log.info("Total clients fetched: %s", len(clients))

        return clients
