from aiohttp import web
from basic.schema.football import FootballRequest

async def post(request):
    try:
        data = await request.json()

        try:
            jreq = FootballRequest(data)
            jreq.validate()
            return web.json_response(data)

        except:
            data = {'error': 'Bad Football Request'}
            return web.json_response(data)

    except:
        data = {'error': 'Invalid JSON in request'}
        return web.json_response(data)


app = web.Application()
app.add_routes([web.post('/football', post)])


if __name__ == "__main__":
    web.run_app(app)