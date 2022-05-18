
from flask import Flask, render_template,request, url_for, redirect,session
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'novel-fyp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# configure secret key for session protection)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route("/test-db")
def test_db():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from users")
    data = cursor.fetchone()
    return str(data)

@app.route("/")
def index():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books where category='fiction'")
    fiction = cursor.fetchall()
    cursor.execute("SELECT * from books where category='science'")
    science = cursor.fetchall()
    cursor.execute("SELECT * from books where category='comics'")
    comics = cursor.fetchall()
    # return str(books)
    if 'loggedin' in session: 
        return render_template("index.html",fiction=fiction,science=science,comics=comics,loggedin=True,username=session['name'])
    else:
        return render_template("index.html",fiction=fiction,science=science,comics=comics,loggedin=False)

@app.route("/order-details")
def order_details():
    return render_template("order-details.html")

@app.route("/books-by-category/<string:category>")
def books_by_category(category):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books where category=%s",category)
    books = cursor.fetchall()
    return render_template("books-by-category.html",books=books,category=category)

@app.route("/search/<string:q>")
def search(q):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title Like '%{text:}%';".format(text=q))
    books = cursor.fetchall()
    if not books:
        cursor.execute("SELECT * FROM books WHERE category Like '%{text:}%';".format(text=q))
        books = cursor.fetchall()
    if not books:
        cursor.execute("SELECT * FROM books WHERE author Like '%{text:}%';".format(text=q))
        books = cursor.fetchall()
    if not books:
        cursor.execute("SELECT * FROM books WHERE publisher Like '%{text:}%';".format(text=q))
        books = cursor.fetchall()

    return render_template("search-results.html",books=books,q=q)



@app.route("/all-books")
def all_books():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books")
    books = cursor.fetchall()
    if 'loggedin' in session:    
        return render_template("all-books.html",books=books,loggedin=True)
    else:
        return render_template("all-books.html",books=books,loggedin=False)

@app.route("/book-detail/<int:id>")
def book_detail(id):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books where id=%s",id)
    book = cursor.fetchone()
    return render_template("book-detail.html",book=book)

@app.route("/details")
def details():
    return render_template("details.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password  = request.form.get("password")
        if not email or not password:
            return "Oops! Something is missing"
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from users where email=%s",(email))
        account = cursor.fetchone()
        if not account:
            return "Invalid Email Address!"
        if password == account[2]:
            session['loggedin'] = True
            session['userid'] = account[0]
            session['name'] = account[3]+ " " + account[4]
            return redirect(url_for("index"))
        else:
            return "Invalid Password!"
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('name', None)
    # Redirect to index page
    return redirect(url_for('index'))

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password  = request.form.get("password")
        conf_password = request.form.get("conf_password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        country = request.form.get("country")
        gender = request.form.get("radiogroup1")
        if not email or not password or not conf_password or not first_name or not last_name or not country or not gender:
            return "Oops! Something is missing"
        if password != conf_password:
            return "Password doesn't match!"
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from users where email=%s",(email))
        exist = cursor.fetchone()
        if exist:
            return "Email address already registered!"
        cursor.execute("INSERT INTO users (email, password, first_name,last_name,country,gender) VALUES (%s, %s,%s, %s,%s, %s);",(email,password,first_name,last_name,country,gender))
        conn.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)