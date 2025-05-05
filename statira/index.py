from fasthtml.common import (
    A,
    Button,
    Div,
    Form,
    H2,
    Img,
    Input,
    Label,
    P,
    Textarea,
    Title,
)

from upload import sample_csv_file_contents

help = P(
    """
This tool allows you to upload a
<a href="https://en.wikipedia.org/wiki/Comma-separated_values" target="_blank">CSV file</a>
from a local file on your computer or enter the data directly into the text area.
Check the box to verify eligibility using Anthem.
""",
    cls="marked",
)


def page():

    return (
        Title("Medicaid Eligibility Checker"),
        Div(
            H2(
                A(
                    Img(
                        src="/static/favicon.ico",
                        alt="logo",
                        style="margin-right: 0.3em",
                    ),
                    href="/",
                ),
                "Medicaid Eligibility Checker",
                style="margin-bottom: 0",
            ),
            Form(
                Input(
                    type="file",
                    name="file",
                    accept=".csv",
                    onchange="document.getElementById('results_content').innerHTML = '';",
                ),
                P(
                    Button(
                        "Load Sample Data",
                        type="button",
                        onclick="document.querySelector('textarea[name=\"paste\"]').value = `"
                        + sample_csv_file_contents.replace("`", "\\`")
                        + "`;",
                        style="margin-bottom: 1em;",
                    ),
                    Label(
                        "Parse file contents:",
                        Input(
                            type="checkbox", name="parse", required=True, checked=True
                        ),
                    ),
                    Label(
                        "Check eligibility on Anthem:",
                        Input(type="checkbox", name="anthem"),
                    ),
                    style="display: flex; gap: 1em;",
                ),
                Textarea(
                    name="paste",
                    placeholder=sample_csv_file_contents,
                    style="margin-bottom: 1em; width: 100%; min-height: 100px;",
                ),
                Button(
                    "Upload",
                    type="submit",
                    style="margin-bottom: 0",
                    onchange="document.getElementById('results_content').innerHTML = 'loading...';",
                ),
                enctype="multipart/form-data",
                hx_post="/upload",
                hx_target="#results_content",
            ),
            Div(help, id="results_content"),
            style="display: flex; flex-direction: column; gap: 1em; padding: 2em; max-width: 600px; margin: auto;",
        ),
    )
