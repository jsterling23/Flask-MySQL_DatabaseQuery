from flask import Flask, session, render_template, redirect, request, flash
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = 'secretKey'
mysql = MySQLConnector(app,'email')

@app.route('/')
def index():

    query = 'SELECT * FROM users'
    friends = mysql.query_db(query)


    return render_template('index.html', all_friends=friends)








@app.route('/friends', methods=['POST'])
def create():

    session['first_name'] =  request.form['first_name']
    session['last_name'] =  request.form['last_name']
    session['email'] =  request.form['email']


    data = {
        'first_name' : session['first_name'],
        'last_name' : session['last_name'],
        'email' : session['email']
    }

    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW() )"

    mysql.query_db(query, data)


    return redirect('/')


# @app.route('/friends/<id>')
# def show(id):
#     # Write query to select specific user by id. At every point where
#     # we want to insert data, we write ":" and variable name.
#     query = "SELECT * FROM users WHERE id = :specific_id"
#     # Then define a dictionary with key that matches :variable_name in query.
#     data = {'specific_id': id}
#     # Run query with inserted data.
#     friends = mysql.query_db(query, data)
#
#     print friends
#     # Friends should be a list with a single object,
#     # so we pass the value at [0] to our template under alias one_friend.
#     return render_template('test.html', one_friend=friends[0])




@app.route('/friends/<id>/edit')
def edit(id):

    query = "SELECT * FROM users WHERE id = :specific_id"

    data = {'specific_id': id}

    friend = mysql.query_db(query, data)


    return render_template('edit.html', friend=friend)


@app.route('/friends/<id>', methods=['POST'])
def update(id):

    query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"

    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'email': request.form['email'],
             'id': id
           }
    mysql.query_db(query, data)

    return redirect('/')


@app.route('/friends/<id>/delete')
def destroy(id):

    query = "DELETE FROM users WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)

    return redirect('/')





app.run(debug=True)
