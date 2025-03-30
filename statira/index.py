from fasthtml.common import (
    Button,
    Div,
    Form,
    H3,
    Input,
    Label,
    P,
    Titled,
)


def page():

    return Titled(
        "Medicaid Eligibility Checker",
        H3("Upload CSV file"),
        Form(
            Input(
                type="file",
                name="file",
                accept=".csv",
                required=True,
                onchange="document.getElementById('content').innerHTML = '';",
            ),
            P(
                Label(
                    "Parse file contents:",
                    Input(type="checkbox", name="parse"),
                ),
                Label(
                    "Check eligibility on Anthem:",
                    Input(type="checkbox", name="anthem"),
                ),
                style="display: flex; gap: 1em;",
            ),
            Button("Upload", type="submit"),
            enctype="multipart/form-data",
            hx_post="/upload",
            hx_target="#content",
        ),
        Div(id="content"),
    )
