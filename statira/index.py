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
    Script,
    Textarea,
    Title,
)

help = (
    P(
        """
This tool allows you to upload a
<a href="https://en.wikipedia.org/wiki/Comma-separated_values" target="_blank">CSV file</a>
from a local file on your computer or enter the data directly into the text area.

You can choose to check eligibility on Anthem.

If you do not select a file, you can still press the Upload button to demo the example CSV data shown above.
        """,
        cls="marked",
    ),
)

sample_csv_file_contents = """\
First Name,Last Name,DOB,MBI,SSN,Medicaid
John,Doe,01/01/1951,123456789,123-45-1111,987654321
Jane,Doe,02/02/1952,234567891,987-65-2222,
John,Smith,01/01/1953,345678912,,987654321
Jane,Smith,02/02/1954,456789123,,
"""


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
                Div(
                    Input(
                        id="file",
                        type="file",
                        name="file",
                        accept=".csv",
                        onchange="checkInputs()",
                        style="padding-right: 3em",
                    ),
                    Button(
                        "X",
                        cls="outline",
                        type="button",
                        style="position: absolute; right: 0; top: 0.4em; padding: 0.5em 1em;",
                        title="Clear file input",
                        onclick="document.getElementById('file').value = ''",
                    ),
                    style="position: relative; display: flex; gap: 1em;",
                ),
                P(
                    Label(
                        "Check eligibility on Anthem:",
                        Input(type="checkbox", name="anthem"),
                    ),
                    style="display: flex; gap: 1em;",
                ),
                Div(
                    Textarea(
                        sample_csv_file_contents,
                        id="paste",
                        name="paste",
                        style="margin-bottom: 1em; width: 100%; min-height: 100px;",
                        onchange="checkInputs()",
                    ),
                    Button(
                        "X",
                        cls="outline",
                        type="button",
                        style="position: absolute; right: 0; top: 0.4em; padding: 0.5em 1em;",
                        title="Clear text input",
                        onclick="document.getElementById('paste').value = ''",
                    ),
                    style="position: relative; display: flex; gap: 1em;",
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
        Script(
            " const checkInputs = () => document.getElementById('results_content').innerHTML = '';"
        ),
    )
