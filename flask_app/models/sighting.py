from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import pprint
pp = pprint.PrettyPrinter(indent=4)

class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.sighting_date = data['sighting_date']
        self.num_sasquatch = data['num_sasquatch']

        self.creator_first_name = data['first_name']
        self.creator_last_name = data['last_name']
        self.creator_id = data['user_id']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = (
            "INSERT INTO sightings "
            "(location, description, sighting_date, num_sasquatch, created_at, updated_at, user_id) "
            "VALUES (%(location)s, %(description)s, %(sighting_date)s, %(num_sasquatch)s, NOW(), NOW(), %(user_id)s );"
        )
        connectToMySQL('sasquatch_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = (
            "UPDATE sightings "
            "SET location=%(location)s, description=%(description)s, "
            "sighting_date=%(sighting_date)s, num_sasquatch=%(num_sasquatch)s, "
            "updated_at=NOW();"
        )
        return connectToMySQL('sasquatch_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = (
            "DELETE FROM sightings "
            "WHERE id = %(sighting_id)s;"
        )
        return connectToMySQL('sasquatch_schema').query_db(query, data)


    @classmethod
    def get_one(cls, data):
        query = (
            "SELECT * FROM sightings WHERE id = %(sighting_id)s; "
        )
        return connectToMySQL('sasquatch_schema').query_db(query, data)
    
    @classmethod
    def get_one_with_creator(cls, data):
        query = (
            "SELECT * FROM sightings "
            "JOIN users ON users.id = sightings.user_id "
            "WHERE sightings.id = %(sighting_id)s;"
        )
        results = connectToMySQL('sasquatch_schema').query_db(query, data)
        # print(results[0])
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = (
            "SELECT * FROM sightings "
            "JOIN users ON users.id = sightings.user_id "
        )
        results = connectToMySQL('sasquatch_schema').query_db(query)
        sightings = []

        for sighting in results:
            pp.pprint(sighting)
            sightings.append( cls(sighting) )
        return sightings

    @classmethod
    def get_skeptics(cls, data):
        query = (
            "SELECT first_name, last_name, users.id FROM sightings "
            "JOIN skeptics ON sightings.id = skeptics.sighting_id "
            "LEFT JOIN users ON users.id = skeptics.user_id "
            "WHERE sightings.id = %(sighting_id)s;"
        )
        results = connectToMySQL('sasquatch_schema').query_db(query, data)
        pp.pprint(results)
        return results

    @classmethod
    def skeptic(cls, data):
        query = (
            "INSERT INTO skeptics (sighting_id, user_id) "
            "VALUES (%(sighting_id)s, %(user_id)s);"
        )
        connectToMySQL('sasquatch_schema').query_db(query, data)

    @classmethod
    def believe(cls, data):
        query = (
            "DELETE FROM skeptics "
            "WHERE sighting_id=%(sighting_id)s "
            "AND user_id=%(user_id)s;"
        )
        connectToMySQL('sasquatch_schema').query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['location']) < 3:
            flash("Location must be longer than 3 chars")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be longer than 3 chars")
            is_valid = False
        if not data['sighting_date']:
            flash("Date of sighting must be provided")
            is_valid = False
        if not data['num_sasquatch'] or int(data['num_sasquatch']) < 1:
            flash("Number of sasquatch must be greater than 0")
            is_valid = False
        return is_valid