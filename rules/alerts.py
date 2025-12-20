from analytics.spending import category_wise_spending
from utils.logger import logger

def category_spend_alert(threshold=10000):
    alerts = []
    data = category_wise_spending()

    for category, total in data:
        if total > threshold:
            alerts.append(
                f"⚠️ High spending in '{category}' category: ₹{total}"
            )

    return alerts
from analytics.spending import category_percentage_contribution


def rent_dominance_alert(limit_percent=40):
    alerts = []
    data = category_percentage_contribution()

    for category, percent in data:
        if category.lower() == "rent" and percent > limit_percent:
            alerts.append(
                f"⚠️ Rent accounts for {percent}% of total spending"
            )

    return alerts
from analytics.high_value import high_value_transactions


def high_value_transaction_alert(threshold=5000):
    alerts = []
    data = high_value_transactions(threshold)

    for txn_id, user_id, amount, category, txn_date in data:
        alerts.append(
            f"🚨 High-value transaction detected: "
            f"Txn {txn_id}, User {user_id}, ₹{amount}, "
            f"{category}, {txn_date}"
        )

    return alerts
def generate_all_alerts():
    alerts = []

    alerts.extend(category_spend_alert(threshold=10000))
    alerts.extend(rent_dominance_alert(limit_percent=40))
    alerts.extend(high_value_transaction_alert(threshold=5000))

    return alerts
