# MCDR_uuid_api_remake
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

Refer to the original work.

**Note:** If your server has hybrid players (e.g., from skin stations, between premium and offline modes) or Bedrock Edition players, **no configuration changes are needed**. These players will use hashed pseudo-UUIDs.

> You do not need to worry about server authentication mode. The plugin auto-detects it.
>If using **BungeeCord** with premium verification enabled, or if actual UUIDs conflict with `online-mode` in `server.properties`,
> set the plugin's `manual_mode` to a boolean value to override the `server.properties` online mode.

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