# This is the project for our products team

## Important: Before you submit a pull request. Make sure
- Run `nosetest` to make sure that all tests are passed and code coverage are no less than 95%
- Run `make lint` to make sure that there is no Pylint error.


## Reminder: Whenever you make changes to the table schema. Run `flask create-db` to sync the database

## Run `flask run` to start the service. If you want to clean the database, run `flask create-db`.

## Product table schema
```
{
      id: auto_generated            Int           Primary key
      name: product_name1           String
      description: description      String
      price: 1.1                    Float
}
```

**List of REST API endpoints**
----
```
POST   /products <- Create a product
GET    /products     <- List all products
GET    /products/{id} <- Read a product 
PUT    /products/{id} <- Update a product
DELETE /products/{id} <- Delete a product
```

**Create a product**
----

* **URL**

  POST /products

* **Request Headers:**
Content-Type: application/json
* **Body:**

  ```json
  {
    "price": "1.1",
    "description": "description"
  }
  ```
 
* **Success Response:**

  * **Code:** HTTP_201_CREATED <br />
    **Content:** 
    ```json
    { 
      "id" : 1, 
      "price" : 1.1, 
      "description": "description" 
    }
    ```

* **Error Response:**

  * **Code:** HTTP_409_CONFLICT <br />
    **Content:** 
    ```json
    {
      "error": "Conflict",
      "message": "409 Conflict: Product 1 already exists",
      "status": 409
    }
    ```


**Update a product**
----
  Update a product by id

* **URL**

  PUT /products/<product_id>

* **Request Headers:**
Content-Type: application/json
* **Body:**

  ```json
  [{
      "price": 2,
      "description": "description"
  }]
  ```
 
* **Success Response:**

  * **Code:** HTTP_201_CREATED <br />
    **Content:** 
    ```json
    {
        "id": 1,
        "price": 2,
        "description": "description"
    }
    ```

* **Error Response:**

  * **Code:** HTTP_404_NOT_FOUND <br />
    **Content:** 
    ```json
    {
    "error": "NOT Found",
    "message": "404 NOT FOUND: Product 1 not found",
    "status": 404
    }
    ```

**Read a product**
----
  Read a product by product_id

* **URL**

  GET /products/<user_id>

* **Request Headers:**
NULL
* **Body:**
NULL
 
* **Success Response:**

  * **Code:** HTTP_200_OK <br />
    **Content:** 
    ```json
    {
        "id": 1,
        "price": 2,
        "description": "description"
    }
    ```

* **Error Response:**

  * **Code:** HTTP_404_NOT_FOUND <br />
    **Content:** 
    ```json
    {
    "error": "Not Found",
    "message": "404 Not Found: Product with id '11' was not found.",
    "status": 404
    }
    ```

**Read all products**
----
  Read all products in table

* **URL**

  GET /products

* **Request Headers:**
NULL
* **Body:**
NULL
 
* **Success Response:**
* **Code:** HTTP_200_OK <br />
    **Content:** 
    ```json
    [
        {
            "id": 1,
            "price": 2,
            "description": "description"
        },
        {
            "id": 2,
            "price": 2,
            "description": "description"
        }
    ]
    ```

* **Error Response:**
NULL

**Delete a product**
----
  Delete a product by product_id

* **URL**
    
    DELETE /products/<product_id>

* **Request Headers:**
NULL
* **Body:**
NULL
 
* **Success Response:**

  * **Code:** HTTP_204_NO_CONTENT <br />
    **Content:** 
    NO_CONTENT

* **Error Response:**
NULL
