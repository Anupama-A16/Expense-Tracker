from flask import Flask, render_template, request, redirect

from app.expenses import (
    add_expense_to_database,
    get_all_expenses,
    delete_expense_from_database,
    update_expense_in_database
)

app = Flask(__name__)


@app.route("/")
def home():
    expenses = get_all_expenses()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form["category"]

    add_expense_to_database(title, amount, category)

    return redirect("/")

@app.route("/edit/<int:expense_id>")
def edit(expense_id):
    expenses = get_all_expenses()

    for expense in expenses:
        if expense[0] == expense_id:
            return render_template("edit.html", expense=expense)

    return "Expense not found", 404


@app.route("/update/<int:expense_id>", methods=["POST"])
def update(expense_id):
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form["category"]

    update_expense_in_database(
        expense_id,
        title,
        amount,
        category
    )

    return redirect("/")


@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    delete_expense_from_database(expense_id)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)