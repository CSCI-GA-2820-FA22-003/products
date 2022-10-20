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
    "user_id": "1",
    "product_id": "2",
    "name": "haha",
    "quantity": 12,
    "price": 1,
    "time": "2020-12-12"
}
```

- **Success Response**:

    - **Code**: HTTP_201_CREATED
    
        **Content**:
    ```
    {
    "id": 1,
    "name": "haha",
    "price": 1.0,
    "product_id": "2",
    "quantity": 12.0,
    "time": "2020-12-12",
    "user_id": "1"
    }
    ```
- **Error Response**: 
    - **Code**: HTTP_409_CONFLICT
        **Content**:
        ```
        {
         "error": "Conflict",
         "message": "409 Conflict: Shopcart 1 already exists",
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
    "user_id": "1",
    "product_id": "2",
    "name": "xixi",
    "quantity": 131,
    "price": 2,
    "time": "2020-12-13"
}
```

- **Success Response**:

    - **Code**: HTTP_200_OK
        **Content**:
        ```
        {
           "id": 2,
           "name": "xixi",
           "price": 2.0,
           "product_id": "2",
           "quantity": 131.0,
           "time": "2020-12-13",
           "user_id": "1"
        }
        ```
        
- **Error Response**:

    - **Code**: HTTP_404_NOT_FOUND
        **Content**:
        ```
        {
         "error": "Not Found",
         "message": "404 Not Found: Product with id 21 was not found in shopcart 1.",
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
            "id": 2,
            "name": "xixi",
            "price": 2.0,
            "product_id": "2",
            "quantity": 13.0,
            "time": "2020-12-13",
            "user_id": "1"
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
        "id": 2,
        "name": "xixi",
        "price": 2.0,
        "product_id": "2",
        "quantity": 13.0,
        "time": "2020-12-13",
        "user_id": "1"
         },
        {
        "id": 3,
        "name": "haha",
        "price": 1.0,
        "product_id": "3",
        "quantity": 12.0,
        "time": "2020-12-12",
        "user_id": "1"
        }
        ]
        ```

- **Error Response**:

    - **Code**: HTTP_404_NOT_FOUND
        Content:
        ```
        {
         "error": "Not Found",
         "message": "404 Not Found: Shopcart with id '11' was not found.",
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
    "user_id": "1",
    "product_id": "2",
    "name": "xixi",
    "quantity": 131,
    "price": 2,
    "time": "2020-12-13"
}
```

- **Success Response**:

    - **Code**: HTTP_200_OK
        Content:
        ```
        {
         "id": 2,
         "name": "xixi",
         "price": 2.0,
         "product_id": "2",
         "quantity": 131.0,
         "time": "2020-12-13",
         "user_id": "1"
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



















## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
