from flask import Flask, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    return "Welcome to my Flask App!"

# Define a route for the API data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "This is a GET response!"})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)