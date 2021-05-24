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
        {'id': id},
        {'password': password}
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
  
@app.route('/signup', methods=['POST','GET'])
def signup():
      if request.method == 'GET':
            return render_template('signup.html')
      elif request.method == 'POST':
        user = userDB.find_one(
          {'id': id}
        )  
        if user is None: 
          user = userDB.insert({
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


# #Routes
# @app.route('/login', methods=['POST','GET'])
# def login():
#     if request.method == 'GET':
#       return render_template('login.html')
#     else:
#       userid = request.json['userid']
#       password = request.json['password']

#       user = userDB.find_one(
#           { 'userid': userid },
#           { 'password': password }
#       )

#       if user is None:
#           return print("login failed")
#       else:
#           return render_template("main.html")

# @app.route('/register', methods=['POST'])
# def createUser():
#   id = userDB.insert({
#     'userid': request.json['userid'],
#     'password': request.json['password']
#   })
#   return jsonify(str(ObjectId(id)))

# @app.route('/tasks', methods=['POST'])
# def createTask():
#   id = taskDB.insert({
#     'title': request.json['title'],
#     'content': request.json['content'],
#     'picture_url': request.json['picture_url']
#   })
#   return jsonify(str(ObjectId(id)))

# @app.route('/tasks', methods=['GET'])
# def getTasks():
#   tasks = []
#   for doc in taskDB.find():
#     tasks.append({
#       '_id': str(ObjectId(doc['_id'])),
#       'title': doc['title'],
#       'content': doc['content'],
#       'picture_url': doc['picture_url']
#     })
#   return jsonify(tasks)

# @app.route('/task/<id>', methods=['GET'])
# def getTask(id):
#   task = taskDB.find_one({'_id': ObjectId(id)})
#   return jsonify({
#     '_id': str(ObjectId(task['_id'])),
#     'title': task['title'],
#     'content': task['content'],
#     'picture_url': task['picture_url']
#   })

# @app.route('/tasks/<id>', methods=['DELETE'])
# def deleteTask(id):
#   taskDB.delete_one({'_id': ObjectId(id)})
#   return jsonify({'msg': 'task deleted'})

# @app.route('/tasks/<id>', methods=['PUT'])
# def editTask(id):
#   taskDB.update_one({'_id': ObjectId(id)}, {'$set': {
#     'title': request.json['title'],
#     'content': request.json['content'],
#     'picture_url': request.json['picture_url']
#   }})
#   return jsonify({'msg': 'task updated'})

# if __name__ == "__main__":
#     app.run(debug=True)
