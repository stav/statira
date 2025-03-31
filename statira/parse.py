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
        # Close Button
        Div(
            "X",
            title="Clear",
            style="position: absolute; top: 12px; right: 10px; cursor: pointer; font-size: 18px; color: white; border: 1px solid white; border-radius: 4px; padding: 8px 14px; text-align: center;",
            onclick="this.parentElement.outerHTML = '';",
        ),
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
        style="border: 1px solid #ccc; padding: 10px; border-radius: 8px; position: relative;",
    )

    return content, display


def parse_display(datas):
    return [
        (
            Div(
                H3(f"Record {i}:"),
                Code(f"{data['user']}"),
                Dl(
                    *[
                        (Dt(key), Dd(Code(value)))
                        for key, value in data.get("data", {}).items()
                        if value
                    ]
                ),
                style="border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; border-radius: 8px;",
            )
            # We only want to display records that have a user
            if data.get("user")
            else ""
        )
        for i, data in enumerate(datas, start=1)
    ]


def parse_message(data):
    return Div(
        H3("Message:"),
        Code(data["message"]),
        style="border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; border-radius: 8px;",
    )
