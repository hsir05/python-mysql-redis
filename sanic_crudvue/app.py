from sanic import Sanic
from sanic_cors import CORS
from aoiklivereload import LiveReloader

from crud import crud_bp, db, ShanghaiPersonInfo, User, Banner, Roles, LOGO

from config import CONFIG

reloader = LiveReloader()
reloader.start_watcher_thread()

app = Sanic(__name__)

CORS(app,
     automatic_options=True)

app.config.LOGO = LOGO.format(
    ', 001')


@app.middleware('response')
async def custom_banner(request, response):
    response.headers["content-type"] = "application/json"


@crud_bp.listener('after_server_stop')
async def close_connection(app, loop):
    print('close')
    await db.close()


app.blueprint(crud_bp)

app.config.from_object(CONFIG)

db.create_tables([ShanghaiPersonInfo, User, Banner, Roles], safe=True)

app.run(host="0.0.0.0", port=8000, debug=app.config['DEBUG'])
