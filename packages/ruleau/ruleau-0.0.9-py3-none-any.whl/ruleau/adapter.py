import logging
from typing import Any, AnyStr, Dict, Optional
from urllib.parse import urljoin

import requests

from ruleau.decorators import api_request
from ruleau.exceptions import APIException
from ruleau.process import Process
from ruleau.rule import Rule

logger = logging.getLogger(__name__)


class ApiAdapter:

    base_url: AnyStr
    base_path: AnyStr
    api_key: Optional[AnyStr]

    def __init__(
        self,
        base_url: AnyStr,
        api_key: Optional[AnyStr] = None,
    ):
        """
        :param base_url: Base URL of the ruleau API
        :param api_key: (Optional) API key to authenticate with the API
        """
        self.base_url = base_url
        self.base_path = "/api/v1/"
        self.api_key = api_key

    @api_request
    def sync_case(self, case_id, process_id, payload) -> dict:
        """
        Synchronise case with API
        :param process_id:
        :param case_id:
        :param payload:
        :return:
        """
        response = requests.get(
            urljoin(self.base_url, f"{self.base_path}cases/{case_id}")
        )
        if response.status_code == 200:
            response = requests.patch(
                urljoin(self.base_url, f"{self.base_path}cases/{case_id}"),
                json={
                    "id": case_id,
                    "payload": payload,
                    "process": process_id,
                    "status": "OPEN",
                },
            )
            if response.status_code != 200:
                raise APIException(f"Failed to update case: {response.text}")
        else:
            response = requests.post(
                urljoin(self.base_url, f"{self.base_path}cases"),
                json={
                    "id": case_id,
                    "payload": payload,
                    "process": process_id,
                    "status": "OPEN",
                },
            )
            if response.status_code != 201:
                raise Exception(f"Failed to create case: {response.text}")

        return response.json()

    @api_request
    def sync_process(self, process: Process):
        # Check if the process exists
        url = urljoin(self.base_url, f"{self.base_path}processes/{process.id}")
        response = requests.get(url)
        # If the rule doesn't exist, create it
        if response.status_code == 404:
            response = requests.post(
                urljoin(self.base_url, f"{self.base_path}processes"),
                json=process.parse(),
            )

            if response.status_code != 201:
                raise Exception(f"Unable to save rules: {response.text}")
        return response.json()

    @api_request
    def create_result(
        self,
        case_id: AnyStr,
        rule: Rule,
    ) -> dict:
        """
        Update rule result after its execution
        :param case_id:
        :param rule:
        :return:
        """
        # Update the rule results
        response = requests.post(
            urljoin(
                self.base_url,
                f"{self.base_path}cases/{case_id}/rules/{rule.id}/results",
            )
        )
        if response.status_code != 201:
            raise Exception(
                f"Failed to create result {case_id}@{rule.id}: {response.text}"
            )
        return response.json()

    @api_request
    def update_result(
        self,
        case_id: AnyStr,
        rule: Rule,
        api_result: Dict[AnyStr, Any],
        execution_result: "ExecutionResult",  # noqa: F821
    ) -> dict:
        """
        Update rule result after its execution
        :param case_id:
        :param rule:
        :param api_result:
        :param execution_result:
        :return:
        """
        # Update the rule results
        response = requests.patch(
            urljoin(
                self.base_url,
                f"{self.base_path}cases/{case_id}/"
                f"rules/{rule.id}/results/{api_result['id']}",
            ),
            json={
                "result": execution_result.result,
                "payload": execution_result.payload.accessed,
                "override": execution_result.override,
                "original_result": execution_result.original_result,
            },
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to store rule result {case_id}@{rule.id}: {response.text}"
            )
        return response.json()

    @api_request
    def fetch_override(
        self, case_id: AnyStr, rule: Rule
    ) -> Optional[Dict[AnyStr, Any]]:
        """
        Fetch rule overrides
        :param rule:
        :param case_id: client ID that identifies a previously established case
        :return: a ruleau overrides Optional[Dict[AnyStr, Any]]
        """
        override = {}
        parsed_rule = rule.parse()
        response = requests.get(
            urljoin(
                self.base_url,
                f"{self.base_path}cases/{case_id}/overrides/search",
            ),
            params={"rule_name": parsed_rule["name"] or parsed_rule["function_name"]},
        )
        if response.status_code == 200:
            override = response.json()
        return override
