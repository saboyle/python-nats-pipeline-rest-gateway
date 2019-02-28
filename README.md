# python-nats-pipeline-rest-gateway
Status: Pre/Alpha / Exploratory

## Overview
Sample REST gateway implemented using python and NATS.

The service will be implemented in three forms (basic, basic-distributed and gateway)

**Basic functionality:**

1. Receive REST requests.
2. Validate the request (using the schematic library).
2. If valid perform a calculation and return the result.
3. If invalid return invalid json message to caller.

**Basic-distributed functionality:**

As 'basic' but with Docker Compose / Swarm containerization.

**Gateway functionality:**

1. Receive REST requests.
2. Validate the request (using the schematic library).
3. If valid submit the request onto a work queue.
4. If invalid return invalid json message to caller.
5. One or more workers will consume the requests and perform the calculation.
6. The workers then submit the results to an output queue.
7. The gateway service listens to the output queue and returns the response.

## Objectives:

* Explore the implementation patterns.
* Consider the performance, failure and scalability characteristics of the basic REST implementation compared to the
gateway 'competing consumer' pattern.
* Generate some rough data for analysis.

## Questions:
* What are the reliability and performance characterists of the basic REST service?
* Is the service scalable, if so how can it be scaled?
* What are the reliability and performance characteristics of the Gateway service?
* What are the pro's / con's of each and When would you choose one over the other?

## Example scenario:

A scalable service to produce market 100% probabilities for a football game based on expected goals for both teams.
The model will be a 'naive' poisson based statistical one with prices being derived from SciPy calculated
correct score grid.

Input POST /football
``` 
{
    "game_id": UID, 
    "home_expected": Float, 
    "away_expected": Float
}
```

Return (Valid)
``` 
{
    "game_id": UID, 
    "home_towin": Float, 
    "away_towin": Float,
    "draw": Float
}
Code: 200 - OK
```

Return (Invalid)
``` 
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
pip freeze > requirements.txt
```

## Testing

``` bash 
# To post to the running gateway

# Valid sample post
curl --data '{"game_id": "qwertyui", "home_expected": 0.1, "away_expected": 1}'  http://localhost:8080/football

# InValid sample post
curl --data '{"game_id": "qwertyui", "home_expected": "0.1", "away_expected": -1}'  http://localhost:8080/football

# Benchmarking with apache bench (~1000 requests per second with single process as basic REST service)
cd test
ab -c 8 -n 10000 -k -p ./post_data.json http://localhost:8080/football

```
## Refs: 
* https://github.com/aio-libs/aiohttp
* https://schematics.readthedocs.io/en/latest/
* https://docs.aiohttp.org/en/stable/index.html
* https://www.roguelynn.com/words/asyncio-we-did-it-wrong/
* https://www.pinnacle.com/en/betting-articles/Soccer/how-to-calculate-poisson-distribution/MD62MLXUMKMXZ6A8
* https://medium.com/containers-on-aws/how-i-do-local-docker-development-for-my-aws-fargate-application-8957e3fdb50
