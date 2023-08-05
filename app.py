import os
from datetime import date, datetime

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from additional import login_required, connection, usd, to_dict, get_last

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Budget/Expense/Income periods
periods = {"annually": 365, "monthly": 31, "bi-weekly": 14, "weekly": 7, "daily": 1}
display_period = {365: "year", 31: "month", 14: "two weeks", 7: "week", 1: "day"}

# Income and Expense categories
income_types = ['Allowance', 'Employment', 'Gifts and Donations', 'Government Assistance', 'Investment', 'Rental Income', 'Retirement Income', 'Royalties and Licensing', 'Scholarship', 'Self-Employment', 'Side Jobs', 'Others']
categories = {
    'Debt Payments': ['Credit Card Payments', 'Student Loans', 'Other Loans'],
    'Education': ['Books', 'Fees', 'Others', 'Supplies', 'Tuition'],
    'Entertainment': ['Concerts', 'Events', 'Gaming', 'Hobbies', 'Movies', 'Parties', 'Shopping', 'Sports', 'Subscriptions', 'Travel', 'Others'],
    'Food': ['Breakfast', 'Lunch', 'Dinner', 'Alcohol', 'Dining Out', 'Drinks', 'Groceries', 'Snacks', 'Others'],
    'Housing': ['Building Management', 'Cable', 'Furniture/Decorations', 'Internet/Data', 'Maintenance/Repairs', 'Rent/Mortgage', 'Utilities', 'Others'],
    'Insurance': ['Car Insurance', 'Health Insurance', "Homeowner's/Renter's Insurance", 'Life Insurance', 'Other Insurances'],
    'Miscellaneous': ['Donations', 'Gifts', 'Unexpected Expenses'],
    'Personal': ['Clothing', 'Cosmetics', 'Fitness', 'Haircut', 'Health', "Pets", 'Religion', 'Others'],
    'Savings/Investments': ['Emergency Fund', 'Retirement', 'Other Investments'],
    'Transportation': ['Fuel', 'Parking/Tolls', 'Public Transit', 'Travel', 'Uber/Lyft', 'Vehicle Maintenance/Repairs', 'Others']
}

@app.after_request
def after_request(response):
    #Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    conn, db = connection()
    id = session["user_id"]
    try:
        budgets_ = db.execute("SELECT budget, period, start FROM users WHERE id = ?", (id,)).fetchall()
        budgets = to_dict(budgets_)[0]
    except:
        conn.close()
        return redirect("/setbudget")

    if budgets["period"] != None and budgets["start"] != None:
        budgets["period"] = display_period[budgets["period"]]
        budgets["start"] = get_last(budgets["start"], budgets["period"])
    else:
        conn.close()
        return redirect("/setbudget")

    #SQL
    expenses = to_dict(db.execute("SELECT * FROM expenses WHERE id = ? AND date >= ? ORDER BY date DESC, amount DESC", (id, budgets["start"])).fetchall())
    for expense in expenses:
        expense["amount"] = usd(expense["amount"])
    period_expenses = to_dict(db.execute("SELECT SUM(amount) as amount FROM expenses WHERE id = ? AND date >= ? ORDER BY date DESC, amount DESC", (id, budgets["start"])).fetchall())[0]
    total_expenses = to_dict(db.execute("SELECT SUM(amount) as amount FROM expenses WHERE id = ? ORDER BY date DESC, amount DESC", (id,)).fetchall())[0]

    incomes = to_dict(db.execute("SELECT * FROM income WHERE id = ? AND date >= ? ORDER BY date DESC, amount DESC", (id, budgets["start"])).fetchall())
    for income in incomes:
        income["amount"] = usd(income["amount"])
    period_incomes = to_dict(db.execute("SELECT SUM(amount) as amount FROM income WHERE id = ? AND date >= ? ORDER BY date DESC, amount DESC", (id, budgets["start"])).fetchall())[0]
    total_incomes = to_dict(db.execute("SELECT SUM(amount) as amount FROM income WHERE id = ? ORDER BY date DESC, amount DESC", (id,)).fetchall())[0]

    goals = to_dict(db.execute("SELECT * FROM goals WHERE id = ? ORDER BY deadline ASC, amount DESC", (id,)).fetchall())

    calculate = {}

    if not budgets["budget"]:
        budgets["budget"] = 0
    if not period_expenses["amount"]:
        period_expenses["amount"] = 0
    if not total_expenses["amount"]:
        total_expenses["amount"] = 0
    if not period_incomes["amount"]:
        period_incomes["amount"] = 0
    if not total_incomes["amount"]:
        total_incomes["amount"] = 0

    # calculation related part
    calculate["current_limit"] = usd(budgets["budget"] - period_expenses["amount"])
    calculate["current_save"] = usd(period_incomes["amount"] - period_expenses["amount"])
    calculate["total_savings"] = total_incomes["amount"] - total_expenses["amount"]

    # convert everything to usd
    budgets["budget"] = usd(budgets["budget"])

    period_expenses["amount"] = usd(period_expenses["amount"])
    total_expenses["amount"] = usd(total_expenses["amount"])

    period_incomes["amount"] = usd(period_incomes["amount"])
    total_incomes["amount"] = usd(total_incomes["amount"])

    # For progress bar
    for goal in goals:
        goal["now"] = calculate["total_savings"]/goal["amount"]*100
        goal["amount"] = usd(goal["amount"])

    calculate["total_savings"] = usd(calculate["total_savings"])
    conn.close()
    return render_template("index.html", goals = goals, expenses = expenses, incomes = incomes, budgets = budgets, period_expenses = period_expenses, total_expenses = total_expenses, period_incomes = period_incomes, total_incomes = total_incomes, calculate = calculate)

