from flask import Flask, request, jsonify
from flask_cors import CORS

# import the functions to get data from finance.py
from functions.finance import getData

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes


@app.route("/", methods=["POST"])
async def get_data():
    # get data from request
    # indicator exmple : 'AAPL', 'MSFT', 'GOOG'
    # start date example : '2010-01-01'
    # end date example : '2023-01-25'
    # montant initial example : 1000
    # montant recurant example : 100

    data = request.get_json()

    indicator = data["indicator"]
    startDate = data["startDate"]
    endDate = data["endDate"]
    montantInitial = float(data["montantInitial"])
    montantRecurant = float(data["montantRecurant"])

    revenueStats = getData(
        indicator, startDate, endDate, montantInitial, montantRecurant
    )

    return jsonify(revenueStats), 200


if __name__ == "__main__":
    app.run(debug=True)
