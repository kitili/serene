from flask import render_template, redirect,url_for,request,flash
from werkzeug.security import generate_password_hash,check_password_hash
from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User,Posts
from .. import db,bcrypt
from ..email import send_mail
from flask_login import login_user,current_user, logout_user,login_required


@auth.route('/register', methods = ['GET','POST'])
def register():
  if current_user.is_authenticated:
      return redirect('main.index')
  form = RegisterForm()
  if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(username = form.username.data, email = form.email.data, password = hashed_password)
      db.session.add(user)
      db.session.commit()
      #send_mail("Welcome to Shrededd","welcome_user",user.email,user=user)
      #flash("You can now login")
      return redirect('login')
  return render_template('register.html', form=form)



@auth.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
      return redirect('main.index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
                return redirect(next)
        
            return redirect(url_for('main.account'))
        flash("invalid username or password")

    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
      logout_user()
      return render_template('index.html')














    