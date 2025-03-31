import io

from starlette.requests import Request
from starlette.datastructures import UploadFile

from anthem import start
from parse import parse_csv, parse_display, parse_message


async def post(request: Request):
    form = await request.form()
    file = form.get("file")
    # Process the sample CSV file if no file is provided
    if not file:
        file = UploadFile(
            filename="sample.csv",
            headers={"content-type": "text/csv"},
            file=io.BytesIO(sample_csv_file_contents.encode("utf-8")),
            size=len(sample_csv_file_contents),
        )
    # Validate the file
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
            process = start(content)
            # datas is a list of dicts from a comprehension that drains the start generator
            datas = [p async for p in process]
            # Messages should be displayed at the top (under the meta)
            for data in datas:
                if data.get("message"):
                    messages.append(parse_message(data))
            # parsed_datas is a list of FT objects to render for display
            parsed_datas = parse_display(datas)
            # Now we can add the output of the processing for each response record
            messages.extend(parsed_datas)

    return messages


sample_csv_file_contents = """\
First Name,Last Name,DOB,MBI,SSN,Medicaid
John,Doe,01/01/1951,123456789,123-45-1111,987654321
Jane,Doe,02/02/1952,234567891,987-65-2222,
John,Smith,01/01/1953,345678912,,987654321
Jane,Smith,02/02/1954,456789123,,
"""
