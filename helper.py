
#%% Inspect database

import sqlite3
import pandas as pd

def to_df():
    db = sqlite3.connect('flaskblog/site.db')
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    dataframes = {}
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        dataframes[table_name] = table
    cursor.close()
    db.close()
    return dataframes

dataframes = to_df()

#%% Understanding request

from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask('__main__')

@app.route('/home', methods=['GET', 'POST'])
def home_func():
    print('i am inside home')
    print(request.form)
    return 'home'

@app.route('/about/<x>', methods=['GET', 'POST'])
def about(x):
    print('i am inside about')
    print(request.method)
    print(request.form)
    print(request.args)
    print(request.data)
    print(x)
    form_template =f'''
    <form action="{url_for('home_func')}" method="post">
	<p>Name:</p>
	<p><input type="text" name="nm1" id="id1" autocomplete="off"/></p>
    <p><input type="text" name="nm2" id="id2"/></p>
	<input type="submit" value="submit button"/>
    
    </form>

    '''
    print(request.form.get('nm1'))
    print(request.form.get('vehicle'))
    
    return form_template

if __name__ == '__main__':
    app.run(debug=True)
    

#%% SQL Alchamey

#Creating data through shell command
#python
#from app import db
#db.create_all()
#from app import User, POST
#user_1 = User(username='gaurav', email='gaurav@bloag.com', password='password')
#user_2 = User(username='gaurav2', email='gaurav2@bloag.com', password='password2')
#db.session.add(user_1)
#db.session.add(user_2)
#db.session.commit()
# User.query.all()[0]
# User.query.first()
# user = User.query.filter_by(username='gaurav1').all()[0]
# user.id
# user.posts
# user = User.query.get(1)
# post_1 = Post(title='Blog 1', content='First post Content', user_id=user.id)
# post_2 = Post(title='Blog 2', content='First post Content2', user_id=user.id)
# db.session.add(post_1)
# user.posts
# post = Post.query.first()
# post.user_id
# post.author, User.query.get(post.user_id) #same thing
# db.drop_all()
# db.create_all()