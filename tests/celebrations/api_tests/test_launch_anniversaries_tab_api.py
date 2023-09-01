import requests
import pytest


def make_request(url, headers, payload):
    try:
        response = requests.get(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


@pytest.mark.performance
def test_request_performance(benchmark):
    url = "https://i18napi-perf-prd.alamoapp.octanner.io/5464be5f-b704-44c7-907f-8cf6103d3f84/ccyearbook"
    payload = {}
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "cache-control": "no-cache",
        "origin": "https://cc-qa.culturecloud.com",
        "pragma": "no-cache",
        "referer": "https://cc-qa.culturecloud.com/",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    # Use the benchmark fixture to measure the time it takes to make the request
    result = benchmark(make_request, url, headers, payload)
    assert result is not None, "Request failed"


## Run  pytest -v --benchmark-enable
