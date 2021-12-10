from flask import Flask, jsonify
#from redis import Redis, StrictRedis, RedisError
import json
import click
from flask.cli import with_appcontext
import sys
import random
import requests
import hashlib
import math

app = Flask(__name__)
#redis = StrictRedis('redis-server', 6379, charset="utf-8", decode_responses=True)

#@click.command()
#@click.option("--hasho", default = "", help="Returns MD5 Hash String")
#@click.option("--n", default = 0, help="Returns Factorial of Inputed Integer")
#@click.option("--fibo", default = 0, help="Returns Fibonacci Number")
#@click.option("--prime", default = 0, help="Returns Whether Number is Prime or Not")


@app.route("/md5/<string:hasho>")
def return_md5(hasho):
    hash_object = hashlib.md5()
    hash_object.update(hasho.encode('utf-8'))
    md5_hash = hash_object.hexdigest()
    return jsonify({'input': hasho,
                    'output': md5_hash})

@app.route("/factorial/<int:n>")
def show_factorial(n):
    if n == 0:
        return jsonify({'input': n,
        'output': 1})
    else:
        return jsonify({'input': n,
        'output': math.factorial(int(n))})
    
#From fibonacci file
@app.route("/fibonacci/<int:fibo>")
def show_fibonacci(fibo):
    num_list = [i for i in range(0, fibo + 1)]
    fib_num = [0, 1]
    return_string = ""
    while fib_num[-1] <= fibo:
        new_fib = fib_num[-1] + fib_num[-2]
        fib_num.append(new_fib)
        
    fib_num = fib_num[1:-1]

    common_num = set(num_list).intersection(set(fib_num))
    total = len(common_num)

    for i in sorted(common_num):
        return_string += str(i) + ','

    return jsonify({'input': fibo,
    'output': return_string})

#From isPrime file
@app.route("/is-prime/<int:prime>")
def show_prime(prime):
    if prime < 2:
        return jsonify({'input': prime,
        'output': "true"})
    else:
        for n in range(2,prime):
            if prime % n == 0:
               return jsonify({'input': prime,
               'output': "false"})
            else:
                return jsonify({'input': prime,
                'output': "true"})


@app.route("/slack-alert/<string:user_message>")
def send_alert(user_message):
    output_string = "false"
    
    url = "https://hooks.slack.com/services/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"
    message = user_message
    title = "It Worked!"
    slack_data = {
        "username": "Group7-Bot",
        "icon_emoji": ":satellite:",
        #"channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    if response.status_code == 200:
        output_string = "true"

    return jsonify({'input': user_message,
        'output': output_string})


@app.cli.command("hashcom", help = "Returns MD5 Hash String; flask hasho [string]", short_help = "Returns MD5 Hash String; flask hasho [string]")
@click.argument("hasho", type=str)
def hashcom(hasho):
    hash_object = hashlib.md5()
    hash_object.update(hasho.encode('utf-8'))
    md5_hash = hash_object.hexdigest()
    print('input:', hasho)
    print('output:', md5_hash)
    

@app.cli.command("factcom", help = "Returns Factorial of Inputed Integer; flask facto [int]", short_help = "Returns Factorial of Inputed Integer; flask facto [int]")
@click.argument("facto", type=int)
def factcom(facto):
    if facto == 0:
        print('input:', facto)
        print('output:', 1)
    else:
        print('input:', facto)
        print('output:', math.factorial(int(facto)))

@app.cli.command("fibcom", help = "Returns Fibonacci Number; flask fibo [int]", short_help = "Returns Fibonacci Number; flask fibo [int]")
@click.argument("fibo", type=int)
def fibcom(fibo):
    num_list = [i for i in range(0, fibo + 1)]
    fib_num = [0, 1]
    return_string = ""
    while fib_num[-1] <= fibo:
        new_fib = fib_num[-1] + fib_num[-2]
        fib_num.append(new_fib)
        
    fib_num = fib_num[1:-1]

    common_num = set(num_list).intersection(set(fib_num))
    total = len(common_num)

    for i in sorted(common_num):
        return_string += str(i) + ','

    print('input:', fibo)
    print('output', return_string)
   

@app.cli.command("primecom", help = "Returns Whether Number is Prime or Not; flask prime [int]", short_help = "Returns Whether Number is Prime or Not; flask prime [int]")
@click.argument("prime", type=int)
def primecom(prime):
    if prime < 2:
        print('input:', prime)
        print('output:', "true")
    else:
        for n in range(2,prime):
            if prime % n == 0:
               print('input:', prime)
               print('output:', "false")
               return 0
            else:
                print('input:', prime)
                print('output:', "true")
                return 0


#app.cli.add_command(hashcom)
#app.cli.add_command(factcom)
#app.cli.add_command(fibcom)
#app.cli.add_command(primecom)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) 