from flask import Flask, render_template,request, url_for, redirect,session,jsonify
from flaskext.mysql import MySQL
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from PIL import Image
from flask_mail import Mail, Message
from pymysql.cursors import DictCursor

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'book_kingdom'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'LAwrence1234**'
# app.config['MYSQL_DATABASE_DB'] = 'novel-fyp'
# app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)


mysql2 = MySQL(cursorclass=DictCursor)
app.config['MYSQL2_DATABASE_USER'] = 'root'
app.config['MYSQL2_DATABASE_PASSWORD'] = ''
app.config['MYSQL2_DATABASE_DB'] = 'book_kingdom'
app.config['MYSQL2_DATABASE_HOST'] = '127.0.0.1'
mysql2.init_app(app)


# Mail server config.
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bookkingdom172@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Book12345'
app.config['MAIL_PASSWORD'] = 'fbijqpcqyeecdnam'
app.config['MAIL_DEFAULT_SENDER'] = ('bookkingdom172@gmail.com')
mail = Mail(app)

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

@app.route("/search", methods=['GET','POST'])
def search():
    q = request.form.get("q")
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

@app.route("/filter")
def filter():
    category = request.args.get("category")
    price_min = request.args.get("price-min")
    price_max = request.args.get("price-max")
    print(price_min)
    print(price_max)
    print(category)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT * from books where category=%s and price > %s and price <%s;",(category,price_min,price_max))
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
                publisher = request.form.get("publisher")
                isbn = request.form.get("isbn")
                description = request.form.get("description")
                category = request.form.get("category")
                price = float(request.form.get("price"))
                quantity = request.form.get("quantity")
                phone = request.form.get("phone")
                address = request.form.get("address")
                discount = request.form.get("discount")
                added_by = session['name']
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
                    cursor.execute("INSERT INTO books (title, author, added_by,publisher_id,category,price,quantity,image,description,rating,publisher,isbn,phone,address,discount) VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s);",(title,author,added_by,publisher_id,category,price,quantity,filename,description,rating,publisher,isbn,phone,address,discount))
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

