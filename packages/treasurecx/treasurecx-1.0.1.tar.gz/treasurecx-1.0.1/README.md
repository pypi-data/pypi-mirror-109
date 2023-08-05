# treasurecx
## Advanced Python wrapper for "treasure.cx".  

### Synchronous Usage
```py
import treasurecx
account_types = treasurecx.account_types() # Get account types
print(account_types)
account = treasurecx.generate(type=1) # Generate a Minecraft account
print(account) # {'status': '...', 'message': '...'}
```

### Asynchronous Usage
```py
import treasurecx.asynchronous
account_types = await treasurecx.asynchronous.account_types() # Get account types
print(account_types)
account = await treasurecx.treasure_async.generate(type=1) # Generate a Minecraft account
print(account) # {'status': '...', 'message': '...'}
```

# Synchronous Commands
## account_types
`treasurecx.account_types(source="API")`

Return a list of account types.

Arguments:  
`[source]`: The app/website from which the user generated a link (e.g. Discord) ***||*** "API" by default

## generate
`treasurecx.generate(type_=1, source="API")`

Generate an account with the provided type.


Arguments:
`[type_]`: Type of account you want to generate (int) || 1 (Minecraft) by default

`[source]`: The app/website from which the user generated a link (e.g. Discord) ***||*** "API" by default


Account types can be fetched using `treasurecx.treasurecx.account_types()`.

# Asynchronous Commands
## account_types
`await treasurecx.account_types(source="API")`

Return a list of account types.

Arguments:  
`[source]`: The app/website from which the user generated a link (e.g. Discord) ***||*** "API" by default

## generate
`await treasurecx.generate(type_=1, source="API")`

Generate an account with the provided type.


Arguments:
`[type_]`: Type of account you want to generate (int) || 1 (Minecraft) by default

`[source]`: The app/website from which the user generated a link (e.g. Discord) ***||*** "API" by default


Account types can be fetched using `treasurecx.treasurecx.account_types()`.
