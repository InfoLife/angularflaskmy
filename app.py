from flask import Flask, request, jsonify, session, render_template, abort, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from werkzeug import generate_password_hash, check_password_hash
import psycopg2
import urlparse
from flask.ext.heroku import Heroku
import os
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
app = Flask(__name__)
api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/test'
#conn = psycopg2.connect(dbname='test', port='5432', user='postgres',
                            #password='root', host='localhost')
heroku = Heroku(app)
db = SQLAlchemy(app)
app.secret_key = 'why would I tell you my secret key?'

# Create our database model
class User(db.Model):
    __tablename__ = "users"

    def __init__(self, firstname, lastname, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

class UsersBook(db.Model):
    __tablename__ = "users_books"

    def __init__(self, name, price, userid):
        self.name = name
        self.price = price
        self.userid = userid

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.String(120))
    userid = db.Column(db.Integer)



@app.route('/api/users/logout')
def logout():
    session.pop('user', None)
    return jsonify({'result': 'success'})

@app.route('/')
def index():
    return app.send_static_file('index.html')


class CreateUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName')
        parser.add_argument('lastName')
        parser.add_argument('username')
        parser.add_argument('password')
        
        args= parser.parse_args()
        
        firstname = args['firstName']
        lastname = args['lastName']
        username = args['username']
        password = args['password']
        hashed_password = generate_password_hash(password)
        try:
            user = User.query.filter_by(username=args['username']).first()
            if not user:
                reguser = User(firstname,lastname,username,hashed_password)
                db.session.add(reguser)
                db.session.commit()
                #return {'status':200,'message':'User create Success'}
                return {'success': True}
            else:
                return {'status':100,'message':'User  already exists'}
        except:
            return {'status':100,'message':'User creation failure'}


class AuthenticateUser(Resource):
    def post(self):
        try:
            #json_data = request.json
            parser = reqparse.RequestParser()
            parser.add_argument('username')
            parser.add_argument('password')

            args= parser.parse_args()

            username = args['username']
            password = args['password']
            #username = json_data['username']
            #password = json_data['password']

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = (%s)", (username,))
            data = cursor.fetchall()

            user = User.query.filter_by(username=args['username']).first()

            if user and check_password_hash(
            user.password, args['password']):
        
                session['user'] = data[0][0]

                return {'success': True}
            else:
                return {'status':100,'message':'Wrong  email/password'}
            

            #user = User.query.filter_by(username=args['username']).first()
            #user = User.query.filter_by(username=json_data['username']).first()
            #if user and check_password_hash(
            #user.password, json_data['password']):
                
        except:
            return {'status':100,'message':'Authentication failure'}

@app.route('/api/addbook',methods=['POST'])
def addbook():
    if session.get('user'):
        json_data = request.json
        user = session.get('user')
        name = json_data['name']
        price = json_data['price']

        addbook = UsersBook(name,price,user)
        db.session.add(addbook)
        db.session.commit()
        return jsonify( {'success': True} )
    else:
        return {'status':100,'message':'Unauthorized Access'}

@app.route('/api/getBook')
def getBook():
    if session.get('user'):
        user = session.get('user')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_books WHERE userid = (%s)", (user,))
        books = cursor.fetchall()
        books_dict = []
        for book in books:
            book_dict = {
                'id': book[0],
                'name': book[1],
                'price': book[2]}
            books_dict.append(book_dict)
        return json.dumps(books_dict)
    else:
        return {'status':100,'message':'Unauthorized Access'}

@app.route('/api/DeleteBook', methods=['DELETE'])
def deleteBook():
    if session.get('user'):
        user = session.get('user')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users_books WHERE userid = (%s)", (user,))
        conn.commit()
        return json.dumps({'status':'OK'})
    else:
        return {'status':100,'message':'Unauthorized Access'}
        
    

api.add_resource(CreateUser, '/api/CreateUser')
api.add_resource(AuthenticateUser, '/api/AuthenticateUser')
    

if __name__ == '__main__':
    #app.debug = True
    app.run()
