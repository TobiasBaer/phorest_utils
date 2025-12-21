"""Module for exporting client phonebook data to FritzBox XML format."""
import logging
import os
import time

from jinja2 import Environment, FileSystemLoader

log = logging.getLogger(__name__)


def export_fritzbox_phonebook(clients, output_filename):
    """Exporting client phonebook data to FritzBox XML format.

    Args:
      clients (list): List of client dictionaries containing phonebook data.
      output_filename (str): The output filename for the Fritzbox phonebook XML file.
    """

    # Get the directory of the module
    directory = os.path.join(os.path.dirname(__file__), "jinja-templates/")
    log.info("Module directory: %s", directory)

    environment = Environment(loader=FileSystemLoader(directory))
    template = environment.get_template("fritzbox_xml_template.jinja")

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    unix_time = int(time.time())
    context = {"clients": clients, "unix_timestamp": unix_time}

    with open(output_filename, mode="w", encoding="utf-8") as results:
        results.write(template.render(context))
        log.info("Wrote %s", output_filename)
