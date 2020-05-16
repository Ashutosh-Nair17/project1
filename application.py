import os
import requests
from flask import Flask, session, render_template, request,redirect,url_for,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
     return render_template("Login_v8/index.html")



@app.route("/login",methods=["POST"])
def login():
  username=request.form.get('username')
  password=request.form.get('pass')
  if db.execute("SELECT * FROM users WHERE email = :username AND password = :password", {"username":username,"password":password}).rowcount == 0:
    return render_template("search.html")

  else :
    return ("no such user exists.Register the user first")




@app.route("/register.html")
def register():
	return render_template("Login_v8/registration.html")



@app.route("/register",methods=["POST"])
def registration():
	name=request.form.get('email')
	pass1 = request.form.get('psw') 
	password=request.form.get('psw-repeat')
	if db.execute("SELECT * FROM users WHERE email = :username", {"username":name}).rowcount == 0:
		if (pass1==password) :
				db.execute("INSERT INTO users(email,password) VALUES(:name,:pass)",{"name":name ,"pass":pass1})
				db.commit()
				return redirect(url_for('index'))
			
		else:
			return redirect(url_for('Login_v8/registration.html'))

	else:
		return "user with that name already exists"



@app.route('/login/search',methods=["POST","GET"])
def search():
	search=request.form.get('search')
	cari = "%" + search +"%"
	flag=False

	check1=request.form.get('isbn')
	if check1:
		results=db.execute(" SELECT  * FROM books where isbn LIKE :search ",{"search":cari}).fetchall()
		if results is None:
			flag=True
		return render_template('results.html',results=results,flag=flag)

	check2=request.form.get('title')
	if check2:
		results=db.execute("SELECT  * FROM books where UPPER(title) LIKE UPPER(:search) ",{"search":cari}).fetchall()
		if results is None:
			flag=True
		return render_template('results.html',results=results,flag=flag)

	check3=request.form.get('author')
	if check3:
		results=db.execute("SELECT  * FROM books where UPPER(author) LIKE UPPER(:search) ",{"search":cari}).fetchall()
		if results is None:
			flag=True
		return render_template('results.html',results=results,flag=flag)


@app.route("/login/search/<int:book_id>",methods=["POST","GET"])
def book(book_id):
 desc=db.execute("SELECT * from books where id = :id",{"id":book_id}).fetchone()
 isbns=db.execute("SELECT isbn from books where id=:id",{"id":book_id}).fetchone()
 reviews=db.execute("SELECT review from reviews where books_id = :id",{"id":book_id}).fetchall()
 res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "b10J7lLvEotDKteFFqng", "isbns":"isbns"})
 data = res.json()
 newDict={}
 for item in data['books']:
  newDict.update(item)
 data['books']=newDict
 avg_rating=data['books']['average_rating']
 review_count=data['books']['work_reviews_count']
 return render_template('book.html',desc=desc,reviews=reviews,rate=avg_rating,count=review_count)


@app.route("/reviewposting/<int:book_id>",methods=["POST"])
def insert(book_id):
	review=request.form.get('name')
	rating=request.form['val']
	db.execute("INSERT into reviews(books_id,review,rating) values(:id,:review,:rating)",{"id":book_id ,"review":review,"rating":rating})
	db.commit()
	return redirect(url_for('book',book_id=book_id))	


@app.route("/api/<string:isbn>")
def flight_api(isbn):
    
    apires = db.execute("SELECT * FROM BOOKS WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if apires is None:
        return jsonify({"error": "Invalid isbn"}), 422
    return jsonify({
            "title": apires.title,
            "author": apires.author,
            "year": apires.year,
            "isbn": apires.isbn
        })