@app.route("/edit-book/<string:id>", methods=['GET','POST'])
def edit_book(id):
    if 'loggedin' in session: 
        if session['type'] == 'shopkeeper':
            if request.method == 'POST':
                title = request.form.get("title")
                author = request.form.get("author")
                publisher = request.form.get("publisher")
                isbn = request.form.get("isbn")
                description = request.form.get("description")
                category = request.form.get("category")
                price = float(request.form.get("price"))
                quantity = request.form.get("quantity")
                phone = request.form.get("phone")
                address = request.form.get("address")
                discount = request.form.get("discount")
                added_by = session['name']
                publisher_id =session['userid']
                image = request.files["image"]
                rating = None
                if image:
                    if allowed_file(image.filename):
                        filename = secure_filename(image.filename)
                        image.save(
                            os.path.join(BOOK_IMAGES, filename))
                        # compress image
                        newimage = Image.open(os.path.join(BOOK_IMAGES, str(filename)))
                        newimage.thumbnail((400, 400))
                        newimage.save(os.path.join(BOOK_IMAGES, str(filename)), quality=95)
                        conn = mysql.connect()
                        cursor =conn.cursor()
                        cursor.execute("UPDATE books SET title=%s,author=%s,added_by=%s,publisher_id=%s,category=%s,price=%s,quantity=%s,image=%s,description=%s,rating=%s,publisher=%s,isbn=%s,phone=%s,address=%s,discount=%s WHERE id=%s",(title,author,added_by,publisher_id,category,price,quantity,filename,description,rating,publisher,isbn,phone,address,discount,id))
                        conn.commit()
                    else:
                        return "File incorrect format"
                else:
                    conn = mysql.connect()
                    cursor =conn.cursor()
                    cursor.execute("UPDATE books SET title=%s,author=%s,added_by=%s,publisher_id=%s,category=%s,price=%s,quantity=%s,description=%s,rating=%s,publisher=%s,isbn=%s,phone=%s,address=%s,discount=%s WHERE id=%s;",(title,author,added_by,publisher_id,category,price,quantity,description,rating,publisher,isbn,phone,address,discount,id))
                    conn.commit()
                return redirect(url_for('my_books'))
                
            else:
                conn = mysql.connect()
                cursor =conn.cursor()
                cursor.execute("SELECT * from books where id=%s",(id))
                book = cursor.fetchone()
                return render_template("edit-book.html",book=book,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
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
            delivery_method = request.form['delivery_method']
            print(product_ids)
            print(name)
            print(email)
            print(phone)
            print(address)
            print(del_ins)
            print(delivery_method)
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
                bookQty = book[6]
                bookQty = bookQty - 1
                if delivery_method == "delivery":
                    price = price+200
                cursor.execute("INSERT INTO orders (user_id, book_id,publisher_id,total_price,status,city,delivery_address,name,email,phone,del_ins,del_method) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s);",(user_id,book_id,publisher_id,price,"pending",city,address,name,email,phone,del_ins,delivery_method))
                conn.commit()
                cursor.execute("UPDATE books SET quantity=%s where id=%s",(bookQty,book_id))
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
        if request.method == 'POST':
            product_ids = request.form['product_ids']
            product_ids = product_ids.split(",")
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            del_ins = request.form['del_ins']
            city = request.form['city']
            delivery_method = request.form['delivery_method']
            print(product_ids)
            print(name)
            print(email)
            print(phone)
            print(address)
            print(del_ins)
            print(delivery_method)
            # fetch book data 
            user_id =0
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
                bookQty = book[6]
                bookQty = bookQty-1
                if delivery_method == "delivery":
                    price = price+200
                cursor.execute("INSERT INTO orders (user_id, book_id,publisher_id,total_price,status,city,delivery_address,name,email,phone,del_ins,del_method) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s);",(user_id,book_id,publisher_id,price,"pending",city,address,name,email,phone,del_ins,delivery_method))
                conn.commit()
                cursor.execute("UPDATE books SET quantity=%s where id=%s",(bookQty,book_id))
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
            return render_template("cart.html",loggedin=False,username="Guest",userid=0,type="Guest",products=products,sub_total=sub_total,product_ids=product_ids)

@app.route("/order-placed")
def order_placed():
    if 'loggedin' in session:
        return render_template("order-placed.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return render_template("order-placed.html",loggedin=False,username="Guest",userid=0,type="Guest")

@app.route("/view-user-orders/<int:userid>")
def view_user_orders(userid):
    if 'loggedin' in session:
        if session['type'] == 'user':
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("SELECT * from orders where user_id=%s and status='pending'",(userid))
            pending_orders = cursor.fetchall()
            cursor.execute("SELECT * from orders where user_id=%s and status='delivered'",(userid))
            delivered_orders = cursor.fetchall()
            return render_template("view-user-orders.html",pending_orders=pending_orders,delivered_orders=delivered_orders,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
        else:
            return "Please Login First as user account!"
    else:
        return "Please Login First!"

@app.route("/view-shopkeeper-orders/<int:userid>")
def view_shopkeepers_orders(userid):
    if 'loggedin' in session:
        if session['type'] == 'shopkeeper':
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("SELECT * from orders where publisher_id=%s and status='pending' and user_id<>%s",(userid,userid))
            pending_orders = cursor.fetchall()
            cursor.execute("SELECT * from orders where publisher_id=%s and status='delivered'",(userid))
            delivered_orders = cursor.fetchall()
            cursor.execute("SELECT * from orders where status='pending' and user_id=%s",(userid))
            my_orders = cursor.fetchall()
            return render_template("view-shopkeeper-orders.html",pending_orders=pending_orders,delivered_orders=delivered_orders,my_orders=my_orders,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
        else:
            return "Please Login First as shopkeeper account!"
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
            # now rate book            
            cursor.execute("SELECT * from orders where order_id=%s",(id))
            order = cursor.fetchone()
            book_id = order[2]
            cursor.execute("UPDATE books SET rating=%s WHERE id=%s",(rate,book_id))
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
        elif session['type'] == 'shopkeeper':
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("DELETE FROM orders WHERE order_id=%s",(id))
            conn.commit()
            return redirect(url_for("view_shopkeepers_orders",userid=session['userid']))
        else:
            return "Please Login First as customer!"
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

@app.route("/contact-us",methods=['GET','POST'])
def contact_us():
    if 'loggedin' in session:   
        if request.method=="POST": 
            name=request.form.get("name") 
            email=request.form.get("email") 
            message=request.form.get("message") 
            msg = Message("BookKingdom | New Contact",sender='bookkingdom172@gmail.com', recipients=["bookkingdom172@gmail.com"])
            msg.html = "<p><strong>Name</strong></p><p>"+name+"</p><br><p><strong>email</strong></p><p>"+email+"</p><br><p><strong>message</strong></p><p>"+message+"</p>"
            mail.send(msg)
            return render_template("contact-us.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'],msg="sent")
        else:
            return render_template("contact-us.html",loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        if request.method=="POST":
            name=request.form.get("name")  
            email=request.form.get("email") 
            message=request.form.get("message") 
            msg = Message("BookKingdom | New Contact",sender='bookkingdom172@gmail.com', recipients=["bookkingdom172@gmail.com"])
            msg.html = "<p><strong>Name</strong></p><p>"+name+"</p><br><p><strong>email</strong></p><p>"+email+"</p><br><p><strong>message</strong></p><p>"+message+"</p>"
            mail.send(msg)
            return render_template("contact-us.html",loggedin=False,msg="sent")
        else:
            return render_template("contact-us.html",loggedin=False)

@app.route("/forgot-password", methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get("email")
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from users where email=%s",email)
        data = cursor.fetchone()
        if not data:
            return render_template("forgot-password.html",error="Email Address Not Registered!")
        msg = Message("BookKingdom",sender='bookkingdom172@gmail.com', recipients=[email])
        # msg = Message('Hello from the other side!', sender =   'bookkingdom172@gmail.com', recipients = ['mali29april@gmail.com'])
        msg.html = "<p>Hello,</p><p>we've received a forget password request for your account</p><p>so here is the your password <strong>"+data[2]+"</strong></p><p>If you didn't request this, please let us know immediately by replying to this email.</p><br><p>The BookKingdom Team</p>"
        mail.send(msg)
        return render_template("forgot-password.html",success="Your Password Has been sent to your email address!")
        

    else:
        return render_template("forgot-password.html")

@app.route("/profile",methods=['GET','POST'])
def profile():
    if 'loggedin' in session:   
        if request.method == 'POST':
            f_name = request.form.get("f_name")
            l_name = request.form.get("l_name")
            email = request.form.get("email")
            password = request.form.get("password")
            gender = request.form.get("gender")
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute("UPDATE users SET first_name=%s,last_name=%s,email=%s,password=%s ,gender=%s WHERE userid=%s",(f_name,l_name,email,password,gender,session['userid']))
            conn.commit()
            return redirect(url_for("profile"))
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from users where userid=%s",session['userid'])
        data = cursor.fetchone() 
        return render_template("profile.html",data=data,loggedin=True,username=session['name'],userid=session['userid'],type=session['type'])
    else:
        return render_template("contact-us.html",loggedin=False)


# ----------------------------------------- MOBILE APIS -------------------------------------------------

@app.route("/register-user-api", methods=['POST'])
def register_api():
    try:
        if request.method == 'POST':
            if request.is_json:            
                data = request.get_json()
                email = data["email"]
                password = data["password"]
                first_name = data["first_name"]
                last_name = data["last_name"]
                gender = data["gender"]
                type = "user"
                if not email or not password  or not first_name or not last_name or not gender:
                    return jsonify({"success":False,"error":"Oops! Something is missing"})
                conn = mysql2.connect()
                cursor =conn.cursor()
                cursor.execute("SELECT * from users where email=%s",(email))
                exist = cursor.fetchone()
                if exist:
                    return jsonify({"success":False,"error":"Email address already registered"})
                cursor.execute("INSERT INTO users (email, password, first_name,last_name,gender,type) VALUES (%s,%s, %s, %s,%s, %s);",(email,password,first_name,last_name,gender,type))
                conn.commit()
                cursor.execute("SELECT * from users where email=%s",(email))
                data = cursor.fetchone()
                return jsonify({"success":True,"status":"Registered Successfully!","data":data})
            else:
                return jsonify({"success":False,"error":"Invalid Json!"})
        else:
            return jsonify({"success":False,"error":"Invalid Request Type!"})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route("/login-user-api", methods=['POST'])
def login_api():
    try:
        if request.method == 'POST':
            if request.is_json:            
                data = request.get_json()
                email = data["email"]
                password = data["password"]
                if not email or not password:
                    return jsonify({"success":False,"error":"Oops! Something is missing!"})
                conn = mysql2.connect()
                cursor =conn.cursor()
                cursor.execute("SELECT * from users where email=%s",(email))
                account = cursor.fetchone()
                if not account:
                    return jsonify({"success":False,"error":"Invalid Email Address!"})
                if password == account[2]:                
                    return jsonify({"success":True,"status":"Login Success!", "data":account})
                else:
                    return jsonify({"success":False,"error":"Invalid Password!"})
            else:
                    return jsonify({"success":False,"error":"Invalid Json!"})
        else:
            return jsonify({"success":False,"error":"Invalid Request Type!"})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route("/get-all-books-api")
def get_all_books_api():
    try:
        conn = mysql2.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from books")
        books = cursor.fetchall()
        return jsonify({"success":True,"data":books})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route("/get-books-by-category-api/<string:category>")
def get_books_by_category_api(category):
    try:
        conn = mysql2.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from books where category=%s",category)
        books = cursor.fetchall()
        return jsonify({"success":True,"data":books})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route("/search-api", methods=['GET','POST'])
def search_api():
    try:
        if request.is_json:            
            data = request.get_json()
            q = data["keyword"]
            conn = mysql2.connect()
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
            return jsonify({"success":True,"data":books})
        else:
                return jsonify({"success":False,"error":"Invalid Json!"})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route("/single-book-detail-api/<int:id>")
def single_book_detail_api(id):
    try:
        conn = mysql2.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from books where id=%s",id)
        book = cursor.fetchone()
        return jsonify({"success":True,"data":book})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)
