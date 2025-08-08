import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Config
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'clients.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    haircut_type = db.Column(db.String(100), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return redirect(url_for('list_clients'))

@app.route('/clients')
def list_clients():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('clients.html', clients=clients)

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        name = request.form['name']
        haircut_type = request.form['haircut_type']
        amount_paid = request.form['amount_paid']

        if not name or not haircut_type or not amount_paid:
            return "Please fill all fields", 400

        try:
            amount_paid = float(amount_paid)
        except ValueError:
            return "Amount paid must be a number", 400

        new_client = Client(name=name, haircut_type=haircut_type, amount_paid=amount_paid)

        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('list_clients'))
        except Exception as e:
            return f"Error adding client: {e}", 500

    return render_template('add_client.html')

# Auto create DB tables on startup
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
