from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
    user = userDB.find_one(  
      {'id': id },
      {'password': password } 
    )

    #if no matches found, show an alarm and go back to login page
    if user is None:
      print('login failed')
      return render_template('login.html')
    #if matches found, record the session so that the user can logout from the page later
    else:
      session['id'] = request.form['id']
      return redirect(url_for('main'))


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


@app.route('/main')
def main():
  i = 0
  if 'id' in session:
    id = session['id']
  diary = mongo.db.users
  output = []
  count = 0
  path_arr = []
  for item in diary.find():
    output.append({
      'title': item['title'],
      'description': item['description'],
      'profile_image_name': item['profile_image_name'],
      'date': item['date']
    })
    str = output[count]['profile_image_name']
    path='file/'+str
    path_arr.append(path)
    count += 1
  print(path_arr)
  return render_template('main.html', output = output, path = path_arr)


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

# @app.route('/file/<filename>')
# def file(filename):
#   return mongo.send_file(filename)

# @app.route('/profile/<title>')
# def profile(title):
#   user = mongo.db.users.find_one_or_404({'title' : title})
#   return f'''
#     <h1>{title}</h1>
#     <img src="{url_for('file',filename=user['profile_image_name'])}">
#   '''

@app.route('/edit', methods=['POST', 'GET'])
def edit():
  if request.method == 'GET':
    return render_template('edit.html')
  elif request.method == 'POST':
    title = request.form['title']
    description = request.form['description']

    addDiary = diaryDB.insert({
      'title': request.form['title'],
      'description': request.form['description']
    })
    return redirect(url_for('main'))


if __name__ == "__main__":
  app.run(debug=True)
