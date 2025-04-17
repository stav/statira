from starlette.requests import Request
from fasthtml.common import fast_app, serve

from index import page
from upload import post
from config import PORT, env, fast_config

app, rt = fast_app(**fast_config)
print(f'Using "{env}" environment for {app} on port {PORT}')
serve(port=PORT)


@rt
def index():
    return page()


@rt("/upload", methods=["POST"])
async def upload(request: Request):
    return await post(request)
