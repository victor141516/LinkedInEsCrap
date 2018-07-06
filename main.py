from flask import Flask, request
from linkedin import get_profile
app = Flask(__name__)

@app.route("/")
def get_linkedin():
    email = request.args.get('e')
    return get_profile(email)

if __name__ == "__main__":
    app.run('0.0.0.0', 9988, debug=True)
