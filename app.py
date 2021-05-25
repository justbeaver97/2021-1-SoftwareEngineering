from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'software_engineering'

cluster = MongoClient(
  "mongodb+srv://YeHyunSuh:Tjdmdgka55!@cluster0.qbm6b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["software_engineering"]
taskDB = database["tasks"]
userDB = database["user"]

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
      addUser = userDB.insert({
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
  if 'id' in session:
    id = session['id']
    return render_template('main.html')


if __name__ == "__main__":
  app.run(debug=True)
