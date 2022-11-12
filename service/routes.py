"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from .common import status  # HTTP Status Codes
from service.models import Product

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(name="Product REST API Service",
                version="1.0",
                # paths=url_for("list_products", _external=True)
                ),
        status.HTTP_200_OK,
    )


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# LIST ALL PRODUCTS
######################################################################

@app.route("/products", methods=["GET"])
def list_products():
    """"Return all of the Products"""
    app.logger.info("Request for product list")
    products = []
    flag = False
    name = request.args.get("name")
    price = request.args.get("price")
    description = request.args.get("description")
    if name:
        app.logger.info('Filtering by name: %s', name)
        products = Product.find_by_name(name)
        flag = True
    if price:
        app.logger.info('Filtering by price: %s', price)
        products = Product.find_by_price(price)
        flag = True
    if description:
        app.logger.info('Filtering by description: %s', description)
        products = Product.find_by_description(description)
        flag = True

    if not flag:
        app.logger.info('Returning unfiltered list.')
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RETRIEVE A Product
######################################################################


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on it's id
    """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND,
              f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK

######################################################################
# ADD A NEW Product
######################################################################


@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for(
        "get_products", product_id=product.id, _external=True)

    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

# ######################################################################
# # UPDATE AN EXISTING Product
# ######################################################################


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product

    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to update Product with id: %s", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND,
              f"Product with id '{product_id}' was not found.")

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    app.logger.info("Product with ID [%s] updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a Product
    This endpoint will delete a Product based the body that is posted
    """
    app.logger.info("Request to delete Product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()

    app.logger.info("Product with ID [%s] delete complete.", product_id)
    return "", status.HTTP_204_NO_CONTENT


# ######################################################################
# # ACTIONS ON PRODUCT
# ######################################################################

@app.route("/products/<int:product_id>/like", methods=["PUT"])
def like_product(product_id):
    """
    like a Product
    This endpoint will add the like_num of the product
    """
    app.logger.info("Request to like Product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND,
              f"Product with id '{product_id}' was not found.")

    product.id = product_id
    product.like_num += 1
    product.update()

    app.logger.info("Product with ID [%s] add one like.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>/unlike", methods=["PUT"])
def unlike_product(product_id):
    """
    unlike a Product
    This endpoint will decrease the like_num of the product
    """
    app.logger.info("Request to like Product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND,
              f"Product with id '{product_id}' was not found.")

    product.id = product_id
    product.like_num -= 1
    product.update()

    app.logger.info("Product with ID [%s] decrease one like.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>/on-shelf", methods=["PUT"])
def on_shelf_product(product_id):
    """
    mark a Product as on sell
    """
    app.logger.info("Request to on shelf Product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND,
              f"Product with id '{product_id}' was not found.")

    product.is_on_shelf = True
    product.update()

    app.logger.info("Product with ID [%s] is on shelf.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>/off-shelf", methods=["PUT"])
def off_shelf_product(product_id):
    """
    mark a Product as off sell
    """
    app.logger.info("Request to off shelf Product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND,
              f"Product with id '{product_id}' was not found.")

    product.is_on_shelf = False
    product.update()

    app.logger.info("Product with ID [%s] is off shelf.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Product.init_db(app)


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s",
                     request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
