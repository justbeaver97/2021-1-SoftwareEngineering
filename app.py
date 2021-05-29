from flask import Flask, render_template, request, redirect, url_for, session, abort
from pymongo import MongoClient
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import os
import datetime 

app = Flask(__name__)
app.secret_key = 'software_engineering'

cluster = MongoClient(
  "mongodb+srv://YeHyunSuh:Tjdmdgka55!@cluster0.qbm6b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["software_engineering"]
diaryDB = database["diary"]
userDB = database["user"]

app.config['MONGO_URI']='mongodb+srv://YeHyunSuh:Tjdmdgka55!@cluster0.qbm6b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)

#Route
@app.route('/')
def root():
  return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    id = request.form['id']
    password = request.form['password']   

    #Find the data that matches the id and password
    user = userDB.find(  
      {'id': id }
    ) 
    
    for item in user:
      userName = item['name']

    #if no matches found, show an alarm and go back to login page
    if user is None:
      return render_template('login.html')
    #if matches found, record the session so that the user can logout from the page later
    else:
      session['id'] = request.form['id']
      return redirect(url_for('main', userName=userName))


@app.route('/logout')
def logout():
  # remove the username from the session if it is there
  session.pop('id', None)
  return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')
  elif request.method == 'POST':
    id = request.form['id']
    password = request.form['password']    
    name = request.form['name']
    email = request.form['email']
    
    addUser = userDB.find_one( 
      {'id': id }
    )
    if addUser is None:
      userDB.insert({
        'id': request.form['id'],
        'password': request.form['password'],
        'name': request.form['name'],
        'email': request.form['email']
      })
      return redirect(url_for('login'))
    else:
      print('the id already exists')
      return redirect(url_for('signup'))


#need to show the diaries in newly added order
@app.route('/main', methods=['GET'])
def main():
  userName = request.args.get('userName')
  if userName is None:
    print('path error')
    return abort(401)
  else:
    if request.method == 'GET':
      if 'id' in session:
        id = session['id']
      diary = mongo.db.users 
      output = []

      for item in diary.find():
        output.append({
          'title': item['title'],
          'description': item['description'],
          'profile_image_name': item['profile_image_name'],
          'date': item['date']
        })
        output.reverse()

      return render_template('main.html', output=output, id=id, userName=userName)
  


@app.route('/post', methods=['POST', 'GET'])
def post():
  if request.method == 'GET':
    return render_template('post.html')
  elif request.method == 'POST':
    title = request.form['title']
    description = request.form['description']
    f = request.files['file']

    if not os.path.exists("./data"):
      os.makedirs('./data')
    filename = secure_filename(f.filename)

    mongo.save_file(f.filename, f)
    mongo.db.users.insert_one({
      'title': request.form['title'],
      'description': request.form['description'],      
      'profile_image_name': f.filename,
      'date': datetime.datetime.now()
    })
    # diaryDB.insert_one({
    #   'title': request.form['title'],
    #   'description': request.form['description'],
    #   'filename': f.filename
    # })
    return redirect(url_for('main'))
 
@app.route('/<filename>')
def file(filename):
  return mongo.send_file(filename)

@app.route('/profile/<title>')
def profile(title):
  user = mongo.db.users.find_one_or_404({'title' : title})
  return f'''
    <h1>title: {title}</h1>
    <p>description: {user['description']}<p>
    <img src="{url_for('file',filename=user['profile_image_name'])}" width="200">
  '''

@app.route('/edit', methods=['POST', 'GET'])
def edit():
  if request.method == 'GET':
    return render_template('edit.html')
  elif request.method == 'POST':
    title = request.form['title']
    description = request.form['description']
    f = request.files['file']

    if not os.path.exists("./data"):
      os.makedirs('./data')
    filename = secure_filename(f.filename)

    mongo.save_file(f.filename, f)
    mongo.db.users.update_one({
      'title': request.form['title'],
      'description': request.form['description'],
      'profile_image_name': f.filename
    })
    # insert_one({
    #   'title': request.form['title'],
    #   'description': request.form['description'],      
    #   'profile_image_name': f.filename,
    #   'date': datetime.datetime.now()
    # })
    return redirect(url_for('main'))

@app.route('/delete', methods=['POST'])
def delete():
  if request.method == 'POST':
    title = request.form['title']
    print(title)
    delete_diary = mongo.db.users
    delete_diary.delete_one({
      'title':request.form['title']
    })
    return redirect(url_for('main'))


if __name__ == "__main__":
  app.run(debug=True)
