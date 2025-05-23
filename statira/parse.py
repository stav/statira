import csv
from io import StringIO

import chardet
from fasthtml.common import (
    Code,
    Dd,
    Div,
    Dl,
    Dt,
    H3,
    Pre,
)


def parse_csv(file):
    # Detect encoding
    file.file.seek(0)  # Reset file pointer
    preview = file.file.read(1000)  # Read a sample for encoding detection
    encoding = chardet.detect(preview)["encoding"] or "utf-8"

    # Check if we have the sample data
    if file.filename == "paste.csv":
        message = "Data from text area uploaded successfully"
    else:
        message = "File uploaded successfully"

    # Reset file pointer and read content
    file.file.seek(0)
    content: str = file.file.read().decode(encoding, errors="replace")

    def csv_reader():
        return csv.reader(StringIO(content))

    # Analyze CSV structure
    reader = csv_reader()
    headers = [h.strip() for h in next(reader, None) or []]
    sample_rows = [row for _, row in zip(range(5), reader) if row]
    line_count = sum(1 for _ in csv_reader())
    row_count = sum(1 for r in csv_reader() if r)
    column_count = len(headers) if headers else 0

    def rows_with_wrong_cols():
        rows = (r for r in csv_reader() if r)
        return [True for row in rows if len(row) != column_count]

    ok = True
    # Validate CSV content
    if len(sample_rows) == 0:
        message = "No data rows found in the uploaded CSV file"
        ok = False
    elif rows_with_wrong_cols():
        message = "Inconsistent number of columns in the uploaded CSV file"
        ok = False

    display = Dl(
        # Close Button
        Div(
            "X",
            title="Clear",
            style="position: absolute; top: 12px; right: 10px; cursor: pointer; font-size: 18px; color: white; border: 1px solid white; border-radius: 4px; padding: 8px 14px; text-align: center;",
            onclick="this.parentElement.outerHTML = '';",
        ),
        # Name
        Dt(f"{message}:"),
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
        # Row Count of lines with data
        Dt("Row Count of lines with data:"),
        Dd(Code(row_count)),
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
        style="border: 1px solid #ccc; padding: 10px; border-radius: 8px; position: relative;",
    )

    return content, display, ok


def parse_display(datas):
    return [
        (
            Div(
                H3(f"Record {i}: {data['user']['firstName']} {data['user']['lastName']}"),
                Div(
                    # Left column - user data
                    Dl(
                        *[
                            (Dt(key), Dd(Code(value)))
                            for key, value in data["user"].items()
                        ],
                        style="flex: 1; margin-right: 10px;",
                    ),
                    # Right column - data items
                    Dl(
                        *[
                            (Dt(key), Dd(Code(value)))
                            for key, value in data.get("data", {}).items()
                            if value
                        ],
                        style="flex: 1;",
                    ),
                    style="display: flex;",
                ),
                style="border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; border-radius: 8px;",
            )
            # We only want to display records that have a user
            if data.get("user")
            else ""
        )
        # This is the comprehension that drains the start generator
        for i, data in enumerate(datas, start=1)
    ]


def parse_message(data):
    return Div(
        H3("Message:"),
        Code(data["message"]),
        style="border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; border-radius: 8px;",
    )
