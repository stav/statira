from fasthtml.common import (
    Button,
    Div,
    Form,
    H4,
    Input,
    Label,
    P,
    Pre,
    Titled,
)

help = (
    P(
        """
        This tool allows you to upload a CSV file containing Medicaid data.
        You can choose to parse the file contents and check eligibility on Anthem.
        """
    ),
    H4("Example CSV File:"),
    Pre(
        """
First Name,Last Name,DOB,MBI,SSN,Medicaid
John,Doe,01/01/1951,123456789,123-45-1111,987654321
Jane,Doe,02/02/1952,234567891,987-65-2222,
John,Smith,01/01/1953,345678912,,987654321
Jane,Smith,02/02/1954,456789123,,
"""
    ),
)


def page():

    return Titled(
        "Medicaid Eligibility Checker",
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
                    Input(type="checkbox", name="parse", required=True, checked=True),
                ),
                Label(
                    "Check eligibility on Anthem:",
                    Input(type="checkbox", name="anthem"),
                ),
                style="display: flex; gap: 1em;",
            ),
            Button("Upload", type="submit", style="margin-bottom: 0"),
            enctype="multipart/form-data",
            hx_post="/upload",
            hx_target="#results_content",
        ),
        Div(help, id="results_content"),
        style="display: flex; flex-direction: column; gap: 1em; padding: 2em; max-width: 600px; margin: auto;",
    )
