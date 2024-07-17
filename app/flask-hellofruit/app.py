from flask import Flask, render_template
import fruitbowl.fruit as fr

app = Flask(__name__)


@app.route("/")
def index():
    fruit = fr.get_fruit()
    return render_template("index.html", fruit=fruit)


if __name__ == "__main__":
    app.run()
