import os

# --- CRITICAL FIX: Kill the zombie variable before anything else loads ---
if 'CELERY_RESULT_BACKEND' in os.environ:
    del os.environ['CELERY_RESULT_BACKEND']
# -----------------------------------------------------------------------

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Post, Message, Notification

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification}
