import MySQLdb.cursors
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flask_restapi"

mysql = MySQL(app)

@app.get('/')
def hello():

    return jsonify([
        {"message": "Hello world...!"}
    ]), 200

@app.post("/api/users")
def create_user():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = sha256_crypt.encrypt(data["password"])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username =%s", (username,))
    account = cursor.fetchone()
    if(account):
        return jsonify({"error" : "Account already exist"}), 403
    else:
   
        cursor.execute("INSERT INTO users (username, email, pass) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cursor.close()
        message = "Created "+username+" successfully"
        return jsonify(
            {"message": message}
        ), 201
    
@app.put("/api/users/<int:id>")
def update_user(id):
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = sha256_crypt.encrypt(data["password"])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    account = cursor.fetchone()

    if(account):
        cursor.execute("UPDATE users SET username =%s,\
                email =%s, pass=%s WHERE id =%s",\
                (username, email, password, id))
        mysql.connection.commit()
        cursor.close()
        message = "Updated "+username+" successfully"
        return jsonify(
                {"message": message}
            ), 200
    else:
        cursor.close()
        message = "User id "+id+" not found"
        return jsonify(
                {"error": message}
            ), 404
    
@app.delete("/api/users/<int:id>")
def delete_user(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id =%s", (id,))
    account = cursor.fetchone()

    if(account):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Delete user data successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app.get("/api/users/<int:id>")
def single_user(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    account = cursor.fetchone()
    cursor.close()

    return jsonify(account), 200

@app.get("/api/users")
def multiple_user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    accounts = cursor.fetchall()
    cursor.close()
    
    return jsonify(accounts), 200

if __name__ == '__main__':
    app.run(debug=True)