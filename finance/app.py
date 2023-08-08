import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

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
    transactions = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total = cash
    for transaction in transactions:
        total += transaction["price"] * transaction["shares"]

    return render_template("index.html", transactions=transactions, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        user_id = session["user_id"]
        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("Please priovide a valid symbol")

        stock = lookup(symbol)
        if stock == None:
            return apology("Symbol does not exist or left blank")

        shares = request.form.get("shares")
        if not shares:
            return apology("Please provide number of shares")

        if not shares.isdigit():
            return apology("Must be an intiger")

        if int(shares) < 0:
            return apology("Possitive integer only")

        transaction_value = int(shares) * stock["price"]

        cash_dic = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        cash = cash_dic[0]["cash"]
        name = stock["name"]

        if transaction_value > cash:
            return apology("Not enough money")

        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, time, type) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                   user_id, symbol, name, int(shares), stock["price"], "bought")

        updated_cash = cash - transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
        flash("Stock bought")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT type, symbol, name, shares, price, time FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please provide a valid symbol")
        else:
            stock = lookup(symbol.upper())
            if stock == None:
                return apology("Symbol does not exist")
            else:
                return render_template("/quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username is provided
        if not request.form.get("username"):
            return apology("please provide username")

        # Ensure password is provided
        elif not request.form.get("password"):
            return apology("please provide password")

        # Ensure confirmation password is provided
        elif not request.form.get("confirmation"):
            return apology("please confirm password")

        # Ensure password and confirmation password are the same
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Query database for username
        result = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if result:
            return apology("username already exists")

        # Hash the password
        hashed_password = generate_password_hash(request.form.get("password"))

        # Insert a new user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hashed_password)

        # Remember which user has logged in
        id = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = id[0]["id"]

        # Redirect to homepage
        return redirect("/")

    else:
        # User reached route via GET
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    user_id = session["user_id"]

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please select a symbol")

        shares_entered = request.form.get("shares")

        if not shares_entered:
            return apology("Number of shares cannot be blank")

        elif int(shares_entered) <= 0:
            return apology("Please enter a positive number of shares")

        shares = db.execute("SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)[
            0]["total_shares"]

        price = lookup(symbol)["price"]
        name = lookup(symbol)["name"]
        if int(shares_entered) > shares:
            return apology("You don't have enough shares")

        transaction_value = int(shares_entered) * price

        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, time, type) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                   user_id, symbol, name, -int(shares_entered), price, "sold")

        updated_cash = cash + transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        flash("Stock sold")

        return redirect("/")

    else:

        # Stocks user has
        transactions = db.execute("SELECT symbol, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

        return render_template("sell.html", transactions=transactions)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("old_password"):
            return apology("must provide old password", 403)

        elif not request.form.get("new_password"):
            return apology("must provide new password", 403)

        elif not request.form.get("confirm_password"):
            return apology("must provide password confirmation", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("invalid old password", 403)

        # Ensure password and confirmation password are the same
        if request.form.get("new_password") != request.form.get("confirm_password"):
            return apology("passwords do not match", 403)

         # Hash the password
        hashed_password = generate_password_hash(request.form.get("new_password"))

        # Insert a new user
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, session["user_id"])

        flash("Password successfully changed")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("change_password.html")