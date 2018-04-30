from rmon.app import create_app
from rmon.models import db 

app = create_app()


@app.cli.command()
def init_db():
    """
    initialize database
    """
    print('sqlite3 database file is {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
    db.create_all()
