from fasthtml.common import fast_app, Div, P, serve, Titled

app, rt = fast_app(live=True, debug=True)

serve()


@rt
def index():
    return Titled("Hello World!", Div(P("Hello World!"), hx_get="/change"))


@rt("/change")
def get():
    return P("Nice to be here!")
