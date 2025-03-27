from starlette.requests import Request

from fasthtml.common import (
    fast_app,
    serve,
    Form,
    Titled,
    Div,
    Input,
    Button,
    Code,
    Dl,
    Dt,
    Dd,
)

app, rt = fast_app(live=True, debug=True)

serve()


@rt
def index():
    return Titled(
        "Hello World!",
        Form(
            Input(type="file", name="file", accept=".csv"),
            Button("Upload", type="submit"),
            method="post",
            enctype="multipart/form-data",
            action="/upload",
            hx_post="/upload",
            hx_target="#content",
        ),
        Div(id="content"),
    )


@rt("/upload", methods=["POST"])
async def upload(request: Request):
    form = await request.form()
    file = form["file"]

    # filename = file.filename
    # with open(filename, "wb") as f:
    #     f.write(file.file.read())
    # print(f"File saved as: {filename}")
    # print(type(file), file)
    # print(dir(file))
    # file.file.seek(0)  # Reset the file pointer to the beginning

    preview_size = min(1000, file.size)
    buffer = file.file.read(preview_size)
    contents = buffer.decode("utf-8", errors="replace")

    return Dl(
        # Name
        Dt("File uploaded successfully:"),
        Dd(Code(file.filename)),
        # Type
        Dt("Content type: "),
        Dd(Code(file.content_type)),
        # Size
        Dt("Size: (bytes)"),
        Dd(Code(file.size)),
        # File object
        Dt(f"Preview: ({preview_size} bytes)"),
        Dd(Code(contents)),
    )
