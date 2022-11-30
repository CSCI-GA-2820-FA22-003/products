# NYU DevOps Fall 22 Project Products Team

[![Passing](https://img.shields.io/badge/TDD%20tests-Passing-green.svg)](https://github.com/CSCI-GA-2820-FA22-003/products/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

## Overview

This project contains code for class project products microservice. The `/service` folder contains `models.py` file for database model and a `routes.py` file for REST API service. The `/tests` folder has a test cases file `test_model.py` for databse model, and `test_routes.py` for testing API routes.

## Setup
Using the following code to setup the repository on your machine:

```
git clone https://github.com/nyu-devops-fall22-products/products.git
cd products
code .
```
Then Visual Studio Code will be opened. Select `Reopen In Container` to open it in the preset Docker environment.

To run tests for database models and routes, run the command: `nosetests -v --with-spec --spec-color`

To launch the service, run the command: `make run`

## Deploy the Microservice to IBM Cloud Kubernetes

Firstly, if you don't have a IBM Cloud Kubernetes Cluster, go to https://cloud.ibm.com/kubernetes/catalog/create to create one.

As a first step, go to https://cloud.ibm.com/iam to create a API KEY so that you can use IBM Cloud CLI to control your resources. Save the `apikey.json` file to `~/.products` (create this folder if you don't have one).

Open Visual Studio Code and enter the Dev Container environment according to the instruction above. If you have opened and built a docker container of an older version, you need to rebuild and reopen the container.

Run `make login` to login to IBM Cloud

Run `make build` to build a docker image that can be used for production deployment. There new image will have two tags: `latest` and the trimmed git commit hash of the current commit. Run `make image-push` to push the image to `nyu-devops-products` IBM Cloud Container Registry. If you are deploying this application to your own account, you need to create a container registry namespace and modify everywhere that use `nyu-devops-products` to your own registry namespace.

Run `make deploy` to deploy the app to Kubernetes. The service will be deployed to two namespaces: `dev` and `prod`. You can modify `deployment.yaml` file to choose the image you want to deploy for each namespace.

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

## Github Action CI

Every Pull Request should guarantee to pass all tests first before it is merged into master.


## Product table schema
```
{
      id: auto_generated              Int           Primary key
      name: "product_name1"           String
      description: "description"      String
      price: 1.1                      Float
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
    "name": "airPods"
    "price": "1.1",
    "description": "description"
  }
  ```
 
* **Success Response:**

  * **Code:** HTTP_201_CREATED <br />
    **Content:** 
    ```json
    { 
      "name": "airPods"
      "id" : 1, 
      "price" : 1.1, 
      "description": "description" 
    }
    ```

* **Error Response:**

  * **Code:** HTTP_415_UNSUPPORTED_MEDIA_TYPE <br />
    **Content:** 
    ```json
    {
      "error": "Unsupported media type",
      "message": "415 Unsupported Media Type: Content-Type must be application/json",
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
  {
      "price": 2,
      "description": "description",
      "name": "airPods"
  }
  ```
 
* **Success Response:**

  * **Code:** HTTP_201_CREATED <br />
    **Content:** 
    ```json
    {
        "name": "airPods"
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
        "name": "airPods"
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
  
  GET /products/?name=

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
            "name": "airPods"
            "id": 1,
            "price": 2,
            "description": "description"
        },
        {
            "name": "airPods2"
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

## Just Test Github Webhook Trigger

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
