# -*- coding: utf-8 -*-

"""Top-level package for OctoParse Api Client."""
# -*- coding: utf-8 -*-

__author__ = """Robert Wendt"""
__email__ = "rob.w@conequip.com"
__version__ = "0.1.1"

import ssl
from typing import Dict, Optional, Union

import requests
from requests import Session
from urllib3 import poolmanager


class TLSAdapter(requests.adapters.HTTPAdapter):
    """
    Usage:

    >>> import requests
    >>> from octoparse_api_client import Client, TLSAdapter
    >>> session = requests.session()
    >>> session.mount("https://", TLSAdapter())
    >>> octo_client = Client(username="username", password="password", session=session)

    requests.exceptions.SSLError: HTTPSConnectionPool(host='dataapi.octoparse.com', port=443): Max retries exceeded with url: /token (Caused by SSLError(SSLError(1, '[SSL: WRONG_SIGNATURE_TYPE] wrong signature type (_ssl.c:1123)')))
    https://stackoverflow.com/questions/61631955/python-requests-ssl-error-during-requests
    """

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx,
        )


class Client:
    """
    Client for octoparse api http://dataapi.octoparse.com/

    Usage:

    create the client

    >>> import requests
    >>> from octoparse_api_client import Client, TLSAdapter
    >>> session = requests.session()
    >>> session.mount("https://", TLSAdapter())
    >>> octo_client = Client(username="username", password="password", session=session)

    get all task groups

    >>> groups = octo_client.list_task_groups()
    >>> group_ids = [data["taskGroupId"] for data in groups["data"]]

    get all task ids for every group id

    >>> all_task_ids = []
    >>> for gid in group_ids:
    >>>     tasks = octo_client.list_tasks_for_group(gid)
    >>>     task_ids = [data["taskId"] for data in tasks["data"]]
    >>>         for t in task_ids:
    >>>             all_task_ids.append(t)

    export task data from a task id

    TODO: What is the difference ``between export_task_data`` and ``get_all_data``?

    >>> for tid in all_task_ids:
    >>>     print(octo_client.export_task_data(tid))
    >>>     print(octo_client.get_all_data(tid))
    """

    _base_url = "https://dataapi.octoparse.com/"
    _token_url = _base_url + "token"
    _task_group_url = _base_url + "api/TaskGroup"
    _task_for_group_url = _base_url + "api/Task"
    _export_task_data_url = _base_url + "api/notexportdata/gettop"
    _get_all_data_url = _base_url + "api/alldata/GetDataOfTaskByOffset"
    _update_data_status_url = _base_url + "api/notexportdata/update"
    _clear_data_url = _base_url + "api/task/RemoveDataByTaskId"

    _token_data: Dict[str, Union[str, int]] = {}

    def __init__(self, username: str, password: str, session: Session = None):
        self.username = username
        self.password = password
        if session:
            self.session = session
        else:
            self.session = requests.session()

    def obtain_new_access_token(self):
        """
        obtains initial access token containing username and password, sets the
        initial token data.

        Example token data::
            {
                "access_token": "ABCD1234",      # Access permission
                "token_type": "bearer",          # Token type
                "expires_in": 86399,             # Access Token Expiration time (in seconds)(It is recommended to use the same token repeatedly within this time frame.)
                "refresh_token": "refresh_token" # To refresh Access Token
            }
        """
        post_fields = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }  # Set POST fields here
        r = self.session.post(self._token_url, data=post_fields)
        return r.json()

    def _refresh_token(self):
        """
        refresh and update access token data using the given refresh token

        Example token data::
            {
                "access_token": "ABCD1234",      # Access permission
                "token_type": "bearer",          # Token type
                "expires_in": 86399,             # Access Token Expiration time (in seconds)(It is recommended to use the same token repeatedly within this time frame.)
                "refresh_token": "refresh_token" # To refresh Access Token
            }
        """
        post_fields = {
            "refresh_token": self.token_data().get(
                "refresh_token", "Default string to prevent key errors"
            ),
            "grant_type": "refresh_token",
        }
        r = self.session.post(self._token_url, data=post_fields)
        return r.json()

    def token_data(self, refresh: bool = False):
        """
        Provide auth data for requests, refreshing token data if necessary.

        usage:

        configure client

        >>> import requests
        >>> from octoparse_api_client import Client, TLSAdapter
        >>> session = requests.session()
        >>> session.mount("https://", TLSAdapter())
        >>> octo_client = Client(username="********", password="********", session=session)

        get auth token data

        >>> token_data = octo_client.token_data()

        refresh auth token data
        >>> token_data_refreshed = octo_client.token_data(refresh=True)

        """
        if self._token_data == {}:
            # haven't logged in yet, do that and return token data
            self._token_data = self.obtain_new_access_token()
            return self._token_data
        elif refresh:
            # refresh stale token data and return it
            self._token_data = self._refresh_token()
            return self._token_data
        else:
            return self._token_data

    def auth_headers(self, refresh: bool = False) -> dict:
        """
        provide authentication header for requests
        """
        auth_token = self.token_data(refresh=refresh).get(
            "access_token", "Default string to prevent key errors"
        )
        return {"Authorization": f"bearer {auth_token}"}

    def _get(
        self,
        url: Union[bytes, str],
        headers: Optional[dict] = None,
        retries: int = 10,
        *args,
        **kwargs,
    ):
        """
        every get request by the client should route through here. provides
        exception handling for error states OctoParse sends us[1]. Currently
        only handles 401 for refreshing tokens.


        TODO: implement rate limiting according to their specifications[2].

        [1] http://dataapi.octoparse.com/help#_ref_status_code
        [2] http://dataapi.octoparse.com/help#_paths
        Octoparse limits API usage to 20 requests/second.
        Please reduce access frequency if you receive status code ‘429’.

        Note: Octoparse uses a leaky bucket algorithm to limit API access
        frequency. The maximum number of requests is 100 within any five-second
        time interval; no more requests will be taken thereafter until the next
        5-second time interval.




        """
        if headers is None:
            headers = {}
        headers = {**headers, **self.auth_headers()}
        for _ in range(retries - 1):
            result = self.session.get(url, headers=headers, **kwargs)

            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as e:  #
                # Invoke the code responsible for get a new token
                if e.response.status_code == 401:
                    headers = {**headers, **self.auth_headers(refresh=True)}

        result = self.session.get(
            url, headers=headers, **kwargs
        )  # once the token is refreshed, we can retry the operation
        result.raise_for_status()
        return result

    def list_task_groups(self):
        """
        List all task groups


        Example Response::
            {
                "data": [
                    {
                        "taskGroupId": 1,
                        "taskGroupName": "Example Task Group 1"
                    },
                    {
                        "taskGroupId": 2,
                        "taskGroupName": "Example Task Group 2"
                    }
                ],
                "error": "success",
                "error_Description": "Operation successes."
            }
        """

        return self._get(self._task_group_url).json()

    def list_tasks_for_group(self, group_id: int, *args, **kwargs):
        """
        list a all tasks for group

        Example Response::
            {
                "data": [
                    {
                        "taskId": "337fd7d7-aded-4081-9104-2b551161ccc8",
                        "taskName": "Example Task 1",
                        "creationUserId": "5d1e4b3c-645c-44ab-ac0e-bfa9ad600ece"
                    },
                    {
                        "taskId": "4adf489b-f883-43fa-b958-0cfde945ddb7",
                        "taskName": "Example Task 2",
                        "creationUserId": "5d1e4b3c-645c-44ab-ac0e-bfa9ad600ece"
                    }
                ],
                "error": "success",
                "error_Description": "Operation successes."
            }
        """
        params = {"taskGroupId": group_id}
        return self._get(self._task_for_group_url, params=params).json()

    def export_task_data(self, task_id: str, size: Optional[int] = None):
        """
        Example Response::
            {
                "data": {
                "total": 100000,
                "currentTotal": 4,
                "dataList": [
                        {
                            "state": "Texas",
                            "city": "Plano"
                        },
                        {
                            "state": "Texas",
                            "city": "Houston"
                        },
                        {
                            "state": "Texas",
                            "city": "Austin"
                        },
                        {
                            "state": "Texas",
                            "city": "Arlington"
                        }
                    ]
                },
                "error": "success",
                "error_Description": "Operation successes."
            }
        """
        if size is None:
            size = 10
        if size < 1 or size > 1000:
            raise Exception(
                "size needs to be between 1 & 1000"
            )  # TODO: named exception

        params = {"taskID": task_id, "size": size}
        return self._get(self._export_task_data_url, params=params).json()

    def get_all_data(
        self, task_id: str, size: Optional[int] = 10, offset: Optional[int] = 0
    ):
        """
        Example Response::
            {
                "data": {
                    "offset": 4,
                    "total": 100000,
                    "restTotal": 99996,
                    "dataList": [
                        {
                            "state": "Texas",
                            "city": "Plano"
                        },
                        {
                            "state": "Texas",
                            "city": "Houston"
                        },
                        {
                            "state": "Texas",
                            "city": "Austin"
                        },
                        {
                            "state": "Texas",
                            "city": "Arlington"
                        }
                    ]
                },
                "error": "success",
                "error_Description": "Operation successes."
            }
        """
        params = {"taskID": task_id, "size": size, "offset": offset}

        return self._get(self._get_all_data_url, params=params).json()

    def update_data_status(self, task_id: int):
        """
        This updates data status from ‘exporting’ to ‘exported’.

        http://dataapi.octoparse.com/help#_actions_NotExportDataSetExportingDataAsExported

        Example Response::
             {
                "error": "success",
                "error_Description": "Operation successes."
             }
        """
        params = {"taskID": task_id}
        return self.session.post(self._update_data_status_url, params=params).json()

    def clear_data(self, task_id: int):
        """
        http://dataapi.octoparse.com/help#_actions_TaskRemoveDataByTaskId

        Example Response::
             {
                "error": "success",
                "error_Description": "Operation successes."
             }
        """
        params = {"taskID": task_id}
        headers = self.auth_headers()
        r = self.session.post(self._clear_data_url, headers=headers, params=params)
        return r.json()
