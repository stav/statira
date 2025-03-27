from starlette.requests import Request
import csv
from io import StringIO
import chardet

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
            Input(
                type="file",
                name="file",
                accept=".csv",
                required=True,
                onchange="document.getElementById('content').innerHTML = '';"
            ),
            Button("Upload", type="submit"),
            method="post",
            action="/upload",
            enctype="multipart/form-data",
            hx_post="/upload",
            hx_target="#content",
        ),
        Div(id="content"),
    )


@rt("/upload", methods=["POST"])
async def upload(request: Request):
    form = await request.form()
    file = form.get("file")
    if not file:
        return "No file provided."
    if not file.filename.endswith(".csv"):
        return "File name must end with 'csv' extension."
    if file.content_type != "text/csv":
        return "Invalid content type. Only CSV files are allowed."
    if file.size > 10 * 1024 * 1024:  # Limit to 10 MB
        return "File is too large. Maximum size is 10 MB."
    if file.size == 0:
        return "File is empty."

    # Detect encoding
    file.file.seek(0)  # Reset file pointer
    preview = file.file.read(1000)  # Read a sample for encoding detection
    encoding = chardet.detect(preview)["encoding"] or "utf-8"

    # Reset file pointer and read content
    file.file.seek(0)
    content = file.file.read().decode(encoding, errors="replace")

    # Analyze CSV structure
    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader, None)  # Extract headers
    sample_rows = [row for _, row in zip(range(5), csv_reader)]  # Extract sample rows
    line_count = sum(1 for _ in csv.reader(StringIO(content)))  # Count lines
    column_count = len(headers) if headers else 0

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
        # Encoding
        Dt("Detected Encoding:"),
        Dd(Code(encoding)),
        # Line Count
        Dt("Total Lines:"),
        Dd(Code(line_count)),
        # Column Count
        Dt("Number of Columns:"),
        Dd(Code(column_count)),
        # Headers
        Dt("Headers:"),
        Dd(Code(headers if headers else "No headers found")),
        # Sample Rows
        Dt("Sample Rows:"),
        Dd(Code(sample_rows)),
        # Preview
        Dt("Raw Preview:"),
        Dd(Code(preview.decode(encoding, errors="replace"))),
    )
