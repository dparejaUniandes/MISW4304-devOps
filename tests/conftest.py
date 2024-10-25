import pytest

from application import create_flask_app
from models import db


@pytest.fixture(autouse=True)
def app():
    app = create_flask_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///score_test.db'
    })
    db.init_app(app)
    db.create_all()

    yield app
    db.session.rollback()
    db.session.close()
    db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
