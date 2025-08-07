# ZoomInfo API Client

A minimal Python client for ZoomInfo's authentication and enterprise standard search API.

## Usage

```python
from zoominfo_api_client import ZoomInfoClient

client = ZoomInfoClient("username", "password")
client.authenticate()

# Search for contacts with explicit parameters
contacts = client.search_contacts(first_name="John", last_name="Doe")

# Search for companies with explicit parameters
companies = client.search_companies(
    company_name="OpenAI",
    industry_codes="7372",
    revenue_min=1000,
    revenue_max=5000,
)
```

## API

### `ZoomInfoClient`

`ZoomInfoClient(username, password, base_url='https://api.zoominfo.com', session=None)`

- `username` (`str`): ZoomInfo API username.
- `password` (`str`): ZoomInfo API password.
- `base_url` (`str`, optional): Base URL for the ZoomInfo API.
- `session` (`requests.Session`, optional): Existing session to use for requests.

### `authenticate()`

Authenticates with the API and returns a JWT token.

### `search_contacts(..., **extra_filters)`

Search for contacts using explicit keyword arguments that map to the fields
accepted by the ZoomInfo contact search API. Any additional unrecognized
arguments can be supplied via `extra_filters`.

### `search_companies(..., **extra_filters)`

Search for companies using explicit keyword arguments that map to the fields
accepted by the ZoomInfo company search API. Any additional unrecognized
arguments can be supplied via `extra_filters`.
