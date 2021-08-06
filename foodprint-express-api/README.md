# Foodprint Express REST API

## Layers
- (M)VC Architectural Pattern
    - Controllers
      - Insights, Receipt Scanning, Search, User
    - Routes
      - Endpoints for above controllers
    - Queries
        - PSQL DB Config
    - Server
        - App entrypoint

## Setting up server
- Clone repo and run `npm i` in terminal
- Run `npm start` to open server at port:3000

## Setting Up PostgreSQL
- Create an `.env` file, with the following keys: `POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_HOST`

## User Routes
### GET /users/allUsers
Gets all users

**Example Fetch:**
`/users/allUsers`

**Response:**
- No users exist, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
    - Body response is all rows from PSQL users table
    
### POST /users/newUser
Posts a new user with the name, `req.body.name`

**Example Post:**
`/users/newUser`

**Example Payload:**
```json
{
    "name": "John Doe"
}
```

**Response:**
- Name not specified, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 201 CREATED
    - Body response is `message: User added`
    
### DEL /users/deleteUser
Deletes a user with the specified `req.body.id`

**Example Delete:**
`/users/deleteUser`

**Example Payload:**
```json
{
    "id": "507f191e810c19729de860ea"
}
```

**Response:**
- User does not exist, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
    - Body response is `message: User deleted`
 
 
## Search Routes
### GET /search/food
Gets the food item emissions and other relevant .csv data, given a food item

**Example Payload:**
```json
{
    "nlp_search": "banana"
}
```

**Response:**
- Food item not specified, does not exist, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
    - Body response is row from PSQL DB with searched food item emissions
 
 
## Receipt Scanning Routes
### POST /receipt/upload
Posts a new receipt image to have the data extracted and estimate emissions off averages

**Example Payload:**
```json
{
    "file_path": "C:/Users/123456789/Documents/loblaws_receipt.png"
}
```

**Response:**
- Invalid image or file type, invalid file path, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
    - Body response is `message: Receipt upload successful, receipt_id: uuid of receipt`
 
    
 ## Insights Routes
### GET /insights/get
Gets the insights from our data science models, given an existing receipt ID

**Example Payload:**
```json
{
    "receipt_id": "2e51ff35-b35e-416a-a0d7-e11347386987"
}
```

**Response:**
- Invalid receipt id, receipt with specified id does not exist, bad request
    - 400 Bad Request
    - Body response is `message: error`
- Otherwise ...
    - 200 OK
    - Body response is `message: Insight generated, insight: insight generated based off model for meat, non meat, and general`   
