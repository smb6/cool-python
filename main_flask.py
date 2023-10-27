from flask import Flask, request, url_for
import requests

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


# Define some internal routes
@app.route('/internal_route', methods=['POST'])
def internal_route():
    data = request.json  # Get data from the request
    return f'Received data: {data}'


@app.route('/call_internal', methods=['POST'])
def call_internal():
    data_to_send = {"key": "value"}

    # Generate the URL for the internal route using url_for
    internal_route_url = url_for('internal_route')

    # Make a POST request to the internal route and send data
    response = requests.post(internal_route_url, json=data_to_send)

    return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
