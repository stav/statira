from starlette.requests import Request
from fasthtml.common import fast_app, serve, Link, MarkdownJS

from index import page
from upload import post
from config import PORT

dev_config = {
    "live": True,
    "debug": True,
    "hdrs": [
        Link(rel="icon", href="/static/favicon.ico"),
        MarkdownJS(),
    ],
    "static_path": "./statira",
}

app, rt = fast_app(**dev_config)

serve(port=PORT)


@rt
def index():
    return page()


@rt("/upload", methods=["POST"])
async def upload(request: Request):
    return await post(request)
