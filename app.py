from flask import Flask
from flask import jsonify, request
app = Flask(__name__)

def change(amount):
    # calculate the resultant change and store the result (res)
    res = []
    coins = [1,5,10,25] # value of pennies, nickels, dimes, quarters
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}

    # divide the amount*100 (the amount in cents) by a coin value
    # record the number of coins that evenly divide and the remainder
    coin = coins.pop()
    num, rem  = divmod(int(amount*100), coin)
    # append the coin type and number of coins that had no remainder
    res.append({num:coin_lookup[coin]})

    # while there is still some remainder, continue adding coins to the result
    while rem > 0:
        coin = coins.pop()
        num, rem = divmod(rem, coin)
        if num:
            if coin in coin_lookup:
                res.append({num:coin_lookup[coin]})
    return res

def new_change(amount):
    
    old_change = change(amount)
    new_change = []
    
    for old_item in old_change:
        new_dict = {}
        for dict_item in old_item.items():
            new_dict[str(int(dict_item[0])*100)] = dict_item[1]
        new_change.append(new_dict)
        
    return new_change


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Hello World! I can make change at route: /change'

@app.route('/change/<dollar>/<cents>')
def changeroute(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    result = change(float(amount))
    return jsonify(result)

@app.route('/newchange/<dollar>/<cents>')
def newchangeroute(dollar, cents):
    print(f"Make New Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    result = new_change(float(amount))
    return jsonify(result)

@app.route('/jsonchange', methods=['POST'])
def json_example():
    
    request_data = request.get_json()
    if request_data:
        if 'amount' in request_data:
            return jsonify(change(float(request_data['amount'])))

    return 'Unknown JSON request'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
