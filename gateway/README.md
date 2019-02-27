# NATS REST Gateway example [In Progress]

## Overview

Provides a REST service that uses NATS request-reply to process each calculation request posted to provided endpoints.

The gateway has been implemented as two separate Docker services

1. REST Gateway
2. Worker (Subscribers)

Docker compose is used to provide a 'service' composed of 1..n Gateways and 1..n Workers.  Using Docker Swarm these 
can be independently and dynamically scaled.

NATS is used as the fabric transparently connecting the gateway and the worker nodes. 

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

https://github.com/nats-io/asyncio-nats/blob/master/examples/aiohttp-example.py