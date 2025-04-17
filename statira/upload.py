import io

from starlette.requests import Request
from starlette.datastructures import UploadFile

from anthem import start
from parse import parse_csv, parse_display, parse_message


async def post(request: Request):
    form = await request.form()
    file = form.get("file")
    paste = form.get("paste")
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
    # Validate the file
    if file.content_type != "text/csv":
        return "Invalid content type. Only CSV files are allowed."
    if file.size > 10 * 1024 * 1024:
        return "File is too large. Maximum size is 10 MB."
    if file.size == 0:
        return "File is empty."

    messages = []

    content, display, ok = parse_csv(file)
    messages.append(display)

    if ok and form.get("anthem"):
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
