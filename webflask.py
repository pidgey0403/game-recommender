from flask import Flask, render_template, url_for,redirect, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('websiteg.html')


@app.route("/<name>")
def user(name):
	return f"Hello {name}!"


@app.route("/admin")
def admin():
	return redirect(url_for("index"))

@app.route("/vmd_timestamp")
def vmd_timestamp():
	return render_template('vmd_timestamp.html')


if __name__=='__main__':
	app.run(debug = True)


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", name=user))
    else:
        return render_template("login.html")


