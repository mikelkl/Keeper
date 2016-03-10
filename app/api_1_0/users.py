from app.api_1_0 import api
from app.models import User
from flask import jsonify


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())
