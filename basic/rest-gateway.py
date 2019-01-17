from aiohttp import web
import json

from basic.schema.football import FootballRequest, FootballResponse
from basic.model.football_poisson import calc_mw

async def post(request):
    try:
        data = await request.json()

        try:
            jreq = FootballRequest(data)
            jreq.validate()

            # Handle valid request
            markets = calc_mw(jreq['home_expected'], jreq['away_expected'])
            markets['game_id'] = jreq['game_id']

            try:
                # Construct and validate response
                data = FootballResponse(markets)
                data.validate()
                return web.json_response(data.to_primitive()) # Converts back to python native dict

            except Exception as e:
                data = json.dumps({'error': 'Bad Football Response', 'message': f"{e}"})
                raise web.HTTPBadRequest(text=data)

        except:
            data = json.dumps({'error': 'Bad Football Request'})
            return web.HTTPBadRequest(text=data)

    except:
        data = json.dumps({'error': 'Invalid JSON in request'})
        raise web.HTTPBadRequest(text=data)


app = web.Application()
app.add_routes([web.post('/football', post)])


if __name__ == "__main__":
    web.run_app(app)