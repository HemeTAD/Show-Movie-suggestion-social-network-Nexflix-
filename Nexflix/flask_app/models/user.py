from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


# model the class after the friend table from our database
class User:
    DB = "Nexflix"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.shows = []

    @classmethod
    def register(cls, data):
        query = """
                INSERT into users(first_name, last_name, email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                """
        user_id = connectToMySQL(cls.DB).query_db(query, data)
        print("results:", user_id)
        return user_id

    @classmethod
    def find_by_email(cls, email):
        query = """SELECT * from users WHERE email = %(email)s"""
        data = {"email": email}
        list_of_dicts = connectToMySQL(User.DB).query_db(query, data)
        pprint(list_of_dicts)
        if len(list_of_dicts) == 0:
            print("returning none")
            return None
        user = User(list_of_dicts[0])
        return user

    @classmethod
    def find_by_user_id(cls, id):
        query = """SELECT * from users WHERE id = %(id)s"""
        data = {"id": id}
        list_of_dicts = connectToMySQL(User.DB).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user

    # get one data entry
    @classmethod
    def get_one_user(cls, id):
        query = """SELECT * FROM users 
                    WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, {"id": id})
        pprint(results)
        one_entry = cls(results[0])
        return one_entry

    # get all data
    @classmethod
    def get_all_users(cls):
        query = "SELECT * from users;"
        list_of_dicts = connectToMySQL(cls.DB).query_db(query)
        pprint(list_of_dicts)

        return list_of_dicts

    @classmethod
    def delete(cls, id):
        query = """DELETE FROM users
                    WHERE ID = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, {"id": id})
        return results

    @classmethod
    def update(cls, data):
        query = """UPDATE users
                SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s
                where id = %(id)s;"""
        print(query)
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def reg_validate(form_data):
        is_valid = True  # we assume this is true
        if len(form_data["first_name"].strip()) == 0:
            flash("Please enter first name.", "register")
            is_valid = False
        elif len(form_data["first_name"].strip()) < 3:
            flash("first_name must be at least 3 characters.", "register")
            is_valid = False
        if len(form_data["last_name"].strip()) == 0:
            flash("please enter a last name.", "register")
            is_valid = False
        elif len(form_data["last_name"].strip()) < 3:
            flash("last_name must be at least 3 characters.", "register")
            is_valid = False
        if len(form_data["email"].strip()) == 0:
            flash("please enter an email.", "register")
            is_valid = False
        elif len(form_data["email"].strip()) < 3:
            flash("email must be at least 3 characters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(form_data["email"]):
            flash("Invalid email address!", "register")
            is_valid = False
        if len(form_data["password"].strip()) == 0:
            flash("Please enter a password.", "register")
            is_valid = False
        elif len(form_data["password"].strip()) < 8:
            flash("password must be at least 8 characters.", "register")
            is_valid = False
        elif form_data["password"] != form_data["confirm_password"]:
            flash("passwords do not match.", "register")
            is_valid = False
        return is_valid
        # test whether a field matches the pattern

    @staticmethod
    def login_validate(form_data):
        is_valid = True  # we assume this is true
        if len(form_data["email"].strip()) == 0:
            flash("please enter an email.", "login")
            is_valid = False
        elif len(form_data["email"].strip()) < 3:
            flash("email must be at least 3 characters.", "login")
            is_valid = False
        if not EMAIL_REGEX.match(form_data["email"]):
            flash("Invalid email address!", "login")
            is_valid = False
        if len(form_data["password"].strip()) == 0:
            flash("Please enter a password.", "login")
            is_valid = False
        elif len(form_data["password"].strip()) < 8:
            flash("password must be at least 3 characters.", "login")
            is_valid = False
        return is_valid