@app.route("/register", methods=["GET", "POST"])
def register():
    conn, db = connection()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            conn.close()
            return render_template("register.html", error = "must provide username")

        # Ensure password was submitted
        elif not password or not confirm:
            conn.close()
            return render_template("register.html", error = "must provide password")

        # Ensure passwords match each other
        elif password != confirm:
            conn.close()
            return render_template("register.html", error = "passwords do not match")

        # Query database for username to see if already exists
        result = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        if not result:
            # Adds new user to database
            db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", (username, generate_password_hash(password)))
            conn.commit()
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchall()[0]["id"]
            conn.close()
            return redirect("/")
        else:
            conn.close()
            return render_template("register.html", error="username already exists")
    conn.close()
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    
    conn, db = connection()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            conn.close()
            return render_template("login.html", error = "must provide username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            conn.close()
            return render_template("login.html", error = "must provide password")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            conn.close()
            return render_template("login.html", error = "invalid username and/or password")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        conn.close()
        return redirect("/")
    else:
        conn.close()
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/setbudget", methods=["GET", "POST"])
@login_required
def setbudget():
    # Connects to users.db database
    conn, db = connection()
    id = session["user_id"]
    budgets = db.execute("SELECT budget, period FROM users WHERE id = ?", (id,)).fetchall()
    copy = to_dict(budgets)
    print(copy)
    if len(copy) != 0:
        copy = copy[0]
        if copy["period"] != None and copy["budget"] != None:
            copy["period"] = display_period[copy["period"]]
            copy["budget"] = usd(copy["budget"])
        else:
            copy["period"] = 'day'
            copy["budget"] = usd(0)

    else:
        # Usually for newly registerd users
        copy = {}
        copy["period"] = 'day'
        copy["budget"] = usd(0)

    if request.method == "POST":
        period = request.form.get("period")
        try:
            amount = float(request.form.get("amount"))
        except:
            conn.close()
            return render_template("setbudget.html", budgets = copy, periods = periods, error = "invalid input")

        start = request.form.get("date")

        # Ensures proper inputs, similar processes in other routes as well
        if not period or not amount or not start or amount <= 0 or period not in periods:
            conn.close()
            return render_template("setbudget.html", budgets = copy, periods = periods, error = "invalid input")
        period = int(periods[period])

        try:
            db.execute("UPDATE users SET start = ?, period = ?, budget = ? WHERE id = ? ", (start, period, usd(amount), id))
            conn.commit()
        except:
            conn.close()
            return render_template("setbudget.html", budgets = copy, periods = periods, error = "invalid input")
        conn.close()
        return redirect("/")
    conn.close()
    return render_template("setbudget.html", budgets = copy, periods = periods)


@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    conn, db = connection()
    id = session["user_id"]
    goals = to_dict(db.execute("SELECT * FROM goals WHERE id = ? ORDER BY deadline ASC, amount DESC", (id,)).fetchall())
    for goal in goals:
        goal["amount"] = usd(goal["amount"])
    if request.method == "POST":
        item = request.form.get("item")
        try:
            amount = float(request.form.get("amount"))
        except:
            conn.close()
            return render_template("goals.html", goals = goals, error = "invalid input")

        deadline = request.form.get("date")
        if not item or not amount or not deadline or amount <= 0:
            conn.close()
            return render_template("goals.html", goals = goals, error = "invalid input")

        try:
            db.execute("INSERT INTO goals(id, item, amount, deadline) VALUES (?, ?, ?, ?)", (id, item, usd(amount), deadline))
            conn.commit()
        except:
            conn.rollback()
            conn.close()
            return render_template("goals.html", goals = goals, error = "invalid input")
        conn.close()
        return redirect("/goals")
    conn.close()
    return render_template("goals.html", goals = goals)


@app.route("/expenses", methods=["GET", "POST"])
@login_required
def spendings():
    conn, db = connection()
    id = session["user_id"]
    expenses = to_dict(db.execute("SELECT * FROM expenses WHERE id = ? ORDER BY date DESC, amount DESC", (id,)).fetchall())
    for expense in expenses:
        expense["amount"] = usd(expense["amount"])
    if request.method == "POST":
        date = request.form.get("date")
        try:
            amount = float(request.form.get("amount"))
        except:
            conn.close()
            return render_template("expenses.html", periods = periods, expenses = expenses, categories = categories, error = "invalid input")
        type_general = request.form.get('type_general')
        type_specific = request.form.get('type_specific')
        repeat = request.form.get("period")
        repeat_times = request.form.get("times")
        if repeat == "Repeats" or not repeat or not repeat_times:
            repeat = None
            repeat_times = None
        if not date or not amount or not type_general or not type_specific or amount <= 0:
            conn.close()
            return render_template("expenses.html", periods = periods, expenses = expenses, categories = categories, error = "invalid input")
        try:
            db.execute("INSERT INTO expenses(id, date, amount, type_general, type_specific, repeat, repeat_times) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, date, usd(amount), type_general, type_specific, repeat, repeat_times))
            conn.commit()
        except:
            conn.rollback()
            conn.close()
            return render_template("expenses.html", periods = periods, expenses = expenses, categories = categories, error = "invalid input")
        conn.close()
        return redirect("/expenses")
    conn.close()
    return render_template("expenses.html", periods = periods, expenses = expenses, categories = categories)



@app.route("/income", methods=["GET", "POST"])
@login_required
def earnings():
    conn, db = connection()
    id = session["user_id"]
    incomes = to_dict(db.execute("SELECT * FROM income WHERE id = ? ORDER BY date DESC, amount DESC", (id,)).fetchall())
    for income in incomes:
        income["amount"] = usd(income["amount"])
    if request.method == "POST":
        date = request.form.get("date")
        try:
            amount = float(request.form.get("amount"))
        except:
            conn.close()
            return render_template("income.html", periods = periods, incomes = incomes, income_types = income_types, error = "invalid input")

        type = request.form.get('type')
        repeat = request.form.get("period")
        repeat_times = request.form.get("times")

        if repeat == "Repeats" or not repeat or not repeat_times:
            repeat = None
            repeat_times = None
        if not date or not amount or not type or amount <= 0:
            conn.close()
            return render_template("income.html", periods = periods, incomes = incomes, income_types = income_types, error = "invalid input")
        try:
            db.execute("INSERT INTO income(id, date, amount, type, repeat, repeat_times) VALUES (?, ?, ?, ?, ?, ?)", (id, date, usd(amount), type, repeat, repeat_times))
            conn.commit()
        except:
            conn.rollback()
            conn.close()
            return render_template("income.html", periods = periods, incomes = incomes, income_types = income_types, error = "invalid input")
        conn.close()
        return redirect("/")
    conn.close()
    return render_template("income.html", periods = periods, incomes = incomes, income_types = income_types)
