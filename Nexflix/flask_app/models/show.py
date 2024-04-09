from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Show:
    DB = "Nexflix"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.title = db_data["title"]
        self.network = db_data["network"]
        self.comments = db_data["comments"]
        self.release_date = db_data["release_date"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
        self.user_id = db_data["user_id"]

        self.user = None

    @classmethod
    def get_all_shows(cls):
        query = """SELECT * FROM shows;"""
        list_of_dicts = connectToMySQL(cls.DB).query_db(query)
        return list_of_dicts

    @classmethod
    def show_by_id(cls, id):
        id = {"id": id}
        query = """SELECT * FROM shows
                    WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, id)
        return results

    @classmethod
    def find_all_with_users(cls):
        # query to get all the shows data and associated users
        query = """SELECT * FROM shows  JOIN users ON
        shows.user_id = users.id;"""

        # running the query in the db to get our data
        list_of_dicts = connectToMySQL(cls.DB).query_db(query)
        print("\n\n\n\n\nresult from db ---->", list_of_dicts)
        user_with_shows = []
        if list_of_dicts is not ():
            # creating an empty array to hold all the shows and associated users

            # loop through the data we got back from db to parse it to be mroe organized. "CLEAN DATA"
            for each_dict in list_of_dicts:
                # because we are dealing with two tables we need two object
                # this will handle the first table, SHOW
                show_object = cls(each_dict)

                # prepping the user data because ID, created_at, updated_at have similar columns as show table therefore we need to use modified keys.
                user_data = {
                    "id": each_dict["users.id"],
                    "first_name": each_dict["first_name"],
                    "last_name": each_dict["last_name"],
                    "email": each_dict["email"],
                    "password": each_dict["password"],
                    "created_at": each_dict["users.created_at"],
                    "updated_at": each_dict["users.updated_at"],
                }

                # creating a User object and assigning it to the user attribute. This was declared in the constructor, line 17. This handles the second table.
                show_object.user = User(user_data)

                # Adding the associated data to the array to be
                user_with_shows.append(show_object)
                print(
                    "\n\n\n\nline 54 in show model --------------->",
                    user_with_shows[0].user,
                )
            return user_with_shows
        else:
            return user_with_shows

    @classmethod
    def add_show(cls, data):
        query = """INSERT INTO shows (title, network, comments,user_id,release_date) 
                VALUES (%(title)s, %(network)s, %(comments)s,%(user_id)s,%(release_date)s);"""
        print(query)
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def shows_validate(form_data):
        is_valid = True  # we assume this is true
        if len(form_data["title"].strip()) == 0:
            flash("please enter a show title.")
            is_valid = False
        elif len(form_data["title"].strip()) < 3:
            flash("Title  must be at least 3 characters.")
            is_valid = False
        if len(form_data["network"].strip()) == 0:
            flash("please enter a network.")
            is_valid = False
        elif len(form_data["network"].strip()) < 5:
            flash(" network must be at least 5 characters.")
            is_valid = False
        if len(form_data["comments"].strip()) == 0:
            flash("Please enter comments for the show.")
            is_valid = False
        elif len(form_data["comments"].strip()) < 8:
            flash(" comments must be at least 8 characters.")
            is_valid = False
        if len(form_data["release_date"].strip()) == 0:
            flash("Please enter a date.")
            is_valid = False
        return is_valid

    @classmethod
    def count_by_title(cls, title):
        query = """
        SELECT COUNT(title) as "count"
        from shows
        WHERE title = %(title)s
    """
        data = {"title": title}
        list_of_dicts = connectToMySQL(Show.DB).query_db(query, data)
        return list_of_dicts[0]["count"]

    @classmethod
    def update(cls, data):
        query = """UPDATE shows
                SET title=%(title)s,network=%(network)s,comments=%(comments)s,release_date=%(release_date)s
                where id = %(show_id)s;"""
        print(query)
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_one_show(cls, id):
        query = """SELECT * FROM shows 
                WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, {"id": id})
        return cls(results[0])

    @classmethod
    def find_one_with_user(cls, show_id):
        # query to get one the SHOWS data and associated user
        query = """SELECT * FROM shows  JOIN users ON
        shows.user_id = users.id WHERE shows.id = %(show_id)s;"""

        data = {"show_id": show_id}
        # running the query in the db to get our data
        list_of_dicts = connectToMySQL(cls.DB).query_db(query, data)
        print("\n\n\n\n\nresult from db ---->", list_of_dicts)

        show_object = cls(list_of_dicts[0])

        # prepping the user data because ID, created_at, updated_at have similar columns as show table therefore we need to use modified keys.
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }

        # creating a User object and assigning it to the user attribute. This was declared in the constructor, line 17. This handles the second table.
        show_object.user = User(user_data)

        # Adding the associated data to the array to be
        print("\n\n\n\nline 54 in shows model --------------->", show_object.user)
        return show_object

    @classmethod
    def delete(cls, id):
        query = """DELETE from shows 
                WHERE id  = %(id)s;"""
        connectToMySQL(cls.DB).query_db(query, {"id": id})
        return
