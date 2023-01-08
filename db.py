from dataclasses import dataclass
import pathlib
import sqlite3
from typing import Union

import click
from flask import current_app
from flask import g


class DatabaseConnection:
    def __init__(self, location: str) -> None:
        self.connection = sqlite3.connect(
            str(location), detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.connection.row_factory = sqlite3.Row

    def __del__(self):
        self.close()

    def close(self):
        self.connection.close()

    @property
    def table_name(self):
        raise NotImplementedError("Subclasses must implement this")

    def convert_key_values(separator: str, **kwargs):
        return separator.join(
            map(lambda arg: f'{arg[0]}=\'{arg[1]}\'', kwargs.items()))

    def get(self, **kwargs):
        key_values = DatabaseConnection.convert_key_values(
            separator=' AND ', **kwargs)

        result_row = self.connection.execute(
            f"SELECT * FROM {self.table_name} WHERE {key_values}"
        ).fetchone()
        return result_row

    def _set(self, **kwargs):
        keys = ', '.join(map(str, kwargs.keys()))
        values = ', '.join(
            map(lambda value: f"'{str(value)}'", kwargs.values()))

        self.connection.execute(
            f"INSERT INTO {self.table_name} ({keys}) VALUES ({values})",
        )
        self.connection.commit()
        return self.get(**kwargs)['user_id']

    def update(self, user_id: int, **kwargs):
        key_values = DatabaseConnection.convert_key_values(
            separator=', ', **kwargs)

        self.connection.execute(
            f"UPDATE {self.table_name} SET {key_values} WHERE user_id = {str(user_id)}",
        )
        self.connection.commit()
        return user_id

    def set(self, **kwargs):
        raise NotImplementedError("Subclasses must implement this")


class UserDatabaseConnection(DatabaseConnection):

    @property
    def table_name(self):
        return "user"

    def set(self, username: str, password: str):
        return super()._set(username=username, password=password)


class UserdataDatabaseConnection(DatabaseConnection):

    @property
    def table_name(self):
        return "user_data"

    def set(self, user_id: int):
        return super()._set(user_id=user_id)


class Database:
    def __init__(self, location: str) -> None:
        self.user_db = UserDatabaseConnection(location)
        self.user_data_db = UserdataDatabaseConnection(location)

    def init(self, schema: str = "schema.sql"):
        with open(schema) as f:
            self.user_db.connection.executescript(f.read())


def get_db():
    return Database(current_app.config["DATABASE"])


def init_db():
    get_db().init("schema.sql")


@ click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_db_command)


if __name__ == '__main__':
    path = "test.sqlite"

    init_db(path)
    db = UserDatabaseConnection(path)
