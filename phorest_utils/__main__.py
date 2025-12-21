"""Phorest Utilities accessing the Phorest API and doing various tasks."""

import importlib.metadata
import logging
import os
import sys
import time

import coloredlogs
import fire

from phorest_utils.fritzbox.phonebook_export import export_fritzbox_phonebook
from phorest_utils.phorest_api import phorest_api

coloredlogs.install()
log = logging.getLogger(__name__)


class PhorestUtils:
    """
    Phorest Utilities accessing the Porest API and doing various tasks.

    Phorest Utilities accessing the [Phorest API](https://developer.phorest.com/docs/getting-started) and doing various
    tasks like:

    - export_fritzbox_phonebook: Exporting the clients to a Fritzbox phonebook XML file.

    The help for each function can be accessed via the command line. For example:
      $ python -m phorest_api export_fritzbox_phonebook --help
    """

    def __init__(
        self, phorest_api_key=None, phorest_business_id=None, logging_level=logging.INFO
    ):
        """
        Initialize PhorestUtils with optional API key and business ID.

        Args:
          phorest_api_key (str, optional): The API key for authenticating with the Phorest API.
            This key is used to authorize requests to Phorest's services and can be obtained
            from your Phorest account settings. Defaults to the environment variable PHOREST_API_KEY.
          phorest_business_id (str, optional): The unique identifier for your Phorest business.
            This ID is used to specify which business account to interact with when making
            API requests. Defaults to the environment variable PHOREST_BUSINESS_ID.
          logging_level (int, optional): The logging level for debug output. Defaults to logging.INFO. See
            https://realpython.com/python-logging/ for details.
        """

        coloredlogs.install(level=logging_level)

        try:
            if not phorest_api_key:
                log.debug("Setting phorest_api_key from environment variable")
                phorest_api_key = os.environ["PHOREST_API_KEY"]
            if not phorest_business_id:
                log.debug("Setting phorest_business_id from environment variable")
                phorest_business_id = os.environ["PHOREST_BUSINESS_ID"]
        except KeyError as e:
            log.error(
                "Phorest API key or Business ID not set and not found in environment variables: %s", e
            )
            raise e

        self.phorest_api = phorest_api.PhorestAPI(phorest_api_key, phorest_business_id)

    def version(self):
        """
        Get the version of the phorest_utils package.

        Returns:
          str: The version string.
        """
        try:
            version = importlib.metadata.version("phorest_utils")
        except ImportError:
            log.error("Could not obtain version")
            sys.exit(1)
        return version

    def export_fritzbox_phonebook(
        self,
        output_filename=None,
    ):
        """
        Export the Phorest clients to a Fritzbox phonebook XML file.

        Args:
          output_filename (str, optional): The output filename for the Fritzbox phonebook XML file.
            Defaults to "export/<current_date>_fritzbox_phonebook.xml".
        """
        assert self.phorest_api is not None

        if not output_filename:
            output_filename = f"export/{time.strftime('%Y-%m-%d')}_fritzbox_phonebook.xml"

        clients = self.phorest_api.get_clients()
        export_fritzbox_phonebook(clients, output_filename=output_filename)


if __name__ == "__main__":
    fire.Fire(PhorestUtils, name="phorest_utils")
