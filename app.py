import re
from flask import Flask, jsonify, request
from sheets import Sheets
import constants

app = Flask(__name__)


@app.route("/budget/api/email", methods=["POST"])
def parse_email():
    payload = request.json
    body = payload["body"]
    subject = payload["subject"]
    sheet = Sheets()
    print(repr(body))

    if "Your purchase was successful" in subject:
        description = extract("(?<= at )(.*)(?= was successful)", body)
        amount = extract("(?<=Your purchase of )(.*)(?=\ at)", body)
        category = assign_cat_card(description)
        method = "BRIM"
        sheet.add_expense(description, amount, category, method)

    elif "BMO Credit Card Alert" in subject:
        description = extract("(?<= at )(.*)(?= was approved)", body)
        amount = extract("(?<= in the amount of )(.*)(?= at)", body)
        category = assign_cat_card(description)
        method = "BMO"
        sheet.add_expense(description, amount, category, method)
        
    return jsonify({"success": "true"})


def extract(regex, body):
    result = re.search(regex, body)
    return "NOT FOUND" if result is None else result.group()


def assign_cat_card(description):
    for store in constants.STORES.keys():
        if store in description.lower():
            return constants.STORES[store]
    return "NOT FOUND"


if __name__ == "__main__":
    app.run()
