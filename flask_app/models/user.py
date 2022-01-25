from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = (
            "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) "
            "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        )
        return connectToMySQL('sasquatch_schema').query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return connectToMySQL("sasquatch_schema").query_db(query,data)
    
    @classmethod
    def get_others(cls, data):
        query = "SELECT * FROM users WHERE id <> %(id)s;"
        return connectToMySQL("sasquatch_schema").query_db(query,data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("sasquatch_schema").query_db(query,data)

        if not len(result):
            return False
        return cls(result[0])

    @staticmethod
    def validate_register(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash("First name must be longer than 3 chars")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be longer than 3 chars")
            is_valid = False
        
        # EMAIL REGEX CHECK
        if not EMAIL_REGEX.match(data['email']):
            flash("INVALID EMAIL ADDRESS")
            is_valid = False

        # CHECK IF EMAIL EXISTS IN DB
        query = "SELECT * FROM users WHERE email = %(email)s"
        email_exists = connectToMySQL('sasquatch_schema').query_db(query, data)
        print(email_exists)
        if email_exists:
            flash("Email exsits")
            is_valid = False

        if not PASSWORD_REGEX.match(data['password']):
            flash("Minimum eight characters, at least one letter, one number and one special character")
            is_valid = False
        
        if data['password'] != data['confirm_password']:
            flash("Password and Confirm Password must match")
            is_valid = False

        return is_valid