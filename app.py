from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = os.urandom(24)

accounts = {}
DATA_FILE = "accounts.txt"


def save_accounts():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for acc_no, data in accounts.items():
            history_str = "|".join(data["history"])
            line = f"{acc_no},{data['name']},{data['balance']},{data['pin']},{data['email']},{history_str}\n"
            f.write(line)


def load_accounts():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    acc_no = int(parts[0])
                    name = parts[1]
                    balance = int(parts[2])
                    pin = parts[3]
                    email = parts[4]
                    history = parts[5].split("|") if parts[5] else []
                    accounts[acc_no] = {
                        "name": name,
                        "balance": balance,
                        "pin": pin,
                        "email": email,
                        "history": history
                    }
    except FileNotFoundError:
        pass


load_accounts()


def generate_account_number():
    acc_no = random.randint(10000000, 99999999)
    while acc_no in accounts:
        acc_no = random.randint(10000000, 99999999)
    return acc_no


def get_current_user():
    return session.get("account_number")


def require_login():
    acc_no = get_current_user()
    if not acc_no or acc_no not in accounts:
        flash("Please login first", "error")
        return None
    return acc_no


def send_account_email(to_email, name, acc_no):
    sender_email = os.environ.get("BANK_EMAIL")
    app_password = os.environ.get("BANK_EMAIL_PASS")

    if not sender_email or not app_password:
        print("Email credentials not set.")
        return

    subject = "Welcome to Lootera Bank"
    body = f"""
Hello {name},

Your Lootera Bank account has been created successfully.

Your Account Number: {acc_no}

Please keep this number safe. Never share your PIN.

– Lootera Bank
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email failed but app continues:", e)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            acc_no = int(request.form.get("account_number", ""))
            pin = request.form.get("pin", "")

            if acc_no not in accounts or accounts[acc_no]["pin"] != pin:
                flash("Invalid credentials", "error")
                return render_template("login.html")

            session["account_number"] = acc_no
            session["user_name"] = accounts[acc_no]["name"]
            return redirect(url_for("dashboard"))

        except ValueError:
            flash("Invalid account number", "error")

    return render_template("login.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        try:
            initial_deposit = int(request.form.get("initial_deposit", ""))
        except ValueError:
            flash("Invalid deposit amount", "error")
            return render_template("create.html")

        pin = request.form.get("pin", "")
        confirm_pin = request.form.get("confirm_pin", "")

        if not name or not email:
            flash("All fields are required", "error")
            return render_template("create.html")

        if initial_deposit <= 0:
            flash("Deposit must be greater than 0", "error")
            return render_template("create.html")

        if len(pin) != 4 or not pin.isdigit() or pin != confirm_pin:
            flash("Invalid PIN setup", "error")
            return render_template("create.html")

        acc_no = generate_account_number()
        accounts[acc_no] = {
            "name": name,
            "balance": initial_deposit,
            "pin": pin,
            "email": email,
            "history": [f"Account created with ₹{initial_deposit}"]
        }
        save_accounts()
        send_account_email(email, name, acc_no)

        session["account_number"] = acc_no
        session["user_name"] = name

        flash(f"Account created! Your account number is {acc_no}. It has been emailed to you.")
        return redirect(url_for("dashboard"))

    return render_template("create.html")


@app.route("/dashboard")
def dashboard():
    acc_no = require_login()
    if not acc_no:
        return redirect(url_for("login"))

    user_data = accounts[acc_no]
    return render_template("dashboard.html",
                           account_number=acc_no,
                           name=user_data["name"],
                           balance=user_data["balance"])


@app.route("/deposit", methods=["POST"])
def deposit():
    acc_no = require_login()
    if not acc_no:
        return redirect(url_for("login"))

    amount = int(request.form.get("amount", 0))
    if amount > 0:
        accounts[acc_no]["balance"] += amount
        accounts[acc_no]["history"].append(f"Deposited ₹{amount}")
        save_accounts()
        flash(f"₹{amount} deposited successfully")

    return redirect(url_for("dashboard"))


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    acc_no = require_login()
    if not acc_no:
        return redirect(url_for("login"))

    if request.method == "POST":
        amount = int(request.form.get("amount", 0))
        if 0 < amount <= accounts[acc_no]["balance"]:
            accounts[acc_no]["balance"] -= amount
            accounts[acc_no]["history"].append(f"Withdrew ₹{amount}")
            save_accounts()
            flash(f"₹{amount} withdrawn successfully")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid amount or insufficient balance", "error")

    return render_template("withdraw.html", balance=accounts[acc_no]["balance"])


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    acc_no = require_login()
    if not acc_no:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            recipient_acc = int(request.form.get("recipient_account", ""))
            amount = int(request.form.get("amount", ""))
        except ValueError:
            flash("Invalid input", "error")
            return render_template("transfer.html", balance=accounts[acc_no]["balance"])

        if recipient_acc not in accounts:
            flash("Recipient account not found", "error")
            return render_template("transfer.html", balance=accounts[acc_no]["balance"])

        if recipient_acc == acc_no:
            flash("You cannot transfer to your own account", "error")
            return render_template("transfer.html", balance=accounts[acc_no]["balance"])

        if amount <= 0:
            flash("Amount must be greater than 0", "error")
            return render_template("transfer.html", balance=accounts[acc_no]["balance"])

        if amount > accounts[acc_no]["balance"]:
            flash("Insufficient balance", "error")
            return render_template("transfer.html", balance=accounts[acc_no]["balance"])

        accounts[acc_no]["balance"] -= amount
        accounts[recipient_acc]["balance"] += amount

        accounts[acc_no]["history"].append(f"Transferred ₹{amount} to {recipient_acc}")
        accounts[recipient_acc]["history"].append(f"Received ₹{amount} from {acc_no}")

        save_accounts()
        flash(f"Successfully transferred ₹{amount}")
        return redirect(url_for("dashboard"))

    return render_template("transfer.html", balance=accounts[acc_no]["balance"])


@app.route("/history")
def history():
    acc_no = require_login()
    if not acc_no:
        return redirect(url_for("login"))

    return render_template("history.html", transactions=accounts[acc_no]["history"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
