### https://www.youtube.com/watch?v=WxGBoY5iNXY
from sqlalchemy.sql.expression import false
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import func
from functools import wraps
import uuid
import jwt
import datetime
import pytz

### Trial PUSH

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///USERS.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model): ###Table for Users
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    mobile_number = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __init__(self,public_id,fname, lname, mobile_number, email, password, admin):
        self.public_id = public_id
        self.fname = fname
        self.lname = lname
        self.mobile_number = mobile_number
        self.email = email
        self.password = password
        self.admin = admin

class UserSchema(ma.Schema):
    class Meta:
        fields = ("public_id", "fname", "lname", "mobile_number", "email", "password", "admin")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class User_Logs(db.Model): #Table for 
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    time_in = db.Column(db.String(50))
    date_in = db.Column(db.String(50))
    user_id = db.Column(db.Integer)

    def __init__(self, fname, lname, time_in, date_in, user_id):
        self.fname = fname
        self.lname = lname
        self.time_in = time_in
        self.date_in = date_in
        self.user_id = user_id

class LogsSchema(ma.Schema):
    class Meta:
        fields = ("fname", "lname", "time_in", "date_in")

log_schema = LogsSchema()
logs_schema = LogsSchema(many=True)

@app.route('/api/login', methods =['GET','POST'])
def login():
    Email = request.json.get("email") #Get from the Web | Username
    Password = request.json.get("password") #Get from the Web | Password

    user = User.query.filter_by(email=Email).first() #Query user credential in the database
    if check_password_hash(user.password, Password): #Check Hashed Password
        result = user_schema.dump(user)
        print(result)
        return jsonify({'public_id' : user.public_id})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required'})

@app.route('/api/visitorLogin', methods =['GET','POST'])
def visitorLogin():
    Email = request.json.get("email") #Get from the Web | Username
    Password = request.json.get("password") #Get from the Web | Password

    user = User.query.filter_by(email=Email).first() #Query user credential in the database
    if check_password_hash(user.password, Password): #Check Hashed Password
        #result = user_schema.dump(user)
        date_in_local = (datetime.datetime.now(pytz.timezone('Asia/Manila'))).strftime("%x")
        time_in_local = (datetime.datetime.now(pytz.timezone('Asia/Manila'))).strftime("%X")
        new_logs = User_Logs(date_in=date_in_local, 
                            time_in=time_in_local,
                            fname=user.fname,
                            lname=user.lname, 
                            user_id=user.public_id)
        db.session.add(new_logs)
        db.session.commit()
        return jsonify({'public_id' : user.public_id})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required'})

@app.route('/api/register', methods=['POST'])
def register():
    Email = request.json.get("email") #Get from the Web | Username
    Password = request.json.get("password") #Get from the Web | Password
    
    hashed_password = generate_password_hash(Password, method='sha256') #Password Hashing

    new_user = User(public_id=str(uuid.uuid4()), email=Email, password=hashed_password, admin=False) #Registering the person
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/api/registerAdmin', methods=['POST'])
def registerAdmin():
    Email = request.json.get("email") #Get from the Web | Username
    Fname = request.json.get("fname")
    Lname = request.json.get("lname")
    Mobile_Number = request.json.get("mobile_number")
    Password = request.json.get("password") #Get from the Web | Password
    
    hashed_password = generate_password_hash(Password, method='sha256') #Password Hashing

    new_user = User(public_id=str(uuid.uuid4()), 
                    fname=Fname, 
                    lname=Lname,
                    mobile_number=Mobile_Number, 
                    email=Email, 
                    password=hashed_password, 
                    admin=True) #Registering the person
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/api/registerVisitor', methods=['POST'])
def registerVisitor():
    Email = request.json.get("email") #Get from the Web | Username
    Fname = request.json.get("fname")
    Lname = request.json.get("lname")
    Mobile_Number = request.json.get("mobile_number")
    Password = request.json.get("password") #Get from the Web | Password
    
    hashed_password = generate_password_hash(Password, method='sha256') #Password Hashing

    new_user = User(public_id=str(uuid.uuid4()), 
                    fname=Fname, 
                    lname=Lname,
                    mobile_number=Mobile_Number, 
                    email=Email, 
                    password=hashed_password, 
                    admin=False) #Registering the person
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/api/get_logs', methods=['GET'])
def get_logs():
    user_logs = User_Logs.query.all() #LogsSchema
    result = LogsSchema.dump(user_logs)
    return LogsSchema.jsonify(result).data

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'user' : output})

@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    users = User.query.all()

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    print(user_data)
    return jsonify({'user' : user_data})
    #return jsonify({user_data})

@app.route('/user', methods=['POST'])
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    users = User.query.all()
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    users = User.query.all()

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})
    
    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message' : 'The user has been deleted!'})

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)