"""TestRail API binding for Python 3.x.

(API v2, available since TestRail 3.0)

Compatible with TestRail 3.0 and later.

Learn more:

http://docs.gurock.com/testrail-api2/start
http://docs.gurock.com/testrail-api2/accessing

Copyright Gurock Software GmbH. See license.md for details.
"""

import base64
import json

import requests


class APIClient:
    def __init__(self, base_url):
        self.user = ""
        self.password = ""
        if not base_url.endswith("/"):
            base_url += "/"
        self.__url = f"{base_url}index.php?/api/v2/"

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("GET", uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("POST", uri, data)

    def add_run(self, project_id, data):
        """Creates a new test run.

        Args:
            project_id: The ID of the project the test run should be added to
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded.

        Returns:
            A dict containing the result of the request.
        """
        return self.send_post(f"add_run/{str(project_id)}", data)

    def update_run(self, run_id, data):
        """Updates an existing test run (partial updates are supported, i.e. you can submit and update specific fields only).

        Args:
            run_id: The ID of the test run
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded.

        Returns:
            A dict containing the result of the request.
        """
        return self.send_post(f"update_run/{str(run_id)}", data)

    def close_run(self, run_id):
        """Closes an existing test run and archives its tests & results.

        Args:
            run_id: The ID of the test run to close

        Returns:
            A dict containing the result of the request.
        """
        return self.send_post(f"close_run/{str(run_id)}", {})

    def get_tests(self, run_id, filters=None):
        """Returns a list of tests for a test run.

        Args:
            run_id: The ID of the test run
            filters: Dict containing filters to apply to the request

        Returns:
            A dict containing the result of the request.
        """
        return self.send_get(f"get_tests/{str(run_id)}", filters)

    def add_results(self, run_id, data):
        """Adds one or more new test results, comments, or assigns one or more tests. Ideal for test automation to bulk-add multiple test results in one step.

        Args:
            run_id: The ID of the test run the results should be added to
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded.

        Returns:
            A dict containing the result of the request.
        """
        return self.send_post(f"add_results/{str(run_id)}", data)

    def delete_run(self, run_id, soft=0):
        """Deletes an existing test run.

        Args:
            run_id: The ID of the test run
            soft: If soft=1, this will return data on the number of affected tests.

        Returns:
            A dict containing the result of the request.
        """
        return self.send_post(f"delete_run/{str(run_id)}", data={"soft": 0})

    def get_user_by_email(self, email):
        """Returns an existing user by his/her email address.

        Args:
            email: The email address to get the user for

        Returns:
            A dict containing the user information or None if no user was found.
        """
        return self.send_get(f"get_user_by_email&email={email}")

    def get_user_id(self, email):
        """Returns an existing user by his/her email address.

        Args:
            email: The email address to get the user for
        """
        return int(self.send_get(f"get_user_by_email&email={email}")["id"])

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(bytes(f"{self.user}:{self.password}", "utf-8")),
            "ascii",
        ).strip()
        headers = {"Authorization": f"Basic {auth}"}

        if method == "POST":
            if uri[:14] == "add_attachment":  # add_attachment API method
                files = {"attachment": (open(data, "rb"))}
                response = requests.post(url, headers=headers, files=files)
                files["attachment"].close()
            else:
                headers["Content-Type"] = "application/json"
                payload = bytes(json.dumps(data), "utf-8")
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except Exception:
                error = str(response.content)
            raise APIError(
                f"TestRail API returned HTTP {response.status_code} ({error})"
            )
        else:
            if uri[:15] == "get_attachment/":  # Expecting file, not JSON
                try:
                    open(data, "wb").write(response.content)
                    return data
                except Exception:
                    return "Error saving attachment."
            else:
                try:
                    return response.json()
                except Exception:
                    return {}


class APIError(Exception):
    pass
