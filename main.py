import config
from flask import Flask, request, redirect, send_from_directory
from linkedin import Scrapper
from werkzeug.exceptions import NotFound

app = Flask(__name__)
linkedin_scrapper = Scrapper(config.SCRAP_EMAIL, config.SCRAP_PASS)


@app.route("/get")
def get_linkedin():
    email = request.args.get('e')
    try:
        profile = linkedin_scrapper.get_profile(email)
    except Exception as e:
        print(e)
        if 'err' in request.args:
            return str(e)
        elif 'web' in request.args:
            return redirect('/?errorText', code=200)
        else:
            return ':('
    if 'r' in request.args:
        return redirect(profile, code=302)
    else:
        return profile


@app.route("/")
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route("/static/<path:path>")
def serve_static(path):
    try:
        return send_from_directory('static', path)
    except NotFound as e:
        return send_from_directory('static', 'index.html')


if __name__ == "__main__":
    app.run('0.0.0.0', 9988, debug=True)
