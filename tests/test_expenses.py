def test_expense_calculation():

    expenses = [
        {"amount": 100},
        {"amount": 200},
        {"amount": 50}
    ]

    total = sum(expense["amount"] for expense in expenses)

    assert total == 350