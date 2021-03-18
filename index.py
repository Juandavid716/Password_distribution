from flask import Flask, render_template, request, redirect, url_for
from main import main
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template("index.html")


@app.route('/procesar', methods=['POST'])
def procesar():
    password = request.form.get("password")
    key = main(password)
    return render_template("show.html", password=password, key = key)

if __name__ == '__main__':
    app.run(debug=True)