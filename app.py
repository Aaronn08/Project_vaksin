from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    database="project",
    password="")

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = cnx.cursor()
    query = ("select * from user where username = %s and password = %s")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('admin'))
    else:
        return f"salah username atau password!!!"
  

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route('/admin')
def admin():
    if session.get("user"):
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/simpan', methods=["POST", "GET"])
def simpan():
    jenis_vaksin = request.form["jenis_vaksin"] 
    umur = request.form["umur"]
    lokasi = request.form["lokasi"]
    tahun = request.form["tahun"]
    
    query = "INSERT INTO vaksin (id_vaksin, jenis_vaksin, umur, lokasi, tahun) VALUES (%s, %s, %s, %s, %s)"
    data = ("", jenis_vaksin, umur, lokasi, tahun)
    
    cur = cnx.cursor()
    cur.execute(query, data)
    cnx.commit()
    cur.close()
    
    return redirect('/tampil')

@app.route('/tampil')
def tampil():
    cur = cnx.cursor()
    cur.execute("SELECT * FROM vaksin")
    data = cur.fetchall()
    cur.close()
    return render_template('tampil.html', data=data)


@app.route('/syarat')
def syarat():
    cur = cnx.cursor()
    cur.execute("SELECT * FROM vaksin")
    data = cur.fetchall()
    cur.close()
    return render_template('syarat.html', data=data)


@app.route('/hapus/<id>')
def hapus(id):
    query = "DELETE FROM vaksin WHERE id_vaksin = %s"
    data = (id,)
    
    cur = cnx.cursor()
    cur.execute(query, data)
    cnx.commit()
    cur.close()
    
    return redirect('/tampil')

@app.route('/update/<id>')
def update(id):
    query = "SELECT * FROM vaksin WHERE id_vaksin = %s"
    data = (id,)
    
    cur = cnx.cursor()
    cur.execute(query, data)
    value = cur.fetchone()
    cur.close()
    
    return render_template('update.html', value=value)

@app.route('/aksiupdate', methods=["POST", "GET"])
def aksiupdate():
    id = request.form["id_vaksin"]
    jenis_vaksin = request.form["jenis_vaksin"]
    umur = request.form["umur"]
    lokasi = request.form["lokasi"]
    tahun = request.form["tahun"]
    
    query = "UPDATE vaksin SET jenis_vaksin = %s, umur = %s, lokasi = %s, tahun = %s where id_vaksin = %s"
    data = (jenis_vaksin, umur, lokasi, tahun, id,)
    
    cur = cnx.cursor()
    cur.execute(query, data)
    cnx.commit()
    cur.close()
    
    return redirect('/tampil')

if __name__ == "__main__":
    app.run(debug=True)
