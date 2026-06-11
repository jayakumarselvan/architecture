import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin, urlencode


def construct_url(host, port, base_path, path, query_params):
    # Construct the base URL
    base_url = f"{host}:{port}{base_path}/"
    # Join the base URL with the endpoint path
    url = urljoin(base_url, path)
    # Append query parameters
    url += "?" + urlencode(query_params)
    return url


def query_api(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: int = 10
):


    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            json=json,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

