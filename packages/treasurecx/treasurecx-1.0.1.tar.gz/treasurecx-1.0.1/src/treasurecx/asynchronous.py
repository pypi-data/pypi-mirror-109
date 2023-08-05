"""
Asynchronous wrapper for `treasure.cx`.

Example usage:
```
import treasurecx.asynchronous
account_types = await treasurecx.asynchronous.account_types() # Get account types
print(account_types)
account = await treasurecx.treasure_async.generate(type=1) # Generate a Minecraft account
print(account) # {'status': '...', 'message': '...'}
"""
import json
import aiohttp

async def account_types(source: str = "API"):
    """
    Return a list of account types.

    Arguments:
    `[source]`: The app/website from which the user generated a link (e.g. Discord) || "API" by default
    """
    async with aiohttp.ClientSession() as _http:
        async with _http.get("https://treasure.cx/api/types?src=" + source) as resp:
            return (await resp.text())

async def generate(type_: int = 1, source: str = "API") -> dict:
    """
    Generate an account with the provided type.

    Arguments:
    `[type_]`: Type of account you want to generate (int) || 1 (Minecraft) by default
    `[source]`: The app/website from which the user generated a link (e.g. Discord) || "API" by default

    Account types can be fetched using `treasurecx.treasurecx.account_types()`.
    """
    valid_types = json.loads(await account_types())
    invalid_msg = ValueError("Invalid account type. Account types can be fetched using `treasurecx.async.account_types()`.")
    try:
        type_ = int(type_)
    except ValueError:
        raise invalid_msg
    if str(type_) not in valid_types:
        raise invalid_msg
    async with aiohttp.ClientSession() as _http:
        async with _http.get("https://treasure.cx/api/generate?type=" + str(type_) + "&src=" + str(source)) as resp:
            return (await resp.text())
