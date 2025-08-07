import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use DATABASE_URL if provided (Render's Postgres), else fallback to SQLite
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    haircut_type = db.Column(db.String(150), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

@app.route("/")
def home():
    return redirect("/clients")

@app.route("/add", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        name = request.form["name"].strip()
        haircut_type = request.form["haircut_type"].strip()
        amount_paid = request.form["amount_paid"].strip()

        if not name or not haircut_type or not amount_paid:
            return "All fields are required", 400

        try:
            amount_paid = float(amount_paid)
        except ValueError:
            return "Amount must be a number", 400

        new_client = Client(name=name, haircut_type=haircut_type, amount_paid=amount_paid)
        db.session.add(new_client)
        db.session.commit()
        return redirect("/clients")

    return render_template("add.html")

@app.route("/clients")
def list_clients():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template("clients.html", clients=clients)

if __name__ == "__main__":
    app.run(debug=True)

