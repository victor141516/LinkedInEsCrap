import config
from datetime import datetime
from flask import Flask, request, redirect, send_from_directory
from linkedin import Scrapper
from redpie import Redpie
from werkzeug.exceptions import NotFound

app = Flask(__name__)
cache = Redpie(0, 'linkedinescrap-redis')

cookies = None
if '_cookies' in cache:
    cookies = cache['_cookies']
linkedin_scrapper = Scrapper(config.SCRAP_EMAIL, config.SCRAP_PASS, cookie_jar=cookies)


@app.route("/get")
def get_linkedin():
    email = request.args.get('e')
    profile = None
    if email in cache:
        cached_profile = cache[email]
        if (cached_profile['date']-datetime.now()).days < 30:
            profile = cached_profile['data']

    if profile is None:
        try:
            profile = linkedin_scrapper.get_profile(email)
            cache[email] = {'date': datetime.now(), 'data': profile}
        except Exception as e:
            print(e)
            if 'err' in request.args:
                return str(e)
            elif 'web' in request.args:
                return redirect('/?errorText', code=302)
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
    app.run('0.0.0.0', 5000, debug=True)
