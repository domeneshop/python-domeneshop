"""Domeneshop API client implementation."""

import json
import logging
from typing import List

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

API_BASE = "https://api.domeneshop.no/v0"

VALID_TYPES = [
    "A",
    "AAAA",
    "CNAME",
    "ANAME",
    "TLSA",
    "MX",
    "SRV",
    "DS",
    "CAA",
    "NS",
    "TXT",
]

COMMON_KEYS = {"host", "data", "ttl", "type"}

VALID_KEYS = {
    "MX": {"priority"},
    "SRV": {"priority", "weight", "port"},
    "TLSA": {"usage", "selector", "dtype"},
    "DS": {"tag", "alg", "digest"},
    "CAA": {"flags", "tag"},
}


class Client:
    def __init__(self, token: str, secret: str):
        """
        See the documentation at https://api.domeneshop.no/docs/ for
        help on how to acquire your API credentials.

        :param token: The API client token
        :type token: str
        :param secret: The API client secret
        :type secret: str

        """

        #: Doc comment for instance attribute qux.
        self._token = HTTPBasicAuth(token, secret)

    def get_domains(self) -> List[dict]:
        """
        Retrieve a list of all domains.

        :return: A list of domain dictionaries

        """
        resp = self._request("GET", "/domains")
        domains = resp.json()
        return domains

    def get_domain(self, domain_id: int) -> dict:
        """
        Retrieve a domain.
        
        :param domain_id: The domain ID to retrieve

        :return: A domain dictionary
        """

        resp = self._request("GET", "/domains/{0}".format(domain_id))
        domain = resp.json()
        return domain

    def get_records(self, domain_id: int) -> List[dict]:
        """
        Retrieve DNS records for a domain, or raises an error.
        
        :param domain_id: The domain ID to operate on

        :return: A list of record dictionaries
        """
        resp = self._request("GET", "/domains/{0}/dns".format(domain_id))
        records = resp.json()
        return records

    def get_record(self, domain_id: int, record_id: int) -> dict:
        """
        Retrieve a specific DNS record for a domain, or raises an error.
        
        :param domain_id: The domain ID to operate on
        :param record_id: The DNS record ID to retrieve

        :return: A record dictionary
        """
        resp = self._request("GET", "/domains/{0}/dns/{1}".format(domain_id, record_id))
        record = resp.json()
        return record

    def create_record(self, domain_id: int, record: int) -> int:
        """
        Create a DNS record for a domain, or raises an error. The record is validated
        primitively before being passed on to the API.
        
        :param domain_id: The domain ID to operate on
        :param record: A dict

        :return: The Record ID of the created record.

        Raises:
            TypeError: If the record appears to be invalid
        """
        _validate_record(record)
        resp = self._request("POST", "/domains/{0}/dns".format(domain_id), data=record)

        record_id = resp.headers.get("location").split("/")[-1]
        return int(record_id)

    def modify_record(self, domain_id: int, record_id: int, record: dict) -> None:
        """
        Modify a DNS record for a domain, or raises an error. The record is validated
        primitively before being passed on to the API.
        
        :param domain_id:  The domain ID to operate on
        :param record: A dict

        :return: A list of record dictionaries

        Raises:
            TypeError if the record appears to be invalid.
        """
        _validate_record(record)
        self._request(
            "PUT", "/domains/{0}/dns/{1}".format(domain_id, record_id), data=record
        )

    def delete_record(self, domain_id: int, record_id: int) -> None:
        """
        Delete a DNS record for a domain, or raises an error.
        
        :param domain_id:  The domain ID to operate on
        :param record_id: The record ID to delete
        """
        self._request("DELETE", "/domains/{0}/dns/{1}".format(domain_id, record_id))

    def _request(self, method="GET", endpoint="/", data=None, params=None):
        if not data:
            data = {}
        if not params:
            params = {}

        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        resp = requests.request(
            method,
            API_BASE + endpoint,
            data=json.dumps(data),
            params=params,
            headers=headers,
            auth=self._token,
        )
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                data = resp.json()
            except json.JSONDecodeError:
                data = {"error": resp.status_code, "help": "A server error occurred."}
            raise DomeneshopError(resp.status_code, data) from None
        else:
            return resp


class DomeneshopError(Exception):
    def __init__(self, status_code: int, error: dict):
        """
        Exception raised for API errors.

            :param status_code: The HTTP status code
            :type status_code: int
            :param error: The error returned from the API
            :type error: dict
        """
        self.status_code = status_code
        self.error_code = error.get("code")
        self.help = error.get("help")

        error_message = "{0} {1}. {2}".format(
            self.status_code, self.error_code, self.help
        )

        super().__init__(error_message)


def _validate_record(record):
    record_keys = set(record.keys())
    record_type = record.get("type")

    if record_type not in VALID_TYPES:
        raise TypeError("Record has invalid type. Valid types: {0}".format(VALID_TYPES))

    required_keys = COMMON_KEYS | VALID_KEYS.get(record_type, set())

    if record_keys != required_keys:
        raise TypeError(
            "Record is missing or has invalid keys. Required keys: {0}".format(
                required_keys
            )
        )
