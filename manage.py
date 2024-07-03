import os
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Posts

app = create_app('development' if os.getenv('FLASK_CONFIG') is None else os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'Posts': Posts}

if __name__ == '__main__':
    app.run()
