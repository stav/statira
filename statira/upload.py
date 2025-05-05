import io

from starlette.requests import Request
from starlette.datastructures import UploadFile, Headers

from anthem import start
from parse import parse_csv, parse_display, parse_message


async def post(request: Request):
    messages = []

    form = await request.form()
    file = form.get("file")
    paste = form.get("paste")
    anthem = form.get("anthem")

    # Warn if both file and paste are provided
    if file and paste:
        data = dict(
            message="Pasted data ignored. Clear file input to upload pasted data."
        )
        messages.append(parse_message(data))
        ok = False

    # Check if pasted data from the textarea is provided
    # If not, create a fake UploadFile object from the pasted data
    if not file:
        if not paste:
            # No data whatsoever provided
            return "No data provided. Please upload a CSV file."
        else:
            # Create a fake UploadFile object from the pasted data
            file = UploadFile(
                filename="paste.csv",
                headers=Headers({"content-type": "text/csv"}),
                file=io.BytesIO(str(paste).encode("utf-8")),
                size=len(str(paste)),
            )

    # Parse and validate the contents of the file
    content, display, ok = parse_csv(file)

    # More validation
    if isinstance(file, UploadFile):

        if file.content_type != "text/csv":
            data = dict(message="Invalid content type. Only CSV files are allowed.")
            messages.append(parse_message(data))
            ok = False

        if file.size is not None:

            if file.size == 0:
                data = dict(message="File is empty.")
                messages.append(parse_message(data))
                ok = False

            if file.size > 10 * 1024 * 1024:
                data = dict(message="File is too large. Maximum size is 10 MB.")
                messages.append(parse_message(data))
                ok = False

    if anthem and not ok:
        data = dict(message="Data not sent to Anthem because it requires valid CSV.")
        messages.append(parse_message(data))

    # Now we can add the output of the processing for each response record
    messages.append(display)

    if anthem and ok:
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
"""
