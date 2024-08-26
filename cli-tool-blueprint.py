#!/usr/bin/env python

import psycopg2
import requests
import typer

from enum import Enum
from typing import Annotated, NamedTuple, Optional
from psycopg2._psycopg import connection
from psycopg2.extras import NamedTupleCursor
from rich.progress import track, Progress
from dataclasses import dataclass

progress = Progress()
app = typer.Typer(
    # When enabled will print the values of local variables in case of exceptions
    # Should be disabled in case the variables contain sensitive information
    pretty_exceptions_show_locals=True
)


@dataclass
class Config:
    service_url: str
    service_token: str
    db_url: str
    db_password: str
    db_port: str
    db_user: str
    db_name: str
    db_sslmode: str
    dry_run: bool
    db_conn: Optional[connection] = None


class Env(str, Enum):
    prod = "prod"
    dev = "dev"


def log(text: str):
    progress.console.log(text)


def execute_request(conf: Config):
    headers = {
        "Authorization": f"Bearer {conf.service_token}"
    }

    response = requests.get(url=conf.service_url, headers=headers)
    response.raise_for_status()

    return response.json()


def init_db_conn(conf: Config) -> connection:
    return psycopg2.connect(
        host=conf.db_url,
        port=conf.db_port,
        dbname=conf.db_name,
        sslmode=conf.db_sslmode,
        user=conf.db_user,
        password=conf.db_password,
    )


def select_query(conn: connection, query: str, params: dict) -> list[NamedTuple]:
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


def update_query(conn: connection, query: str, params: dict) -> int:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount


def process(line: str, conf: Config) -> str:
    log(f"Processing line {line}")

    response = execute_request(conf)

    select = """
    select * from device where id = %(id)s
    """

    update = """
    update device set status='ACTIVE' where id = %(id)s
    """

    device = select_query(conf.db_conn, select, {'id': line})

    if not conf.dry_run:
        update_count = update_query(conf.db_conn, update, {'id': line})
        log(f"Updated records {update_count}")

    log(f"Finished processing line {line}")

    return str(response)


@app.command()
def main(
        token: Annotated[str, typer.Option(help="Token of http API.", default=...)],
        db_user: Annotated[str, typer.Option(help="DB user.", default=...)],
        db_password: Annotated[str, typer.Option(help="DB password.", prompt=True, hide_input=True)],
        input_file: Annotated[typer.FileText, typer.Option(help="Input file to process.")] = "in.txt",
        output_file: Annotated[typer.FileTextWrite, typer.Option(help="Path to output file.")] = "out.txt",
        dry_run: Annotated[
            bool, typer.Option(help="Dry run executes the script without changing external resources.")] = False,
        environment: Annotated[Env, typer.Option(case_sensitive=False)] = Env.dev
):

    """
    Opinionated blueprint for building modern python CLI tools aiming to speedup development by providing
    basic structure and boilerplate code.
    """

    properties = {
        "dev": {
            "service_url": "http://api.open-notify.org/astros.json",
            "db_url": "localhost",
            "sslmode": "disable"
        },
        "prod": {
            "service_url": "http://api.open-notify.org/astros.json",
            "db_url": "my-prod",
            "sslmode": "require"
        }
    }

    conf = Config(
        service_url=properties[environment]["service_url"],
        service_token=token,
        db_url=properties[environment]["db_url"],
        db_password=db_password,
        db_port="5432",
        db_user=db_user,
        db_name="postgres",
        db_sslmode=properties[environment]["sslmode"],
        dry_run=dry_run
    )

    conf.db_conn = init_db_conn(conf)

    log("Initialization finished.")

    raise ValueError

    for line in track(input_file.readlines()):
        result = process(line, conf)
        output_file.write(result)
        output_file.write("\n")

    conf.db_conn.close()

    log("Processing finished.")


if __name__ == "__main__":
    app()
