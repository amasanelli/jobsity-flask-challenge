# encoding: utf-8

import click
from flask.cli import with_appcontext
from dotenv import load_dotenv


@click.group()
def cli():
    """Main entry point"""
    pass


@cli.command("init")
@with_appcontext
def init():
    """Create test users"""
    from api_service.extensions import db
    from api_service.models import User

    click.echo("create admin user")
    user = User(username="admin", email="admin@mail.com", password="admin", active=True, role='ADMIN')
    db.session.add(user)
    click.echo("create regular user")
    user = User(username="johndoe", email="johndoe@mail.com", password="john", active=True, role='USER')
    db.session.commit()
    click.echo("users created")


if __name__ == "__main__":
    load_dotenv('.flaskenv')
    cli()
