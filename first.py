from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return '<h3> Hello World! </h3>'

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',)