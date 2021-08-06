import flask
from flask.globals import request
from flask.wrappers import Response
import psycopg2
#!/usr/bin/python
from configparser import ConfigParser
import json, sys
from flask_cors import CORS
from numpy import number


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

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def receipt_items_query(string):
    """ query data from the receipt table"""
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT item_name, item_amount, item_emissions, item_category FROM receipt WHERE receipt_id = '{0}'".format(string))
        row = cur.fetchall()
        return row

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def packaged_meat_insight(list):
    '''
    Function checks if any items from a given reciept are considered "packaged meats". 
    If true, then the function will calculate the difference in emissions between packaged meats (i.e beef)
    and packaged poultry (i.e chicken) 
    
    Parameters:
        items (list): The list of items captured from the grocery receipt.
​
    Returns:
        savings_dict(dictionary): Returns a dictionary (for JSON) of CO2 saved and a brief description
    '''
    
    #list of all items classified as packaged meats
    packaged_meats = ['Buffalo', 'Beef', 'Lamb', 'Pork', 'Rabbit', 'Ham', 'Deli meats', 'Bacon', 'Steak', 'Hot dogs', 
                    'Hamburger (beef)', 'Ground sausage']
    
    #Counter for total emissions produced by meat from a receipt
    packaged_meat_total_emissions = 0
    provide_insight = False

    #Checks each item for any packaged meats
    for x in packaged_meats:
        for item in list:
            if item[0] == x:
                provide_insight = True
                packaged_meat_total_emissions += item[2]

    #If no items from the receipt are packaged meats, return no insight 
    if provide_insight == False:
        return ""
    
    #Calculate emissions saved switching from packaged meat to Chicken (packaged poultry)
    total_meat_dollar_value = round((packaged_meat_total_emissions/2.48), 2)
    packaged_poultry_multiplier = 0.947
    poultry_emissions = round((packaged_poultry_multiplier*total_meat_dollar_value), 2)

    #Create and return dictionary with strings containing insight 
    #Key: Exact CO2 savings
    #Value: Explanation 
    save_co2 = str(packaged_meat_total_emissions - poultry_emissions)
    savings_string = "Save " + save_co2 + "Kg of CO2 if you substitute Chicken for Beef"

    return savings_string

def general_insights(list):
    '''
    Function checks if any items from a given reciept are considered Broccoli, Nuts or Cabbage. 
    If true, then the function will return a general insight/tip for those items.
    
    Parameters:
        items (list): The list of items captured from the grocery receipt.
​
    Returns:
        insights(dictionary): Returns a dictionary of the general insights 
    '''
    number_of_insights = 0
    insights = []

    #Loops through all items in a receipt to identify Broccoli, Nuts or Cabbage
    for item in list: 
        if item[0] == "Broccoli":
            insight_string = "Keep on buying broccoli! It has lower relative CO2 emissions because it doesn’t require use of many pesticides"
            insights.append(insight_string)
            number_of_insights += 1
        elif item[0] == "Nuts":
            insight_string = "Great job buying nuts! Many nut producers are carbon negative even accounting for transportation and supply chain related emissions!"
            insights.append(insight_string)
            number_of_insights += 1
        elif item[0] == "Cabbage":
            insight_string = "Cabbage is the best! It has natural defences and doesn’t require as much fertilizer or pesticides to grow compared to other produce!"
            insights.append(insight_string)
            number_of_insights += 1

    return insights

def no_meat_insight(list):
    '''
    Function checks if any items from a given reciept are considered Meats or Fish. 
    If true, then the function will calculate the difference in emissions between Meats/Fish and vegetarian foods.
    
    Parameters:
        items (list): The list of items captured from the grocery receipt.
​
    Returns:
        savings_dict(dictionary): Returns a dictionary (for JSON) of CO2 saved and a brief description
    '''
    #Counter for total emissions produced by meat/fish from a receipt and item costs
    total_meat_emissions = 0
    total_item_cost = 0
    insight_string = ""

    #Checks each item for any Meats/Fish
    for item in list: 
        if item[3] == "Meat and Poultry" or item[3] == "Fish and Shellfish":
            total_meat_emissions += item[2]
            total_item_cost += item[1]

    average_fruit_veg_emissions = 0.78
    veg_emissions = average_fruit_veg_emissions * total_item_cost

    #Create and return dictionary with strings containing insight 
    #Key: Exact CO2 savings
    #Value: Explanation 
    savings = str(round((total_meat_emissions - veg_emissions), 2))
    insight_string = "Save " + savings + "Kg of CO2 if you eat only vegetarian foods instead of meats"

    return insight_string

@app.route('/', methods=['GET'])
def base():
    return "Base API working"

@app.route('/insights', methods=['POST'])
def insights():
    #Get product name and dollar amount purchased 
    receipt_json = json.loads(request.data)
    receipt_id = receipt_json["flask_req"]["receipt_id"]

    #query all items for the given receipt_id
    items_in_receipt = receipt_items_query(receipt_id)

    #dictionary to return 
    insights = {}

    #call all insight functions and add to the dictionary 
    meat_insight = packaged_meat_insight(items_in_receipt)
    nomeat_insight = no_meat_insight(items_in_receipt)
    generalinsight = general_insights(items_in_receipt)

    if meat_insight != "":
        insights['meat_insight'] = (meat_insight)
    else:
        insights['meat_insight'] = ("no meat insight")
    
    if nomeat_insight != "":
        insights['no_meat_insight'] = (nomeat_insight)
    else:
        insights['no_meat_insight'] = ("no non-meat insight")
    
    if generalinsight != []:
        insights['generalinsight'] = (generalinsight)
    else:
        insights['generalinsight'] = ("no general insight")

    #json conversion
    return_data = json.dumps(insights)
    return (return_data)
 
app.run(port=5001)