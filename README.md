# python-nats-pipeline-rest-gateway
Status: Pre/Alpha / Exploratory

## Overview
Sample REST gateway implemented using python and NATS.

**An example gateway to:**

1. Receive REST requests.
2. Submit to message queue.
3. Pipeline stage Validates message.
4. If valid passes message onto second message queue.
5. If invalid post invalid message onto invalid message queue.
6. Gateway listens for response and returns to caller.

## Example scenario:

A scalable service to produce betting prices for a football game based on expected goals for both teams.
The model will be a 'naive' poisson based statistical one with prices being derived from SciPy calculated
correct score grid.

Input POST /football
``` json
{
    "game_id": UID, 
    "home_expected": Float, 
    "away_expected": Float
}
```

Return (Valid)
``` json
{
    "game_id": UID, 
    "home_towin": Float, 
    "away_towin": Float,
    "draw": Float
}
Code: 200 - OK
```

Return (Invalid)
``` json
{
    "game_id": UID, 
    "error": String
}
Code: 400 - Bad Request
```

## Notes

* aiohttp will be used as the async http library.
* schematics will be used to define models and validate incoming messages.
* json will be used as the message format.
* SciPy / Numpy will be used to 'do the math'.

## Setup (Dependencies)
``` bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install aiohttp
pip install cchardet
pip install aiodns
pip install numpy
pip install scipy
pip install schematics
```

## Testing

``` bash 
# To post to the running gateway

# Valid sample post
curl --data '{"game_id": "qwertyui", "home_expected": 0.1, "away_expected": 1}'  http://localhost:8080/football

# InValid sample post
curl --data '{"game_id": "qwertyui", "home_expected": "0.1", "away_expected": -1}'  http://localhost:8080/football

```
## Refs: 
* https://github.com/aio-libs/aiohttp
* https://www.roguelynn.com/words/asyncio-we-did-it-wrong/
* https://www.pinnacle.com/en/betting-articles/Soccer/how-to-calculate-poisson-distribution/MD62MLXUMKMXZ6A8