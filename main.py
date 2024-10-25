from flask import Flask

app = Flask(__name__)

@app.route('/wx')
def handle():
    return "hello, this is handle view"

if __name__ == '__main__':
    app.run(debug=True)