import io

from starlette.requests import Request
from starlette.datastructures import UploadFile

from anthem import start
from parse import parse_csv, parse_display, parse_message


async def post(request: Request):
    messages = []

    form = await request.form()
    file = form.get("file")
    paste = form.get("paste")
    anthem = form.get("anthem")
    if not file:
        # Check if pasted data from the textarea is provided
        if not paste:
            # No data whatsoever provided
            return "No data provided. Please upload a CSV file."
        else:
            # Create a fake UploadFile object from the pasted data
            file = UploadFile(
                filename="paste.csv",
                headers={"content-type": "text/csv"},
                file=io.BytesIO(paste.encode("utf-8")),
                size=len(paste),
            )

    # Parse the data
    content, display, ok = parse_csv(file)

    # Validate the inputs
    if form.get("file") and paste:
        data = dict(message="Pasted data ignored. Clear file input to upload pasted data.")
        messages.append(parse_message(data))
        ok = False
    if file.content_type != "text/csv":
        data = dict(message="Invalid content type. Only CSV files are allowed.")
        messages.append(parse_message(data))
        ok = False
    if file.size > 10 * 1024 * 1024:
        data = dict(message="File is too large. Maximum size is 10 MB.")
        messages.append(parse_message(data))
        ok = False
    if file.size == 0:
        data = dict(message="File is empty.")
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
