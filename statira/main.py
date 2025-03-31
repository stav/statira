from starlette.requests import Request
from fasthtml.common import fast_app, serve, Link, MarkdownJS

import index
import upload

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

serve()


@rt("/")
def _():
    return index.page()


@rt("/upload", methods=["POST"])
async def _(request: Request):
    return await upload.post(request)
