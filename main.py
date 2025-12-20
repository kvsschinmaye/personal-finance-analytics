from rules.alerts import generate_all_alerts
from analytics.spending import (
    category_wise_spending,
    category_percentage_contribution
)
from analytics.trends import monthly_spending_trend
from analytics.users import user_wise_spending
from analytics.high_value import high_value_transactions


def print_category_spending():
    print("\n📊 Category-wise Spending")
    print("-" * 30)
    data = category_wise_spending()
    for category, total in data:
        print(f"{category}: ₹{total}")


def print_category_percentage():
    print("\n📈 Category Contribution (%)")
    print("-" * 30)
    data = category_percentage_contribution()
    for category, percent in data:
        print(f"{category}: {percent}%")


def print_monthly_trend():
    print("\n🗓️ Monthly Spending Trend")
    print("-" * 30)
    data = monthly_spending_trend()
    for month, total in data:
        print(f"{month}: ₹{total}")


def print_user_spending():
    print("\n👤 User-wise Spending")
    print("-" * 30)
    data = user_wise_spending()
    for user_id, total in data:
        print(f"User {user_id}: ₹{total}")


def print_high_value_transactions(threshold=5000):
    print(f"\n🚨 High-Value Transactions (>{threshold})")
    print("-" * 30)
    data = high_value_transactions(threshold)
    for txn_id, user_id, amount, category, txn_date in data:
        print(
            f"Txn {txn_id} | User {user_id} | ₹{amount} | "
            f"{category} | {txn_date}"
        )


def print_alerts():
    print("\n🔔 Alerts")
    print("-" * 30)

    alerts = generate_all_alerts()
    if not alerts:
        print("No alerts triggered.")
    else:
        for alert in alerts:
            print(alert)


def main():
    print("\n=== Personal Finance Analytics Platform ===")

    print_category_spending()
    print_category_percentage()
    print_monthly_trend()
    print_user_spending()
    print_high_value_transactions(threshold=5000)

    # 🔥 PHASE B — Alerts Engine
    print_alerts()

    print("\n=== End of Analytics ===\n")


if __name__ == "__main__":
    main()
