""" This module contains the model for the widgets table """

from typing import TypeVar

# @todo revisit this to ensure it is the proper way to type hint
SQLite = TypeVar("SQLite")

class ModelWidget():
    """ Defines CRUD operations for Widgets Model """

    def __init__(self, db_conn: SQLite) -> None:
        """ Constructor with dependency injection """
        self.db_conn = db_conn

        self.fields=("id", "name", "parts", "date_created", "date_updated")

        self.validation = {
            "id": ("int", ),
            "name": ("length", 64),
            "parts": ("int", )
        }

    def validate(self, values):
        """ Perform basic validation """
        valid = True
        messages = []
        for key, value in values.items():
            if key in self.validation:
                if self.validation[key][0] == "int" and not value.isdigit():
                    valid = False
                    messages.append(f"{key} is not an integer")
                elif self.validation[key][0] == "length":
                    maxlength = self.validation[key][1]
                    if len(value) > maxlength:
                        valid = False
                        messages.append(f"{key} is longer than {maxlength}")

        return {"success": valid, "messages": messages}

    def create_table(self) -> None:
        """ Create the table schema and triggers """
        self.db_conn.execute('''
            pragma encoding = 'UTF-8';
        ''', ())

        self.db_conn.execute('''
            CREATE TABLE widgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                parts INTEGER,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''', ())

        self.db_conn.execute('''
            CREATE TRIGGER widget_updated_trigger AFTER UPDATE ON widgets
            BEGIN
                UPDATE widgets SET date_updated = datetime('now') WHERE id = NEW.id;
            END;
        ''', ())

    def describe(self) -> None:
        """ Output SQLite metadata to console so we can view what was created on init """
        result = self.db_conn.select("SELECT * FROM sqlite_master", ())
        print(result)

    def insert(self, name: str, parts: int) -> int:
        """ Insert a record """
        rowid = self.db_conn.insert(
            "INSERT INTO widgets (name, parts) VALUES (?, ?)",
            (name, parts)
        )
        return rowid

    def select_all(self) -> list:
        """ Select all records in table """
        results = self.db_conn.select("SELECT * FROM widgets", ())

        return_results = [dict(zip(self.fields, row)) for row in results]

        return return_results

    def select_one(self, id_val: int) -> list:
        """ Select one record by id """
        results = self.db_conn.select("SELECT * FROM widgets WHERE id = ?", (id_val,))
        return_results = dict(zip(self.fields, results[0]))
        return return_results

    # @todo handle if only name or parts number is updated
    def update(self, id_val: int, name: str, parts: int) -> int:
        """ Update a record by id """
        return self.db_conn.execute(
            "UPDATE widgets SET name = ?, parts = ? WHERE id = ?",
            (name, parts, id_val)
        )

    def delete(self, id_val: int) -> int:
        """ Delete a record by id """
        return self.db_conn.execute("DELETE from widgets WHERE id = ?", (id_val,))
