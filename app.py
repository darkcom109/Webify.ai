from flask import Flask, render_template
from utils.model import generate

app = Flask(__name__)

@app.route("/")
def index():
    output = generate()
    return render_template("index.html", output=output)