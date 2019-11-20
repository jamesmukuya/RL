#dash imports
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input


VALID_USERNAME_PASSWORD_PAIRS = [('james','12345'),('susan','12345')]
# table page size
page_size = 25

#########################
app = dash.Dash(__name__)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout 









if __name__ == '__main__':
    app.run_server(debug=True)