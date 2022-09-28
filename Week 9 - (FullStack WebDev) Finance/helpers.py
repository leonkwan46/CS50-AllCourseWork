import os
import requests
import urllib.parse

from flask import flash, redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def password_check(passwd):

    SpecialSym = ['$', '&', '!', '@', '#', '%', '^', '&', '*']
    val = True

    if len(passwd) < 6:
        flash("|| Length should be at least 6 || ")
        val = False

    if len(passwd) > 20:
        flash("|| Length should be not be greater than 8 || ")
        val = False

    if not any(char.isdigit() for char in passwd):
        flash("Password should have at least one numeral || ")
        val = False

    if not any(char.isupper() for char in passwd):
        flash("Password should have at least one uppercase letter || ")
        val = False

    if not any(char.islower() for char in passwd):
        flash("Password should have at least one lowercase letter || ")
        val = False

    if not any(char in SpecialSym for char in passwd):
        flash("Password should have at least one of the symbols $ & ! @ # % ^ * ||")
        val = False

    return val