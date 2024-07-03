from flask_mail import Message
from . import mail
from flask import render_template


def send_mail(subject, template, to, **kwags):
    sender = 'serene@gmail.com'
    email = Message(subject, sender = sender,recipients=[to])
    email.body = render_template(template +'.txt', **kwags)
    email.html = render_template(template +'.html', **kwags)
    mail.send(email)