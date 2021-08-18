from app import create_app, db
from app.models import User

app = create_app()

# run 'flask shell' and now you don't have to import db and User
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

