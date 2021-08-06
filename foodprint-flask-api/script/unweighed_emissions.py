import psycopg2
#!/usr/bin/python
from configparser import ConfigParser
import json, sys

# Change database.ini file path to your local path
def config(filename='/Users/562812701/Documents/goodside-amplify-flask/database.ini', section='postgresql'):
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
    """ query data from the individual_food_emissions table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT eio_emission_intensity, hc_main_category FROM individual_food_emissions WHERE display_name = '{0}'".format(string))
        row = cur.fetchone()

        return row

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':

    #Get product name and dollar amount purchased
    receipt_json = json.load( sys.stdin )

    product = ""
    amount = 0
    for key,value in receipt_json.items():
        product = key
        amount = value

    #query db to receive EIO emission and product category
    emission_query = get_emissions(product)

    #store query into variables
    eio_emission_intensity = emission_query[0]
    product_category = emission_query[1]

    #Calculate emission intensity * dollar value of product from receiot
    total_product_emission = (float(eio_emission_intensity))*(float(amount))

    #list to return
    list = []
    list.append(round(total_product_emission, 2))
    list.append(product_category)

    #json conversion
    return_data = json.dumps(list)
    sys.stdout.write(return_data)
