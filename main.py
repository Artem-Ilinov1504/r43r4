from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///order.db"
db = SQLAlchemy(app)

order_product_association = db.Table(
    "order_product",
    db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"))
)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)




class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_owner = db.Column(db.String(50), nullable=False, unique=True)
    products = db.relationship("Product",
                             secondary=order_product_association,
                             backref="orders")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_order", methods=["POST"])
def add_order():
    name = request.form["name"]
    new_order = Order(name_of_owner=name)
    db.session.add(new_order)
    db.session.commit()
    return f"Order {new_order.name_of_owner} created"


@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    new_product = Product(name=name)
    db.session.add(new_product)
    db.session.commit()
    return f"Product {new_product.name} created "


@app.route("/pair_order_product", methods=["POST"])
def pair_order_product():
    order_id = request.form["order_id"]
    product_id = request.form["product_id"]
    order = Order.query.get(order_id)
    product = Product.query.get(product_id)
    order.products.append(product)
    db.session.commit()
    return f"Teacher {order.name_of_owner} and {product.name} paired"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)