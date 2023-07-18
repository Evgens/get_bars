from flask import Flask, jsonify
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route("/sumo/api/v1.0/bars", methods=["POST"])
def post_bars():
    if not request.json or not "sec" in request.json:
        abort(400)
    proc_bar(request.json)
    return jsonify({"bar": "add"})


@app.route("/")
def index():
    return "Hello, SuMo"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


# --------------------
def proc_bar(json):
    return ""


if __name__ == "__main__":
    app.run(debug=True)
