"""
Synchronous wrapper for `treasure.cx`.

Example usage:
```
import treasurecx
account_types = treasurecx.account_types() # Get account types
print(account_types)
account = treasurecx.generate(type=1) # Generate a Minecraft account
print(account) # {'status': '...', 'message': '...'}
"""
import json
import http.client as _http

_http = _http.HTTPSConnection('treasure.cx')

def account_types(source: str = "API"):
    """
    Return a list of account types.

    Arguments:
    `[source]`: The app/website from which the user generated a link (e.g. Discord) || "API" by default
    """
    _http.request("GET", "/api/types?src=" + source)
    resp = _http.getresponse()
    data = json.loads(resp.read().decode())
    return data

def generate(type_: int = 1, source: str = "API") -> dict:
    """
    Generate an account with the provided type.

    Arguments:
    `[type_]`: Type of account you want to generate (int) || 1 (Minecraft) by default
    `[source]`: The app/website from which the user generated a link (e.g. Discord) || "API" by default

    Account types can be fetched using `treasurecx.treasurecx.account_types()`.
    """
    valid_types = account_types()
    invalid_msg = ValueError("Invalid account type. Account types can be fetched using `treasurecx.treasurecx.account_types()`.")
    try:
        type_ = int(type_)
    except ValueError:
        raise invalid_msg
    if str(type_) not in valid_types:
        raise invalid_msg
    _http.request("GET", "/api/generate?type=" + str(type_) + "&src=" + str(source))
    resp = _http.getresponse()
    data = json.loads(resp.read().decode())
    return data