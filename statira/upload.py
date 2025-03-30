from starlette.requests import Request
from parse import parse_csv, parse_display

from sserver import anthem


async def post(request: Request):
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
