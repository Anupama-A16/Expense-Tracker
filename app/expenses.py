from database import get_connection

# Function to add an expense
def add_expense():
    while True:
        title = input("Enter expense title: ").strip()
        if title:
            break
        print("Title cannot be empty.")

    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        category = input("Enter category: ").strip()
        if category:
            break
        print("Category cannot be empty.")

    connection = get_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO expenses (title, amount, category)
        VALUES (%s, %s, %s)
    """
    values = (title, amount, category)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    print("Expense added successfully!")


# Function to view all expenses
def view_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, title, amount, category
        FROM expenses
    """

    cursor.execute(query)

    expenses_from_db = cursor.fetchall()

    if not expenses_from_db:
        print("No expenses found.")
    else:
        for expense in expenses_from_db:
            print(
                f"ID: {expense[0]} | "
                f"{expense[1]} - "
                f"₹{expense[2]} - "
                f"{expense[3]}"
            )

    cursor.close()
    connection.close()


# Function to update an expense
def update_expense():
    connection = get_connection()
    cursor = connection.cursor()

    # Show existing expenses
    query = """
        SELECT id, title, amount, category
        FROM expenses
    """

    cursor.execute(query)

    expenses_from_db = cursor.fetchall()

    if not expenses_from_db:
        print("No expenses found.")
        cursor.close()
        connection.close()
        return

    for expense in expenses_from_db:
        print(
            f"ID: {expense[0]} | "
            f"{expense[1]} - "
            f"₹{expense[2]} - "
            f"{expense[3]}"
        )

    try:
        expense_id = int(input("Enter expense ID to update: "))
    except ValueError:
        print("Please enter a valid ID.")
        cursor.close()
        connection.close()
        return

    # Find the selected expense
    selected_expense = None

    for expense in expenses_from_db:
        if expense[0] == expense_id:
            selected_expense = expense
            break

    if selected_expense is None:
        print("Expense ID not found.")
        cursor.close()
        connection.close()
        return

    print("Leave the field empty to keep the current value.")

    new_title = input(
        f"Enter new title [{selected_expense[1]}]: "
    ).strip()

    new_amount = input(
        f"Enter new amount [{selected_expense[2]}]: "
    ).strip()

    new_category = input(
        f"Enter new category [{selected_expense[3]}]: "
    ).strip()

    # Keep old values if user leaves fields empty
    if not new_title:
        new_title = selected_expense[1]

    if not new_amount:
        new_amount = selected_expense[2]
    else:
        try:
            new_amount = float(new_amount)

            if new_amount <= 0:
                print("Amount must be greater than 0.")
                cursor.close()
                connection.close()
                return

        except ValueError:
            print("Invalid amount.")
            cursor.close()
            connection.close()
            return

    if not new_category:
        new_category = selected_expense[3]

    # Update MySQL
    query = """
        UPDATE expenses
        SET title = %s,
            amount = %s,
            category = %s
        WHERE id = %s
    """

    values = (
        new_title,
        new_amount,
        new_category,
        expense_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Expense updated successfully!")


# Function to delete an expense
def delete_expense():
    connection = get_connection()
    cursor = connection.cursor()

    # Show existing expenses
    query = """
        SELECT id, title, amount, category
        FROM expenses
    """

    cursor.execute(query)

    expenses_from_db = cursor.fetchall()

    if not expenses_from_db:
        print("No expenses found.")
        cursor.close()
        connection.close()
        return

    for expense in expenses_from_db:
        print(
            f"ID: {expense[0]} | "
            f"{expense[1]} - "
            f"₹{expense[2]} - "
            f"{expense[3]}"
        )

    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        cursor.close()
        connection.close()
        return

    query = """
        DELETE FROM expenses
        WHERE id = %s
    """

    cursor.execute(query, (expense_id,))

    if cursor.rowcount == 0:
        print("Expense ID not found.")
    else:
        connection.commit()
        print("Expense deleted successfully!")

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
