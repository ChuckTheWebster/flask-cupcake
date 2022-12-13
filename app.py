"""Flask app for Cupcakes"""

# from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake, DEFAULT_IMAGE

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)

@app.get("/")
def home_page():
    """Renders home page"""
    return render_template('home.html')

@app.get("/api/cupcakes")
def get_all_cupcakes():
    """Returns data about all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Gets data on one cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Creates a cupcake with flavor, size, rating, and image from body of req"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    try:
        image = request.json["image"] or None
    except:
        image = None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
    """Updates an existing cupcake
    returns JSON: {cupcake: [{id, flavor, rating, size, image}]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)

    try:
        cupcake.image = request.json["image"] or DEFAULT_IMAGE
    except:
        cupcake.image = cupcake.image

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized))

@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Removes cupcake from db and returns deleted message
    returns JSON {deleted: cupcake_id}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=cupcake_id)