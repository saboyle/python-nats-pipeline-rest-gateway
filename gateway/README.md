# NATS REST Gateway example [In Progress]

## Overview

Provides a REST service that uses NATS request-reply to process each calculation request posted to provided endpoints.

The gateway has been implemented as two separate Docker services

1. REST Gateway
2. Worker (Subscribers)

Docker compose is used to provide a 'service' composed of 1..n Gateways and 1..n Workers (and a 1..n NATS cluster).  

Docker Swarm is used to provide dynamic scaling & monitoring of each of the component services.

NATS is used as the fabric to transparent connect the gateway and the worker nodes. 

## Instructions

1. Run NATS server
2a. Start Gateway
2b. Run wiretap(s) to monitor work queue (optional)
3. Test using CURL 

## Performance tests

* 1 Gateway + 1 Worker
* 1 Gateway + 2 Workers
* 2 Gateways + 1 Worker
* 2 Gateways + 2 Workers

## References 

1. https://github.com/nats-io/asyncio-nats/blob/master/examples/aiohttp-example.py