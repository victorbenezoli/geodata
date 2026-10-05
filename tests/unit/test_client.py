"""Tests for the IBGE API client."""

import unittest
from unittest.mock import Mock, patch

from geodata.core.client import ApiVersion


class TestApiVersion(unittest.TestCase):
    def test_find_latest_version_with_and_without_version_query(self):
        response = Mock()
        response.text = (
            '<a class="headline" id="malhas" '
            'href="/api/docs/malhas?versao=4"></a>'
            '<a class="headline" id="localidades" '
            'href="/api/docs/localidades"></a>'
        )

        with patch("geodata.core.client.httpx.Client") as client_class:
            client_class.return_value.__enter__.return_value.get.return_value = response
            self.assertEqual(ApiVersion.find_latest_version("malhas").version, 4)
            localidades = ApiVersion.find_latest_version("localidades")

        self.assertEqual(localidades.version, 1)
        self.assertEqual(
            localidades.base_url,
            "https://servicodados.ibge.gov.br/api/v1/localidades",
        )
        self.assertEqual(response.raise_for_status.call_count, 2)

    def test_base_url_does_not_make_http_request(self):
        with patch("geodata.core.client.httpx.Client") as http_client:
            base_url = ApiVersion(name="malhas", version=4).base_url

        self.assertEqual(
            base_url,
            "https://servicodados.ibge.gov.br/api/v4/malhas",
        )
        http_client.assert_not_called()
