import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd, password_check

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    tracsac_data = db.execute(
        "SELECT symbol, SUM(shares) as shares, price, name, SUM(shares) AS total FROM transac WHERE user_id = ? GROUP BY symbol", user_id)
    cash_data = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total = cash_data

    for stock in tracsac_data:
        total += stock["price"] * stock["total"]

    return render_template("index.html", stocks=tracsac_data, cash=cash_data, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol").strip()
        if not symbol:
            return apology("Bruh Symbol is Missing...")

        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Bruh Is this Symbol Real...")

        shares = int(request.form.get("shares").strip())
        if shares < 0:
            return apology("Bruh Are You Selling or Buying...")

        transac_value = shares * stock["price"]
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transac_value:
            return apology("Bruh You Broke...")

        else:
            new_user_cash = user_cash - transac_value
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_user_cash, user_id)
            date = datetime.datetime.now()
            db.execute("INSERT INTO transac(user_id, symbol, shares, price, date, name, total) VALUES (?,?,?,?,?,?,?)",
                       user_id, stock["symbol"], shares, stock["price"], date, stock["name"], transac_value)
            flash("Purchased!")
            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    tracsac_data = db.execute("SELECT * FROM transac WHERE user_id = ? ORDER BY date DESC", user_id)

    return render_template("history.html", data=tracsac_data, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").strip())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password").strip()):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol").strip()
        if not symbol:
            return apology("Bruh Symbol is Missing...")

        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Bruh Is this Symbol Real...")

        else:
            return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        confirm = request.form.get("confirmation").strip()

        if not username:
            return apology("Bruh Username is Missing...")
        if not password:
            return apology("Bruh Password is Missing...")
        if not confirm:
            return apology("Bruh Confirm Password is Missing...")
        if password != confirm:
            return apology("Bruh Passwords are not the same...")

        if password_check(password) == False:
            return render_template("registerfailed.html")

        else:
            hash = generate_password_hash(password)
            try:
                new_user = db.execute("INSERT INTO users(username, hash, password) VALUES (?,?,?)", username, hash, password)
            except:
                return apology("Bruh You Are Existed")

            session["user_id"] = new_user
            flash("Registered!")
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute("SELECT symbol FROM transac WHERE user_id = ? GROUP BY symbol HAVING SUM(shares)", user_id)
        return render_template("sell.html", symbols=symbols_user)

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        user_id = session["user_id"]
        stock = lookup(symbol.upper())

        if not symbol:
            return apology("Bruh Symbol is Missing...")
        if not shares:
            return apology("Bruh Share(s) is Missing...")
        if int(shares) < 1:
            return apology("Bruh you don't even have it...")

        cur_price = float(shares) * stock["price"]
        old_shares = db.execute("SELECT shares FROM transac WHERE user_id = ? AND symbol = ?", user_id, symbol)[0]["shares"]
        old_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        new_cash = old_cash + cur_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)

        if int(shares) > old_shares:
            return apology("Bruh you are Not That Rich...")

        date = datetime.datetime.now()
        db.execute("INSERT INTO transac(user_id, symbol, shares, price, date, name, total) VALUES (?,?,?,?,?,?,?)",
                   user_id, symbol, (int(shares)*-1), stock["price"], date, stock["name"], cur_price)
        flash("Sold!")
        return redirect("/")


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():

    user_id = session["user_id"]
    cur_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    if request.method == "GET":
        return render_template("addcash.html", cash=cur_cash, usd=usd)

    else:
        amount = request.form.get("amount")
        if not amount:
            return apology("Bruh are you bRokE?!")
        if int(amount) < 1:
            return apology("Bruh are you sure you are aDdiNg MoNey?!")
        new_cash = cur_cash + float(amount)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
        flash("Added Successfully!")
        return redirect("/")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    user_id = session["user_id"]
    cur_pass = db.execute("SELECT password FROM users WHERE id = ?", user_id)[0]["password"]

    if request.method == "GET":
        return render_template("password.html")

    else:
        oldpass = request.form.get("oldpass")
        newpass = request.form.get("newpass")
        confirmation = request.form.get("confirmation")
        if oldpass != cur_pass:
            return apology("Bruh Wrong Old Password...")
        if not oldpass:
            return apology("Bruh Old Password Missing...")
        if not newpass:
            return apology("Bruh New Password Missing...")
        if not confirmation:
            return apology("Bruh Confirm Password Missing...")

        newhash = generate_password_hash(newpass)
        db.execute("UPDATE users SET hash = ?, password = ? WHERE id = ?", newhash, newpass, user_id)
        flash("Changed Successfully!")
        return redirect("/")