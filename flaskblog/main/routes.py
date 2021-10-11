from flask import Blueprint, render_template, request
from flaskblog.models import Post, User

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=2)
    page_nums = [page_num for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)]
    posts = [post for post in posts.items]
    authors = [User.query.get(int(post.user_id)) for post in posts]
    posts_authors_zip = [(i, j) for i, j in zip(posts, authors)]
    return render_template('home.html', title='home', posts_authors_zip=posts_authors_zip, page_nums=page_nums, page=page)

@main.route('/about')
def about():
    return render_template('about.html', title='about')