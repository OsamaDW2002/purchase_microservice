import sqlite3

import requests as requests
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('purchase/<param1>' , methods = ['GET'])
def orders(param1):
    base_url = 'http://localhost:5000/query'
    response = requests.get(base_url, params={'item_number': param1})  # Ensuring proper URL encoding

    if response.ok:
        data = response.json()
        if data['count'] <= 0:
            return jsonify({'purchase' : "this book is out of stock" })
        response = requests.patch('http://localhost:5050/update' , json = {'stock_count' : -1
                                                                ,'item_number' : data['ItemNumber']})
        if response == "Updated record successfully":
            return jsonify({'purchase' : 'successfuly'})
        else:
            return jsonify({'purchase': 'Failed'})
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code



if __name__ == '__main__':
    app.run(debug=True ,host= '0.0.0.0' ,port=5060)

