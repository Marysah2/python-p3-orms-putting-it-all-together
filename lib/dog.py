# lib/dog.py

import sqlite3

CONN = sqlite3.connect(':memory:')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        """ Create a table called dogs if it doesn't exist """
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the dogs table if it exists """
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Save the dog instance to the database. If it has an id, update; else insert. """
        if self.id is None:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            # Get the assigned id
            self.id = CURSOR.lastrowid
        else:
            sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()
        return self

    @classmethod
    def create(cls, name, breed):
        """ Create a new dog, save it, and return the instance """
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        """ Given a row from the database, return a Dog instance """
        dog = cls(row[1], row[2])  # name is index 1, breed is index 2
        dog.id = row[0]            # id is index 0
        return dog

    @classmethod
    def get_all(cls):
        """ Return a list of all Dog instances in the database """
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        """ Return a Dog instance with the given name, or None """
        sql = "SELECT * FROM dogs WHERE name = ? LIMIT 1"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        """ Return a Dog instance with the given id, or None """
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        """ Find a dog by name and breed, or create it if it doesn't exist """
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1"
        CURSOR.execute(sql, (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return cls.create(name, breed)

    def update(self):
        """ Update the dog's record in the database to match current attributes """
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()