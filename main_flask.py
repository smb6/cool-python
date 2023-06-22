from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World! (html)</p>"


@app.route('/hello')
def hello():
    return 'Hello, World (plain)'


@app.route('/about')
def about():
    return 'About page'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
