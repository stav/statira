import csv
from io import StringIO

import chardet
from starlette.requests import Request
from fasthtml.common import (
    Button,
    Code,
    Dd,
    Div,
    Dl,
    Dt,
    fast_app,
    Form,
    H3,
    Input,
    Label,
    P,
    Pre,
    serve,
    Titled,
)

from sserver import anthem

app, rt = fast_app(live=True, debug=True)

serve()


@rt
def index():
    return Titled(
        "Medicaid Eligibility Checker",
        H3("Upload CSV file"),
        Form(
            Input(
                type="file",
                name="file",
                accept=".csv",
                required=True,
                onchange="document.getElementById('content').innerHTML = '';",
            ),
            P(
                Label(
                    "Parse file contents:",
                    Input(type="checkbox", name="parse"),
                ),
                Label(
                    "Check eligibility on Anthem:",
                    Input(type="checkbox", name="anthem"),
                ),
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


def parse_csv(file):
    # Detect encoding
    file.file.seek(0)  # Reset file pointer
    preview = file.file.read(1000)  # Read a sample for encoding detection
    encoding = chardet.detect(preview)["encoding"] or "utf-8"

    # Reset file pointer and read content
    file.file.seek(0)
    content: str = file.file.read().decode(encoding, errors="replace")

    # Analyze CSV structure
    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader, None)  # Extract headers
    sample_rows = [row for _, row in zip(range(5), csv_reader)]
    csv_reader = csv.reader(StringIO(content))  # Reset csv_reader
    line_count = sum(1 for _ in csv_reader)
    column_count = len(headers) if headers else 0

    display = Dl(
        # Name
        Dt("File uploaded successfully:"),
        Dd(Code(file.filename)),
        # Type
        Dt("Content type:"),
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
        Dd(Pre(preview.decode(encoding, errors="replace"))),
        # Style Dl
        style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;",
    )

    return content, display


def parse_display(datas):
    return Div(
        *[
            Div(
                H3(f"Record {i}:"),
                Code(f"{user}"),
                Dl(
                    *[
                        (Dt(key), Dd(Code(value)))
                        for key, value in data.items()
                        if value
                    ]
                ),
                style="border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; border-radius: 8px;",
            )
            for i, (user, data) in enumerate(datas, start=1)
        ]
    )


@rt("/upload", methods=["POST"])
async def upload(request: Request):
    form = await request.form()
    file = form.get("file")
    if not file:
        return "No file provided."
    # if not file.filename.lower().endswith(".csv"):
    #     return "File name must end with 'csv' extension."
    if file.content_type != "text/csv":
        return "Invalid content type. Only CSV files are allowed."
    if file.size > 10 * 1024 * 1024:
        return "File is too large. Maximum size is 10 MB."
    if file.size == 0:
        return "File is empty."

    messages = []

    if form.get("parse"):
        content, display = parse_csv(file)
        messages.append(display)

        if form.get("anthem"):
            process = anthem.start(content)
            datas = [data async for data in process]
            json_display = parse_display(datas)
            messages.append(json_display)

    else:
        if form.get("anthem"):
            messages.append(
                "Anthem eligibility check is not available without parsing the file."
            )

    return messages
