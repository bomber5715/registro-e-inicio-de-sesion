from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

#mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_login'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur =  mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    data = cur.fetchall()
    return render_template('Index.html', user = data)
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_encriptada = generate_password_hash(password)
        fullname = request.form['fullname']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO user (username, password, fullname, phone) VALUES (%s, %s, %s, %s)',
        (username, password_encriptada, fullname, phone))
        mysql.connection.commit()
        flash('Contacto añadido exitosamente')
        return redirect(url_for('Index'))
    

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_encriptadaqueseactualiza = generate_password_hash(password)
        fullname = request.form['fullname']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
          UPDATE user
          SET username = %s,
                password = %s,
                fullname = %s,
                phone = %s
          WHERE id = %s
        """, (username, password_encriptadaqueseactualiza, fullname, phone, id))
        mysql.connection.commit()
        flash('Contacto actualizado exitosamente')
        return redirect(url_for('Index'))
    
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM user WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto removido exitosamente')
    return redirect(url_for('Index'))


if __name__ == '__main__':
 app.run(port = 3000, debug = True)
