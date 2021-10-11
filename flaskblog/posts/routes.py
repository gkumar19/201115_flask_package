from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flaskblog.posts.forms import PostForm
from flaskblog import db
from flaskblog.models import Post, User
from flask_login import current_user, login_required
posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    print(request.form)
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('You have successfully Posted', 'success')
        return redirect(url_for("main.home"))

    return render_template('create_post.html', form=form, title="new post", legend="New Post")

@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    author = User.query.get(post.user_id)
    return render_template("post.html", title=post.title, post=post, author=author)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != User.query.get(post.user_id):
        abort(403)
    form = PostForm()
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You have successfully Updated', 'success')
        return redirect(url_for("posts.post", post_id=post_id))
    return render_template("create_post.html", form=form, title="update post", legend="Update Post")

@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != User.query.get(post.user_id):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You have successfully Deleted', 'success')
    return redirect(url_for("main.home"))