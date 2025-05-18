from flask import Blueprint, request, render_template
from navi.brain import get_navi_response

api = Blueprint("api", __name__)

@api.route("/ask-navi", methods=["POST"])
def ask_navi():
    user_input = request.form.get("user_input", "")
    response = get_navi_response(user_input)
    return render_template("components/output_box.html", response=response)
