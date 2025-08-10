from flask import Flask, render_template, request

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# List clients page (just a placeholder since we're not storing data)
@app.route('/clients')
def list_clients():
    return "Client list feature not implemented (no database)."

# Add client form and logging
@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        name = request.form.get('name')
        haircut_type = request.form.get('haircut_type')
        amount_paid = request.form.get('amount_paid')

        # Log details to server console
        print(f"New client: {name}, Haircut: {haircut_type}, Paid: {amount_paid}")

        # Return confirmation message
        return f"Received: {name}, {haircut_type}, {amount_paid}"

    return render_template('add_client.html')

if __name__ == '__main__':
    app.run(debug=True)
