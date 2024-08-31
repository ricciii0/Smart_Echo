from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '''
            <html>
                <body>
                    <h1>Welcome to the Home Page</h1>
                    <a href="/login"><button>Login</button></a>
                </body>
            </html>
        '''


@app.route('/login')
def login():
    return '''
            <html>
                <body>
                    <h1>Hello</h1>
                </body>
            </html>
        '''


if __name__ == '__main__':
    app.run(debug=True)
