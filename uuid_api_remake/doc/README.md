# UUID API REMAKE
This plugin is a remade version of the UUID API. [Original UUID API link: https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api](https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/uuid_api)

This plugin utilizes all code from the original API for obtaining UUIDs in **premium/offline** servers.

### Additional Features in the Remake:

1. Added more commands for easier UUID management.
2. All obtained UUIDs are stored and centrally managed in the `uuid.json` data file.
3. Added the `get_name(uuid)` function to retrieve player names from UUIDs (sourced from `uuid.json` and `usercache.json`).

### UUID Retrieval Workflow (proceeds to next step if failed):

1. Read the plugin data file `uuid.json`.
2. Read `usercache.json`. If successful, store results in `uuid.json`.
3. Call the original API. If successful, store results in `uuid.json`.
4. Generate a pseudo-UUID using the SHA-256 hash of `playername + timestamp`, take the first 50 bits, and store it in `uuid.json`.

### Configuration

```json
{
    "mojang_online_mode": true,
    "online_api": "https://api.mojang.com/users/profiles/minecraft/",
    "use_offline_api": true,
    "offline_api": "http://tools.glowingmines.eu/convertor/nick/"
}
```
**mojang_online_mode**: Indicates whether the server is an official (authenticated) server. When set to true, it uses the official Mojang API to obtain UUIDs

**online_api**: The endpoint URL for the official authentication API. Defaults to `https://api.mojang.com/users/profiles/minecraft/`  

**use_offline_api**: Determines whether to use offline API for UUID retrieval. This setting becomes active only when mojang_online_mode is set to false. Defaults to true

**offline_api**: Offline API URL, defaults to `http://tools.glowingmines.eu/convertor/nick/`  

**Note**: Ensure these four configuration items remain complete in the file. If using custom APIs, please remember to include the trailing `/`

### Commands

Except for `!!uar` and `!!uar help`, all other commands can only be used in the **console**.

For detailed usage, run `!!uar` or `!!uar help`.

### API Usage

**Obtain UUID from player name:**

```python
import uuid_api_remake

name = ... # str
uuid = uuid_api_remake.get_uuid(name)
print(uuid)
```

**Obtain player name from UUID (sourced from `uuid.json` and `usercache.json`):**

```python
import uuid_api_remake

uuid = ... # str
name = uuid_api_remake.get_name(uuid)
print(name)
```