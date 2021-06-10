from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ryan C'}
    apis = [
        {
            'request': {'requestName': 'Login'},
            'status': {'statusCode': '200'}
        },
        {
            'request': {'requestName': 'Users'},
            'status': {'statusCode': '400'}
        }
    ]
    return render_template('index.html', title='Home', user=user, apis=apis)
