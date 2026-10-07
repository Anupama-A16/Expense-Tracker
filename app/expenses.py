from app.database import get_connection

# Function to add an expense
def add_expense_to_database(title, amount, category):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO expenses (title, amount, category)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (title, amount, category))
    connection.commit()

    cursor.close()
    connection.close()


# Function to view all expenses
def get_all_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, title, amount, category
        FROM expenses
    """

    cursor.execute(query)
    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses


# Function to update an expense
def update_expense_in_database(expense_id, title, amount, category):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE expenses
        SET title = %s, amount = %s, category = %s
        WHERE id = %s
    """

    cursor.execute(query, (title, amount, category, expense_id))
    connection.commit()

    cursor.close()
    connection.close()


# Function to delete an expense
def delete_expense_from_database(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = "DELETE FROM expenses WHERE id = %s"

    cursor.execute(query, (expense_id,))
    connection.commit()

    cursor.close()
    connection.close()


# Function to view expense summary
def expense_summary():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """

    cursor.execute(query)

    category_totals = cursor.fetchall()

    if not category_totals:
        print("No expenses found.")
        cursor.close()
        connection.close()
        return

    total = 0

    print("\nExpenses by Category:")

    for category, amount in category_totals:
        print(f"{category}: ₹{amount:.2f}")
        total += amount

    print(f"\nTotal Expenses: ₹{total:.2f}")

    cursor.close()
    connection.close()
