from fasthtml.common import (
    A,
    Button,
    Div,
    Fieldset,
    Form,
    H2,
    Img,
    Input,
    Label,
    Legend,
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

You can choose to check eligibility on Anthem by checking the box.
Then press the Upload button to send your data to the server.
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
                Fieldset(
                    Legend("Upload CSV file", style="margin-bottom: 0"),
                    Input(
                        id="file",
                        type="file",
                        name="file",
                        accept=".csv",
                        onchange="checkInputs()",
                        style="padding-right: 3.5em; margin-bottom: 0",
                    ),
                    Button(
                        "X",
                        cls="outline",
                        type="button",
                        style="position: absolute; right: 1em; top: 0.5em; padding: 0.5em 1em;",
                        title="Clear file input",
                        onclick="document.getElementById('file').value = ''",
                    ),
                    style="position: relative; display: flex; gap: 1em; border: 1px solid #ccc; padding: 0.5em; border-radius: 4px;",
                ),
                Fieldset(
                    Legend("Paste CSV data", style="margin-bottom: 0"),
                    Textarea(
                        sample_csv_file_contents,
                        id="paste",
                        name="paste",
                        title="Clear text input",
                        style="margin-bottom: 0; width: 100%; min-height: 100px;",
                        onchange="checkInputs()",
                    ),
                    Button(
                        "X",
                        cls="outline",
                        type="button",
                        style="position: absolute; right: 1em; top: 0.4em; padding: 0.5em 1em;",
                        title="Clear text input",
                        onclick="document.getElementById('paste').value = ''",
                    ),
                    style="position: relative; display: flex; gap: 1em; border: 1px solid #ccc; padding: 0.5em; border-radius: 4px;",
                ),
                Fieldset(
                    Legend("Check eligibility", style="margin-bottom: 0"),
                    Label(
                        "Anthem:",
                        Input(type="checkbox", name="anthem"),
                    ),
                    style="display: flex; gap: 1em; border: 1px solid #ccc; padding: 0.5em; border-radius: 4px;",
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
