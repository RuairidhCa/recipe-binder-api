from api import app, db
from flask import jsonify, request, Response
from api.models.models import Recipe, User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from functools import wraps


def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        recipe_id = kwargs["recipe_id"]
        current_user_id = get_jwt_identity()
        recipe = Recipe.query.get(recipe_id)
        if recipe == None:
            return jsonify(message="Recipe does not exist"), 404
        if current_user_id != recipe.user_id:
            return jsonify(message="Not auth"), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route("/api/recipes", methods=["POST"])
@jwt_required()
def create_recipe():
    current_user = User.query.get(get_jwt_identity())
    data = request.get_json()
    new_recipe = Recipe(
        title=data["title"].strip(),
        url=data["url"].strip(),
        recipe_tags=",".join(data["tags"]),
        user_id=current_user.id,
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "created recipe"}), 201


@app.route("/api/recipes", methods=["GET"])
def get_all_recipes():
    recipes = Recipe.query.all()
    data = [recipe.to_json() for recipe in recipes]
    return jsonify({"data": data}), 200


@app.route("/api/recipes/<recipe_id>", methods=["PUT"])
@jwt_required()
@owner_required
def update_recipe(recipe_id):
    data = request.get_json()
    recipe = Recipe.query.get(recipe_id)
    recipe.title = data["title"].strip()
    recipe.url = data["url"].strip()
    recipe.recipe_tags = ",".join(data["tags"])

    db.session.commit()

    return Response(status=204)


@app.route("/api/recipes/<recipe_id>", methods=["DELETE"])
@jwt_required()
@owner_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()

    return Response(status=204)


@app.route("/api/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    user_exists = User.query.filter_by(username=username).first()

    if user_exists:
        return (
            jsonify({"message": "A user with that username already exists."}),
            409,
        )

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)

    return (
        jsonify({"username": user.username, "id": user.id, "token": access_token}),
        201,
    )


@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return jsonify({"message": "Username or password incorrect"}), 400

    access_token = create_access_token(identity=user.id, expires_delta=False)
    return jsonify({"username": user.username, "id": user.id, "token": access_token})


@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = User.query.get(get_jwt_identity())
    return jsonify(logged_in_as=current_user.username), 200
