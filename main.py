from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from salesprediction import predict_sales, notValEmail
from pymongo import MongoClient
app = Flask(__name__)
CORS(app)

# connect to MongoDB Atlas
client = MongoClient('mongodb+srv://amirtheswarann:G0lFcDPI8WfxdLxk@sales-forecast.inc7xrp.mongodb.net/?retryWrites=true&w=majority')
db = client['sales_forecast']
# key pass=G0lFcDPI8WfxdLxk
# handle login request
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    if notValEmail(email):
        abort(400, description='Enter a valid email')
    password = data['password']
    print(email, password)
    user = db.users.find_one({'email': email, 'password': password})

    if user:
        print('yes')
        return jsonify({'name': user['name'], 'email': user['email']})
    else:
        abort(401, description='unauthorized')
    # else:
    #     return jsonify({'error': 'Invalid email or password'})

# handle signup request
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['name']
    email = data['email']
    if notValEmail(email):
        abort(400, description='Enter a valid email')
    password = data['password']
    # check if user already exists
    user = db.users.find_one({'email': email})
    if not user:
        # return jsonify({'error': 'Email already registered'})
        db.users.insert_one({'name': name, 'email': email, 'password': password})
        return jsonify({'name': name, 'email': email})
    else:
        abort(401, description='Not a valid user')
    # else:
    #     # add user to database
    #     db.users.insert_one({'name': name, 'email': email, 'password': password})
    #     return jsonify({'name': name, 'email': email})

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve file and date range from form data
    file = request.files['file']
    from_date = request.values.get('fromD')
    to_date = request.values.get('toD')
    return predict_sales(file, from_date, to_date)

if __name__ == '__main__':
    app.run()
