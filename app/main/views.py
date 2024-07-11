from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from . import main  # Ensure the correct import path
from .forms import EditProfile, WriteForm, CommentForm  # Import CommentForm
from ..models import User, Posts, Comment  # Import Comment model
from ..requests import get_quotes




@main.route('/') 
def index():
    # quotes = get_quotes()
    posts = Posts.query.all()

    # blogs = [
    #     {
    #         'title':
    #     }
    # ]

    return render_template('index.html', posts = posts)


@main.route('/publish/new', methods=['GET','POST'])
@login_required
def write():
    form = WriteForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.story.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.account'))
    
    # Query all posts, including those by other users
    posts = Posts.query.all()
    return render_template('write.html', form=form, posts=posts)

@main.route('/account')
@login_required
def account():
    quotes = get_quotes()
    # Filter posts by current user
    posts = Posts.query.filter_by(author=current_user).all()
    image = current_user.image_url
    return render_template('account.html', quotes=quotes, posts=posts, image=image)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, fn_ext = os.path.splitext(form_picture.filename)
    picture_fn = fn_ext
    pic_full_path = os.path.join('app/static/images', 'profile.jpg')
    form_picture.save(pic_full_path)
    return picture_fn


@main.route('/profile', methods = ['GET','POST'])
def profile():
    form = EditProfile()
    image_file = url_for('static', filename = 'images/'+ 'profile.jpg')
    posts = Posts.query.all()
    user = User.query.filter_by(username = current_user.username).first
    if form.validate_on_submit():
        if form.picture_upload.data:
            picture_file = save_picture(form.picture_upload.data)
            current_user.image_url = picture_file
        current_user.username = form.user.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Acount updated successfully', 'success')

    form.user.data = current_user.username
    form.bio.data = current_user.bio

    return render_template('userprof.html', form = form, image = image_file,user = user, posts = posts)


@main.route('/post/<int:post_id>')
def post(post_id):
    posts = Posts.query.get_or_404(post_id)
    return render_template('post.html', posts = posts)


@main.route('/post/<int:post_id>/delete')
def delete(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.account') )


@main.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = Posts.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment_content = form.comment_content.data

        if not comment_content:
            flash('Comment cannot be empty.', 'danger')
            return redirect(url_for('main.account', post_id=post.id))

        comment = Comment(content=comment_content, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
        return redirect(url_for('main.post', post_id=post.id))

    return render_template('post.html', form=form, post=post)




@main.route('/read')
def read():
    posts = Posts.query.all()
    return render_template('read.html', posts=posts)