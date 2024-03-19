import sqlite3

import requests as requests
from flask import Flask, request, jsonify

def get_db_connection():
    conn = sqlite3.connect('orders.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/purchase/<ItemNum>' , methods = ['GET'])
def orders(ItemNum):
    base_url = 'http://localhost:5000/query'
    response = requests.get(base_url, params={'item_number': ItemNum})

    if response.ok:
        data = response.json()
        if data['Count'] <= 0:
            return jsonify({'purchase' : "this book is out of stock" })

        response = requests.patch('http://localhost:5000/update' , json = {'stock_count' : -1
                                                                ,'item_number' : data['ItemNumber']})
        if response.json() == "Updated record successfully":
            con = get_db_connection()
            con.cursor().execute("Insert Into 'order' (item_number) values (" + ItemNum + ")")
            con.commit()
            return jsonify({'message' : 'successfully purchased number =' + ItemNum})
        else:
            return jsonify({'message' : 'failure purchased number =' + ItemNum})
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code




if __name__ == '__main__':
    app.run(debug=True ,host= '0.0.0.1' ,port=5060)

