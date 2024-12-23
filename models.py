from flask_login import UserMixin, current_user
from bson import ObjectId
from datetime import datetime

class Note:
    def __init__(self, db):
        self.db = db

    def add_note(self, data):
        note = {
            "data": data['data'],
            "date": datetime.utcnow(),
             "user_id": data['user_id']
        }
        return self.db.notes.insert_one(note).inserted_id

    def get_all_notes(self, user_id):
        return list(self.db.notes.find({"user_id": user_id}))
    # id = db.Column(db.Integer, primary_key=True)
    # data = db.Column(db.String(10000))
    # date = db.Column(db.DateTime(timezone=True), default=func.now())


# class User(db.model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     first_name = db.Column(db.String(50))


class User(UserMixin):
    def __init__(self, db, user_data=None):
        self.db = db
        self.user_data = user_data

    @property
    def id(self):
        return str(self.user_data.get('_id'))

    @property
    def email(self):
        return self.user_data.get('email')

    @property
    def password(self):
        return self.user_data.get('password')

    @property
    def firstName(self):
        return self.user_data.get('firstName')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_data.get('_id'))

    @staticmethod
    def get_user_by_email(db, email):
        user_data = db.signin_details.find_one({"email": email})
        if user_data:
            return User(db, user_data)
        return None

    @staticmethod
    def get_user_by_id(db, user_id):
        user_data = db.signin_details.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(db, user_data)
        return None

    @staticmethod
    def add_user(db, email, password, firstName):
        user = {
            "email": email,
            "password": password,
            "firstName": firstName
        }
        return db.signin_details.insert_one(user).inserted_id
