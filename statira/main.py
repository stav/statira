from starlette.requests import Request
from fasthtml.common import fast_app, serve

import index
import upload

app, rt = fast_app(live=True, debug=True)

serve()


@rt("/")
def _():
    return index.page()


@rt("/upload", methods=["POST"])
async def _(request: Request):
    return await upload.post(request)
