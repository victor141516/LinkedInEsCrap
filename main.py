from flask import Flask, request, redirect
from linkedin import get_profile
app = Flask(__name__)

@app.route("/")
def get_linkedin():
    email = request.args.get('e')
    try:
        profile = get_profile(email)
    except Exception:
        return ':('
    if request.args.has_key('r'):
        return redirect("http://www.example.com", code=302)
    else:
        return profile

if __name__ == "__main__":
    app.run('0.0.0.0', 9988, debug=True)
