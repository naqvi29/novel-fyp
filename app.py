
from flask import Flask, render_template,request, url_for, redirect,session
from flaskext.mysql import MySQL
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'novel-fyp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3307
mysql.init_app(app)

# configure secret key for session protection)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

BOOK_IMAGES = join(dirname(realpath(__file__)), 'static/assets/book-images')

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg',}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        return render_template("index.html",fiction=fiction,science=science,comics=comics,loggedin=True,username=session['name'],type=session['type'])
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
    if 'loggedin' in session: 
        return render_template("books-by-category.html",books=books,category=category,loggedin=True,username=session['name'],type=session['type'])
    else:
        return render_template("books-by-category.html",books=books,category=category,loggedin=False)

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
    if 'loggedin' in session: 
        return render_template("search-results.html",books=books,q=q,loggedin=True,username=session['name'],type=session['type'])
    else:
        return render_template("search-results.html",books=books,q=q,loggedin=False)



@app.route("/all-books")
def all_books():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books")
    books = cursor.fetchall()
    if 'loggedin' in session:    
        return render_template("all-books.html",books=books,loggedin=True,username=session['name'],type=session['type'])
    else:
        return render_template("all-books.html",books=books,loggedin=False)

@app.route("/book-detail/<int:id>")
def book_detail(id):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books where id=%s",id)
    book = cursor.fetchone()
    if 'loggedin' in session: 
        return render_template("book-detail.html",book=book,loggedin=True,username=session['name'],type=session['type'])
    else:
        return render_template("book-detail.html",book=book,loggedin=False)

@app.route("/my-books")
def my_books():
    if 'loggedin' in session: 
        if session['type'] == 'shopkeeper':            
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("SELECT * from books where publisher_id=%s",(session['userid']))
            books = cursor.fetchall()
            return render_template("my-books.html",loggedin=True,books=books,username=session['name'],type=session['type'])
        else:
            return "ShopKeeper Account Not Found!"
    else:
        return "Please Login First as a shop keeper!"

@app.route("/delete-book/<int:id>")
def delete_book(id):
    if 'loggedin' in session: 
        if session['type'] == 'shopkeeper' or session['type'] == 'admin':            
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("DELETE  from books where id=%s",(id))
            conn.commit()
            if session['type'] == 'shopkeeper':
                return redirect(url_for("my_books"))
            elif session['type'] == 'admin':
                return redirect(url_for("books"))
        else:
            return "ShopKeeper or Admin Account Not Found!"
    else:
        return "Please Login First as a shop keeper or Admin!"


@app.route("/add-book", methods=['GET','POST'])
def add_book():
    if 'loggedin' in session: 
        if session['type'] == 'shopkeeper':
            if request.method == 'POST':
                title = request.form.get("title")
                author = request.form.get("author")
                description = request.form.get("description")
                category = request.form.get("category")
                price = float(request.form.get("price"))
                quantity = request.form.get("quantity")
                publisher = session['name']
                publisher_id =session['userid']
                image = request.files["image"]
                rating = None
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(
                        os.path.join(BOOK_IMAGES, filename))
                    # compress image
                    newimage = Image.open(os.path.join(BOOK_IMAGES, str(filename)))
                    newimage.thumbnail((400, 400))
                    newimage.save(os.path.join(BOOK_IMAGES, str(filename)), quality=95)
                    conn = mysql.connect()
                    cursor =conn.cursor()
                    cursor.execute("INSERT INTO books (title, author, publisher,publisher_id,category,price,quantity,image,description,rating) VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s, %s);",(title,author,publisher,publisher_id,category,price,quantity,filename,description,rating))
                    conn.commit()
                    return redirect(url_for('index'))
                else:
                    return "File not found or incorrect format"
                
            else:
                return render_template("add-book.html",loggedin=True,username=session['name'],type=session['type'])
        else:
            return "ShopKeeper Account Not Found!"
    else:
        return "Please Login First as a shop keeper!"

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
            session['type'] = account[7]
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

@app.route("/checkout/<string:total_price>,")


#ADMIN DASHBOARD
@app.route("/admin-dashboard")
def admin_dashboard():        
    if 'loggedin' in session: 
        if session['type'] == 'admin':    
            return render_template("admin-dashboard.html")
        else:
            session.pop('loggedin', None)
            session.pop('userid', None)
            session.pop('name', None)
            return redirect(url_for("login"))
    else:
            return redirect(url_for("login"))

@app.route("/users")
def users():        
    if 'loggedin' in session: 
        if session['type'] == 'admin':    
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("SELECT * from users")
            users = cursor.fetchall()
            return render_template("users.html",loggedin=True,users=users,username=session['name'],type=session['type'])
        else:
            return "Admin Account Not Found!"
    else:
        return "Please Login First as a admin!"

@app.route("/books")
def books():        
    if 'loggedin' in session: 
        if session['type'] == 'admin':    
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("SELECT * from books")
            books = cursor.fetchall()
            return render_template("books.html",loggedin=True,books=books,username=session['name'],type=session['type'])
        else:
            return "Admin Account Not Found!"
    else:
        return "Please Login First as a admin!"



if __name__ == '__main__':
    app.run(debug=True)