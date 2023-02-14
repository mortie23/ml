from flask import Flask, render_template
import helloworld.helloworld as hw

app = Flask(__name__)


@app.route('/')
def index():
    hello_message = hw.helloworld('christopher')
    return render_template('index.html', hello=hello_message)


if __name__ == '__main__':
    app.run()
