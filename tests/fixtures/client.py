import os
import tempfile

import pytest

from app import app, db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///" + db_path,
        JWT_SECRET_KEY="super-secret",
    )

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
