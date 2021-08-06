import flask
from flask.globals import current_app
from flask.wrappers import Response
import psycopg2
#!/usr/bin/python
from configparser import ConfigParser
import json, sys
from flask import Flask, request
from flask_cors import CORS

"""
Weighed
Request -  dict: '{"item_name": "weight"}'            eg. {"Salmon": "387.89"}
Response -  List: [item_emissions, "HC_Category"]     eg. [1345.98, "Fish and Shellfish"]

Unweighed
Request -  dict: '{"item_name": "dollar_amount"}'     eg. {"Salmon": "7.89"}
Response -  List: [item_emissions, "HC_Category"]     eg. [27.38, "Fish and Shellfish"]

Parameters
item_name = The product name after it's been NLP matched to the dataset
Weight = Weight given on the receipt for the product I.e 0.456kg @ $1.75 etc
dollar_amount = the cost of the item from the receipt
item_emission = The calculated emissions for the item
Hc_category = The category which is going to be display on the UI i.e Fish and Shellfish
"""

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


# Change database.ini file path to your local path
def config(filename='/Users/346990047/repos/amp2021-flask-api/goodside-amplify-flask/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_emissions(string):
    """ query data from the individual_food_emissions table"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT c_emission_intensity, hc_main_category FROM individual_food_emissions WHERE display_name = '{0}'".format(string))
        row = cur.fetchone()

        return row

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@app.route('/', methods=['GET'])
def base():
    return "Base API working"

@app.route('/weighedemissions', methods=['POST'])
def weighed_emissions():

    # load request
    response = json.loads(request.data)
    receipt_json = response["emissions"]

    product = ""
    weight = 0
    list = []

    for i in range(len(receipt_json)):
        # Get product name and dollar amount purchased   
        product = receipt_json[i]["choice"]
        weight = receipt_json[i]["price"]                       # update

        #query db to receive EIO emission and product category
        emission_query = get_emissions(product)

        #store query into variables
        individual_c_emission_intensity = emission_query[0]
        product_category = emission_query[1]

        if product_category == "":
            product_category = "Miscellaneous"

        #Calculate emission intensity * dollar value of product from receiot
        total_product_emission = (float(individual_c_emission_intensity))*(float(weight))

        #list to return
        list.append(round(total_product_emission, 2))
        list.append(product_category)


    return json.dumps(list)


@app.route('/unweighedemissions', methods=['POST'])
def unweighed_emissions():

    # load request
    response = json.loads(request.data)
    receipt_json = response["obj"]["emission"]

    product = ""
    amount = 0
    list = []
    dict = {}

    for i in range(len(receipt_json)):
        # Get product name and dollar amount purchased   
        product = receipt_json[i]["choice"]
        amount = receipt_json[i]["price"]
        sku = receipt_json[i]["sku"]
        
        # query db to receive EIO emission and product category
        emission_query = get_emissions(product)

        # store query into variables
        eio_emission_intensity = emission_query[0]
        product_category = emission_query[1]
        
        if product_category == "":
            product_category = "Miscellaneous"

        # Calculate emission intensity * dollar value of product from receiot
        total_product_emission = (float(eio_emission_intensity))*(float(amount))
        rounded_emissions = round(total_product_emission, 2)

        # Custom Object for each line item
        curr_line_item = {}
        curr_line_item['product'] = (product)
        curr_line_item['amount'] = (amount)
        curr_line_item['rounded_emissions'] = (rounded_emissions)
        curr_line_item['product_category'] = (product_category)
        curr_line_item['sku'] = (sku)

        # #list to return
        list.append(curr_line_item)

    dict['list'] = list
    return(dict)

 
app.run(port=5000)