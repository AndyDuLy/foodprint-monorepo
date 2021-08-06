# Foodprint Flask REST API

## Setting up server
- Clone repo and run the following commands to create a vitrual environment
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt 
```
- CD into the API folder and run `python emissions.py` and `python insights.py` to open server at port:5000 and 5001 respectively

## Setting Up PostgreSQL
- Create an `database.ini` file, with the following keys: `host, database, user, password`

## Emissions Routes
### POST /weighedemissions
Assign a carbon score to an item by its weight

**Example Fetch:**
`/weighedemissions`

**Response:**
- No users exist, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
    - List: [item_emissions, "HC_Category"] 

**Example Request**
- {"Salmon": "387.89"}

**Example Response**
- [1345.98, "Fish and Shellfish"]

### POST /unweighedemissions
Assign a carbon score to an item by its price

**Example Fetch:**
`/weighedemissions`

**Response:**
- No users exist, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
    - List: [item_emissions, "HC_Category"] 

**Example Request**
- {"Salmon": "387.89"}

**Example Response**
- [1345.98, "Fish and Shellfish"]


## Insights Routes
### POST /insights
Generates insights for meat items, non meat items, and general improvements

**Example Fetch:**
`/weighedemissions`

**Example Payload:**
```json
{
    "receipt_id": "2e51ff35-b35e-416a-a0d7-e11347386987"
}
```

**Response:**
- No receipt with that id exist, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
```json
{
    "meat_insights": "you can reduce your emissions by 1.5kg by switching to chicken",
    "no_meat_insight": "you can reduce your emissions by 2kg if you switch to vegetarian foods",
    "general_insights": "keep buying broccoli, it has lower co2 because it requires less pesticides"
}
```
