# This is the project for our products team

## Important: Before you submit a pull request. Make sure
- Run `nosetest` to make sure that all tests are passed and code coverage are no less than 95%
- Run `make lint` to make sure that there is no Pylint error.


## Reminder: Whenever you make changes to the table schema. Run `flask create-db` to sync the database

## Run `flask run` to start the service. If you want to clean the database, run `flask create-db`.

Product table schema

```
{
      id: auto_generated            Int           Primary key
      user_id: user_id1             String        foreign key
      product_id: product_id1       String        key
      quantity: product_quantity1   Float
      name: product_name1           String
      price: price1                 Float
      time: purchase_time1          Date
}
```

Products table schema

```
Products schema
{
      id: auto_generated          Int          Primary key
      user_id: user_id1           String       unique
}
```

## List of REST API endpoints

```

```

## Create a product
Create a product by used_id and product detail

- **URL**

POST /shopcarts/<user_id>/items

- **Request Headers**: Content-Type: application/json

- **Body**:

```
{
    "id": 85265765, 
    "name": "airPods",
    "description": "headphone developed by Apple", 
    "price": 149
}
```

- **Success Response**:

    - **Code**: HTTP_201_CREATED
    
        **Content**:
    ```
    {
    "id": 85265765, 
    "name": "airPods",
    "description": "headphone developed by Apple", 
    "price": 149
    }
    ```
- **Error Response**: 
    - **Code**: HTTP_409_CONFLICT
        **Content**:
        ```
        {
         "error": "Conflict",
         "message": "409 Conflict: Product airPods already exists",
         "status": 409
        }
        ```

## Update a product

Update a product by user_id and product_id and product detail

- **URL**

PUT /shopcarts/<user_id>

- **Request Headers**: Content-Type: application/json

- **Body**:

```
{
    "id": 85265765, 
    "name": "airPods",
    "description": "headphone developed by Apple", 
    "price": 149
}
```

- **Success Response**:

    - **Code**: HTTP_200_OK
        **Content**:
        ```
        {
         "id": 85265765, 
         "name": "airPods",
         "description": "headphone developed by Apple", 
         "price": 149
        }
        ```
        
- **Error Response**:

    - **Code**: HTTP_404_NOT_FOUND
        **Content**:
        ```
        {
         "error": "Not Found",
         "message": "404 Not Found: Product with id 21 was not found.",
         "status": 404
        }
        ```
        

## Read a product
Read a shopcart by user_id and product_id

- **URL**

GET /shopcarts/<user_id>/items/<product_id>

- **Request Headers**: NULL

- **Body**: NULL

- **Success Response**:

    - **Code**: HTTP_200_OK

        Content:
        ```
        {
             "id": 85265765, 
             "name": "airPods",
             "description": "headphone developed by Apple", 
             "price": 149
        }
        ```
- **Error Response**:

    - **Code**: HTTP_404_NOT_FOUND
        
        Content:
        ```
        {
          "error": "Not Found",
          "message": "404 Not Found: Product with id 1 was not found in shopcart 1.",
          "status": 404
        }
        ```




## Read all products
Read all product in table

- **URL**

GET /shopcarts/<user_id>/items

- **Request Headers**: NULL

- **Body**: NULL

- **Success Response**:

    -**Code**: HTTP_200_OK
        Content:

       ```
        [
        {
           "id": 85265765, 
           "name": "airPods",
           "description": "headphone developed by Apple", 
           "price": 149
         },
        {
           "id": 85265765, 
           "name": "airPods",
           "description": "headphone developed by Apple", 
           "price": 149
        }
        ]
        ```

- **Error Response**:

    - **Code**: HTTP_404_NOT_FOUND
        Content:
        ```
        {
         "error": "Not Found",
         "message": "404 Not Found: Product with id '11' was not found.",
         "status": 404
        }
        ```

## Update a product

Update a product by user_id and product_id and product detail

- **URL**

PUT /shopcarts/<user_id>

- **Request Headers**: Content-Type: application/json

- **Body**:

```
{
    "id": 85265765, 
    "name": "airPods",
    "description": "headphone developed by Apple", 
    "price": 149
}
```

- **Success Response**:

    - **Code**: HTTP_200_OK
        Content:
        ```
        {
            "id": 85265765, 
            "name": "airPods",
            "description": "headphone developed by Apple", 
            "price": 149
        }
        ```
- **Error Response**:

    - **Code**: HTTP_404_NOT_FOUND
        Content:
        ```
        {
         "error": "Not Found",
         "message": "404 Not Found: Product with id 21 was not found in shopcart 1.",
         "status": 404
        }
        ```

## Delete a product
Delete a product by user_id and product_id

- **URL**

DELETE /shopcarts/<user_id>/items/<product_id>

- **Request Headers**: NULL

- **Body**: NULL

- **Success Response**:

    - **Code**: HTTP_204_NO_CONTENT
        Content: NO_CONTENT
- **Error Response**:

    - **Code**: HTTP_404_NOT_FOUND
        Content:
        ```
        {
            "error": "Not Found",
            "message": "404 Not Found: Product with id 3 was not found in shopcart 2.",
            "status": 404
        }
        ```
