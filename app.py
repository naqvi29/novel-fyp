
from django.shortcuts import render
from flask import Flask, render_template,request, url_for, redirect,session,jsonify
from flaskext.mysql import MySQL
import os
from os.path import join, dirname, realpath
from importlib_metadata import method_cache
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'novel-fyp'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'LAwrence1234**'
# app.config['MYSQL_DATABASE_DB'] = 'novel-fyp'
# app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
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
        return render_template("index.html",fiction=fiction,science=science,comics=comics,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
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
        return render_template("books-by-category.html",books=books,category=category,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
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
        return render_template("search-results.html",books=books,q=q,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return render_template("search-results.html",books=books,q=q,loggedin=False)



@app.route("/all-books")
def all_books():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books")
    books = cursor.fetchall()
    if 'loggedin' in session:    
        return render_template("all-books.html",books=books,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return render_template("all-books.html",books=books,loggedin=False)

@app.route("/book-detail/<int:id>")
def book_detail(id):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books where id=%s",id)
    book = cursor.fetchone()
    if 'loggedin' in session: 
        return render_template("book-detail.html",book=book,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
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
            return render_template("my-books.html",loggedin=True,books=books,username=session['name'],userid=session['userid'],type=session['type'])
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
                return render_template("add-book.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
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
            return render_template("login.html",error="Oops! Something is missing")
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from users where email=%s",(email))
        account = cursor.fetchone()
        if not account:
            return render_template("login.html",error="Invalid Email Address!")
        if password == account[2]:
            session['loggedin'] = True
            session['userid'] = account[0]
            session['name'] = account[3]+ " " + account[4]
            session['type'] = account[6]
            if session['type'] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("index"))
        else:
            return render_template("login.html",error="Invalid Password!")
        
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
        type = request.form.get("type")
        print(type)
        gender = request.form.get("radiogroup1")
        if not email or not password or not conf_password or not first_name or not last_name or not gender or not type:
            return render_template("register.html",error="Oops! Something is missing")
        if password != conf_password:
            return render_template("register.html",error="Password doesn't match!")
        if type != "user" and type != "shopkeeper":
            return render_template("register.html",error="Invalid User Type!")
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from users where email=%s",(email))
        exist = cursor.fetchone()
        if exist:
            return render_template("register.html",error="Email address already registered!")
        cursor.execute("INSERT INTO users (email, password, first_name,last_name,gender,type) VALUES (%s,%s, %s, %s,%s, %s);",(email,password,first_name,last_name,gender,type))
        conn.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/checkout", methods=['GET','POST'])
def checkout():        
    if 'loggedin' in session:
        cart_total = request.form['cart_total']
        product_ids = request.form['product_ids']
        return str(product_ids)
        product_ids = product_ids.split(",")
        print(cart_total)
        print(product_ids)
        # fetch book data 
        user_id = session['userid']
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from users where userid=%s",(user_id))
        user_data = cursor.fetchone()
        city = user_data[8]
        address = user_data[9]
        book = cursor.fetchone()
        for i in product_ids:
            print(i)
            cursor =conn.cursor()
            cursor.execute("SELECT * from books where id=%s",(i))
            book = cursor.fetchone()
            print("book")
            print(book)
            book_id = book[0]
            print(book_id)
            publisher_id = book[10]
            price = book[5]
            cursor.execute("INSERT INTO orders (user_id, book_id,publisher_id,total_price,status,city,delivery_address) VALUES (%s, %s,%s, %s,%s, %s,%s);",(user_id,book_id,publisher_id,price,"pending",city,address))
            conn.commit()
        return "Order Placed Successfully!"
    else:
        return "Please Login First!"


@app.route("/cart/<string:product_ids>", methods=["GET","POST"])
def cart(product_ids):        
    if 'loggedin' in session:
        if request.method == 'POST':
            product_ids = request.form['product_ids']
            product_ids = product_ids.split(",")
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            del_ins = request.form['del_ins']
            city = request.form['city']
            print(product_ids)
            print(name)
            print(email)
            print(phone)
            print(address)
            print(del_ins)
            # fetch book data 
            user_id = session['userid']
            sub_total = 0
            for i in product_ids:
                print(i)
                conn = mysql.connect()
                cursor =conn.cursor()
                cursor.execute("SELECT * from books where id=%s",(i))
                book = cursor.fetchone()
                book_id = book[0]
                publisher_id = book[10]
                price = book[5]
                cursor.execute("INSERT INTO orders (user_id, book_id,publisher_id,total_price,status,city,delivery_address,name,email,phone,del_ins) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s);",(user_id,book_id,publisher_id,price,"pending",city,address,name,email,phone,del_ins))
                conn.commit()
            return redirect(url_for("order_placed"))
        else:
            products = []
            productids = product_ids.split(",")
            sub_total = 0
            for i in productids:
                conn = mysql.connect()
                cursor =conn.cursor()
                cursor.execute("SELECT * from books where id=%s",(int(i)))
                product = cursor.fetchone()
                sub_total = sub_total+float(product[5])
                products.append(product)
            return render_template("cart.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'],products=products,sub_total=sub_total,product_ids=product_ids)
    else:
        return "Please Login First!"

@app.route("/order-placed")
def order_placed():
    if 'loggedin' in session:
        return render_template("order-placed.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return "Please Login First!"

@app.route("/view-user-orders/<int:userid>")
def view_user_orders(userid):
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from orders where user_id=%s and status='pending'",(userid))
        pending_orders = cursor.fetchall()
        cursor.execute("SELECT * from orders where user_id=%s and status='delivered'",(userid))
        delivered_orders = cursor.fetchall()
        return render_template("view-user-orders.html",pending_orders=pending_orders,delivered_orders=delivered_orders,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return "Please Login First!"

@app.route("/view-shopkeeper-orders/<int:userid>")
def view_shopkeepers_orders(userid):
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from orders where publisher_id=%s and status='pending'",(userid))
        pending_orders = cursor.fetchall()
        cursor.execute("SELECT * from orders where publisher_id=%s and status='delivered'",(userid))
        delivered_orders = cursor.fetchall()
        return render_template("view-shopkeeper-orders copy.html",pending_orders=pending_orders,delivered_orders=delivered_orders,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return "Please Login First!"

@app.route("/deliver-order/<int:id>")
def deliver_order(id):
    if 'loggedin' in session: 
        if session['type'] == 'shopkeeper':
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("UPDATE orders SET status='delivered' WHERE order_id=%s",(id))
            conn.commit()
            return redirect(url_for("view_shopkeepers_orders",userid=session['userid']))
        else:
            return "Please Login First as shopkeeper!"
    else:
        return "Please Login First!"

@app.route("/rate-order/<int:id>", methods=['GET','POST'])
def rate_order(id):
    if 'loggedin' in session: 
        if session['type'] == 'user':
            rate = request.form.get("rate")
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("UPDATE orders SET rating=%s WHERE order_id=%s",(rate,id))
            conn.commit()
            return redirect(url_for("view_user_orders",userid=session['userid']))
        else:
            return "Please Login First as user!"
    else:
        return "Please Login First!"

@app.route("/cancel-order/<int:id>")
def cancel_order(id):
    if 'loggedin' in session: 
        if session['type'] == 'user':
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("DELETE FROM orders WHERE order_id=%s",(id))
            conn.commit()
            return redirect(url_for("view_user_orders",userid=session['userid']))
        else:
            return "Please Login First as shopkeeper!"
    else:
        return "Please Login First!"




    



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
            return render_template("users.html",loggedin=True,users=users,username=session['name'],userid=session['userid'],type=session['type'])
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
            return render_template("books.html",loggedin=True,books=books,username=session['name'],userid=session['userid'],type=session['type'])
        else:
            return "Admin Account Not Found!"
    else:
        return "Please Login First as a admin!"

@app.route("/orders")
def orders():        
    if 'loggedin' in session: 
        if session['type'] == 'admin':    
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("SELECT * from orders")
            orders = cursor.fetchall()
            return render_template("orders.html",loggedin=True,orders=orders,username=session['name'],userid=session['userid'],type=session['type'])
        else:
            return "Admin Account Not Found!"
    else:
        return "Please Login First as a admin!"

        
@app.route("/delete-user/<int:id>")
def delete_user(id):
    if 'loggedin' in session: 
        if session['type'] == 'admin':            
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("DELETE  from users where userid=%s",(id))
            conn.commit()
            return redirect(url_for("users"))
        else:
            return "Please Login First as Admin!"
    else:
        return "Please Login First as Admin!"
        
@app.route("/my-account", methods = ['GET','POST'])
def my_account():
    if 'loggedin' in session: 
        if session['type'] == 'admin':
            if request.method == 'POST':
                email = request.form.get("email")
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                gender = request.form.get("gender")
                password = request.form.get("password")
                conn = mysql.connect()
                cursor =conn.cursor()
                cursor.execute("UPDATE users SET email=%s,first_name=%s,last_name=%s,gender=%s,password=%s WHERE userid=%s",(email,first_name,last_name,gender,password,session['userid']))
                conn.commit()
                return redirect(url_for("users"))
            else:
                conn = mysql.connect()
                cursor =conn.cursor()
                cursor.execute("SELECT * from users where userid=%s",session['userid'])
                data = cursor.fetchone()
                return render_template("my-account.html",data=data)
        else:
            return "Please Login First as Admin!"
    else:
        return "Please Login First as Admin!"

@app.route("/our-vision")
def our_vision():
    if 'loggedin' in session:    
        return render_template("our-vision.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return render_template("our-vision.html",loggedin=False)

@app.route("/about-us")
def about_us():
    if 'loggedin' in session:    
        return render_template("about-us.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return render_template("about-us.html",loggedin=False)

@app.route("/contact-us")
def contact_us():
    if 'loggedin' in session:    
        return render_template("contact-us.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return render_template("contact-us.html",loggedin=False)

if __name__ == '__main__':
    app.run(debug=True)
