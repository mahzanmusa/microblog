import sys
import time
import json
import sqlalchemy as sa
from app import create_app, db
from celery import shared_task, current_task
from app.models import Task, User, Post
from flask import render_template
from app.email import send_email

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    # In Celery, we check if a request is active
    if not current_task:
        return
    
    # 1. Update Celery's internal state (replaces job.meta)
    # This stores 'progress' in the backend so you can fetch it via AsyncResult
    current_task.update_state(state='PROGRESS', meta={'progress': progress})

    # 2. Update your SQL Database (Same logic as RQ)
    task_id = current_task.request.id
    task = db.session.get(Task, task_id)

    if task:
        task.user.add_notification('task_progress', {'task_id': task_id, 'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id):
    try:
        user = db.session.get(User, user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = db.session.scalar(sa.select(sa.func.count()).select_from(user.posts.select().subquery()))
        for post in db.session.scalars(user.posts.select().order_by(Post.timestamp.asc())):
            data.append({'body': post.body, 'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_posts)

        # send email with data to user
        send_email(
            '[Microblog] Your blog posts',
            sender=app.config['ADMINS'][0], recipients=[user.email],
            text_body=render_template('email/export_posts.txt', user=user),
            html_body=render_template('email/export_posts.html', user=user),
            attachments=[('posts.json', 'application/json',
                          json.dumps({'posts': data}, indent=4))],
            sync=True)
    except Exception:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
         _set_task_progress(100)