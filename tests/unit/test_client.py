"""Tests for the IBGE API client."""

import unittest
import warnings
from unittest.mock import Mock, call, patch

from curl_cffi import requests

from geodata.core.client import ApiVersion


class TestApiVersion(unittest.TestCase):
    def test_find_latest_malhas_version_in_descending_order(self):
        valid_response = Mock()
        invalid_response = Mock()
        invalid_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("not found")
        )

        with patch("geodata.core.client.requests.Session") as session_class:
            session = session_class.return_value.__enter__.return_value
            session.get.side_effect = [invalid_response] * 16 + [valid_response]

            result = ApiVersion.find_latest_version("malhas")

        self.assertEqual(result, ApiVersion(name="malhas", version=4))
        session_class.assert_called_once_with(
            impersonate="chrome",
            debug=False,
        )
        self.assertEqual(
            session.get.call_args_list,
            [
                call(
                    "https://servicodados.ibge.gov.br/api/docs/"
                    f"malhas?versao={version}"
                )
                for version in range(20, 3, -1)
            ],
        )

    def test_find_latest_version_stops_at_first_valid_version(self):
        valid_response = Mock()

        with patch("geodata.core.client.requests.Session") as session_class:
            session = session_class.return_value.__enter__.return_value
            session.get.return_value = valid_response

            result = ApiVersion.find_latest_version("malhas")

        self.assertEqual(result.version, 20)
        session.get.assert_called_once_with(
            "https://servicodados.ibge.gov.br/api/docs/malhas?versao=20"
        )

    def test_localidades_uses_version_one_without_request(self):
        with patch("geodata.core.client.requests.Session") as session_class:
            result = ApiVersion.find_latest_version("localidades")

        self.assertEqual(result, ApiVersion(name="localidades", version=1))
        session_class.assert_not_called()

    def test_network_errors_do_not_interrupt_version_search(self):
        valid_response = Mock()

        with patch("geodata.core.client.requests.Session") as session_class:
            session = session_class.return_value.__enter__.return_value
            session.get.side_effect = [
                requests.exceptions.ConnectionError("network error"),
                valid_response,
            ]

            result = ApiVersion.find_latest_version("malhas")

        self.assertEqual(result.version, 19)
        self.assertEqual(
            session.get.call_args_list,
            [
                call(
                    "https://servicodados.ibge.gov.br/api/docs/"
                    "malhas?versao=20"
                ),
                call(
                    "https://servicodados.ibge.gov.br/api/docs/"
                    "malhas?versao=19"
                ),
            ],
        )

    def test_find_latest_version_does_not_emit_warnings(self):
        valid_response = Mock()

        def get_with_warning(*args, **kwargs):
            warnings.warn("diagnostic warning", UserWarning)
            return valid_response

        with patch("geodata.core.client.requests.Session") as session_class:
            session = session_class.return_value.__enter__.return_value
            session.get.side_effect = get_with_warning

            with warnings.catch_warnings(record=True) as emitted_warnings:
                warnings.simplefilter("always")
                result = ApiVersion.find_latest_version("malhas")

        self.assertEqual(result.version, 20)
        self.assertEqual(emitted_warnings, [])

    def test_raises_runtime_error_when_no_version_is_valid(self):
        invalid_response = Mock()
        invalid_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("not found")
        )

        with patch("geodata.core.client.requests.Session") as session_class:
            session = session_class.return_value.__enter__.return_value
            session.get.return_value = invalid_response

            with self.assertRaises(RuntimeError):
                ApiVersion.find_latest_version("malhas")

        self.assertEqual(session.get.call_count, 20)

    def test_base_url_does_not_make_http_request(self):
        with patch("geodata.core.client.requests.Session") as session_class:
            base_url = ApiVersion(name="malhas", version=4).base_url

        self.assertEqual(
            base_url,
            "https://servicodados.ibge.gov.br/api/v4/malhas",
        )
        session_class.assert_not_called()
