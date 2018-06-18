# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

# Setup the app
app = dash.Dash()

app.css.append_css({
    'external_url': ('https: // maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/'
                     'css/bootstrap.min.css')
})

app.layout = html.Div([
    html.Div(
        [
            dcc.Markdown(
                '''
                # A View that shows the the devolpment of buybox prices
                First Fail
                '''.replace('  ', '')
            ),
            dcc.Markdown(
                '''
                # A View that shows the the devolpment of buybox prices
                First Fail
                '''.replace('  ', '')
            )
        ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
