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
    Title,
)

help = (
    P(
        """
This tool allows you to upload a
<a href="https://en.wikipedia.org/wiki/Comma-separated_values" target="_blank">CSV file</a>
containing client records.
You can choose to parse the file contents and check eligibility on Anthem.

If you do not select a file, you can still press the Upload button to demo the example CSV file below.

#### Example CSV File:

```csv
First Name,Last Name,DOB,MBI,SSN,Medicaid
John,Doe,01/01/1951,123456789,123-45-1111,987654321
Jane,Doe,02/02/1952,234567891,987-65-2222,
John,Smith,01/01/1953,345678912,,987654321
Jane,Smith,02/02/1954,456789123,,
```
The CSV file should contain the following columns:
- `First Name`
- `Last Name`
- `DOB` (Date of Birth)
- `MBI` (Medicare Beneficiary Identifier)
- `SSN` (Social Security Number) *[optional]*
- `Medicaid` (Medicaid ID) *[optional]*
        """,
        cls="marked",
    ),
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
