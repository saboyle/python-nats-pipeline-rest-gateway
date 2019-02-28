import sys
import asyncio
import datetime
import signal
import json
import traceback

from nats.aio.client import Client as NATS

from model.football_poisson import calc_mw
from schema.football import FootballRequest


def calculate(msg):
    try:
        print("Received calculation request")
        jreq = FootballRequest(json.loads(msg.data))
        jreq.validate()
    except Exception as e:
        print(e)
        traceback.print_stack()

    # Valid calculation request
    preq = jreq.to_primitive()
    resp = calc_mw(preq['home_expected'], preq['away_expected'])
    print("Response calculated:", resp)
    return resp


def main(loop, subject):
    #####################
    # Connection to NATS
    #####################
    nc = NATS()
    yield from nc.connect("localhost:4222", loop=loop)

    #####################
    # Message Handlers
    #####################
    async def mh_markets(msg):
        resp = calculate(msg)
        print("Response returned to caller:", resp)
        await nc.publish(msg.reply, json.dumps(resp).encode())
        print("Published response to reply queue:", resp)

    yield from nc.subscribe(subject, cb=mh_markets)


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == "__main__":

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main(event_loop, subject="markets"))

    signal.signal(signal.SIGINT, signal_handler)

    print("Worker Enabled: Listening to 'markets'")
    event_loop.run_forever()
