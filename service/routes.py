"""
My Service

Describe what your service does here
"""
import secrets
from flask import jsonify, request, url_for, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from service.models import DataValidationError, DatabaseConnectionError
from service.common import error_handlers, status    # HTTP Status Codes
from .common import status  # HTTP Status Codes
from service.models import Product

from . import app, api


######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return app.send_static_file('index_temp.html')


    # id = db.Column(db.Integer, primary_key=True)
# Define the model so that the docs reflect what can be sent
create_model = api.model('Product', {
    'name': fields.String(required=True,
                          description='The name of the Product'),
    'description': fields.String(required=False,
                                 description='The description of the Product'),
    'price': fields.Integer(required=True,
                            description='The price of the Product'),
    'like_num': fields.Integer(description='Peoples\' votes to this product'),
    'is_on_shelf': fields.Boolean(description='Is the Product is currently ready to sale?')
})

product_model = api.inherit(
    'ProductModel',
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, required=False, location='args',
                          help='Find the Product by name')
product_args.add_argument('description', type=str, required=False, location='args',
                          help='List Products contains specified description')
product_args.add_argument('price', type=int, required=False, location='args',
                          help='List Products which has a price less than or equal to input')

######################################################################
# GET HEALTH CHECK
######################################################################


@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# Authorization Decorator
######################################################################
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'X-Api-Key' in request.headers:
#             token = request.headers['X-Api-Key']

#         if app.config.get('API_KEY') and app.config['API_KEY'] == token:
#             return f(*args, **kwargs)
#         else:
#             return {'message': 'Invalid or missing token'}, 401
#     return decorated


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return secrets.token_hex(16)


######################################################################
#  PATH: /products/{id}
######################################################################
@api.route('/products/<product_id>')
@api.param('product_id', 'The Product identifier')
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single product
    GET /products/{id} - Returns a product with the id
    PUT /products/{id} - Update a product with the id
    DELETE /products/{id} -  Deletes a product with the id
    """
    # ------------------------------------------------------------------
    # RETRIEVE A PRODUCT
    # ------------------------------------------------------------------
    @api.doc('get_product')
    @api.response(404, 'product not found')
    @api.marshal_with(product_model)
    def get(self, product_id):
        """
        Retrieve a single Product

        This endpoint will return a Product based on it's id
        """
        app.logger.info(
            "Request to Retrieve a product with id [%s]", product_id)
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND,
                  "Product with id '{}' was not found.".format(product_id))
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PRODUCT
    # ------------------------------------------------------------------
    @api.doc('update_product')
    @api.response(404, 'Product not found')
    @api.response(400, 'The posted Product data was not valid')
    @api.expect(create_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """
        Update a Product

        This endpoint will update a Product based the body that is posted
        """
        app.logger.info('Request to Update a product with id [%s]', product_id)
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND,
                  "Product with id '{}' was not found.".format(product_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        product.deserialize(data)
        product.id = product_id
        product.update()
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PRODUCT
    # ------------------------------------------------------------------
    @api.doc('delete_product')
    @api.response(204, 'Product deleted')
    def delete(self, product_id):
        """
        Delete a Product

        This endpoint will delete a Product based the id specified in the path
        """
        app.logger.info('Request to Delete a product with id [%s]', product_id)
        product = Product.find(product_id)
        if product:
            product.delete()
            app.logger.info('Product with id [%s] was deleted', product_id)

        return '', status.HTTP_204_NO_CONTENT

######################################################################
#  PATH: /products
######################################################################


@api.route('/products', strict_slashes=False)
class ProductCollection(Resource):
    """ Handles all interactions with collections of Products """
    # ------------------------------------------------------------------
    # LIST ALL PRODUCTS
    # ------------------------------------------------------------------
    @api.doc('list_products')
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """"Return all of the Products"""
        app.logger.info("Request for product list")
        products = []
        args = product_args.parse_args()
        if args['name']:
            app.logger.info('Filtering by name: %s', args['name'])
            products = Product.find_by_name(args['name'])
        elif args['price']:
            app.logger.info('Filtering by price: %s', args['price'])
            products = Product.find_by_price(args['price'])
        elif args['description']:
            app.logger.info('Filtering by description: %s',
                            args['description'])
            products = Product.find_by_description(args['description'])
        else:
            app.logger.info('Returning unfiltered list.')
            products = Product.all()
       
        results = [product.serialize() for product in products]
        app.logger.info("Returning %d products", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PRODUCT
    # ------------------------------------------------------------------
    @api.doc('create_a_product')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a Product
        This endpoint will create a Product based the data in the body that is posted
        """
        app.logger.info("Request to create a product")
        product = Product()
        app.logger.debug('Payload = %s', api.payload)
        product.deserialize(api.payload)
        product.create()
        app.logger.info("Product with ID [%s] created.", product.id)
        location_url = api.url_for(
            ProductResource, product_id=product.id, _external=True)
        return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

# ######################################################################
# # ACTIONS ON PRODUCT
# ######################################################################
@api.route('/products/<product_id>/like')
@api.param('product_id', 'The Product identifier')
class LikeProduct(Resource):
    """ Like action on a Product """
    @api.doc('like_products')
    @api.response(404, 'Product not found')
    def put(self, product_id):
        """
        Like a Product
        This endpoint will increase the like_num of the Product
        """
        app.logger.info('Request to like a Product')
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, 'Product with id [{}] was not found.'.format(product_id))

        product.id = product_id
        product.like_num += 1
        product.update()

        app.logger.info('Product with id [%s] has been liked!', product.id)
        return product.serialize(), status.HTTP_200_OK


@api.route('/products/<product_id>/unlike')
@api.param('product_id', 'The Product identifier')
class UnlikeProduct(Resource):
    """ Unlike action on a Product """
    @api.doc('unlike_products')
    @api.response(404, 'Product not found')

    def put(self, product_id):
        """
        Unlike a Product
        This endpoint will decrease the like_num of the Product
        """
        app.logger.info('Request to unlike a Product')
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, 'Product with id [{}] was not found.'.format(product_id))

        product.id = product_id
        product.like_num -= 1
        product.update()

        app.logger.info('Product with id [%s] decrease one like', product.id)
        return product.serialize(), status.HTTP_200_OK


@api.route('/products/<product_id>/on-shelf')
@api.param('product_id', 'The Product identifier')
class OnshelfProduct(Resource):
    """
    mark a Product as on sell
    """
    @api.doc('onshelf_products')
    @api.response(404, 'Product not found')
    def put(self, product_id):
        """
        Onshelf a Product
        This endpoint will onshelf the Product
        """
        app.logger.info('Request to onshelf a Product')
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, 'Product with id [{}] was not found.'.format(product_id))

        product.is_on_shelf = True
        product.update()

        app.logger.info('Product with id [%s] is now onshelf', product.id)
        return product.serialize(), status.HTTP_200_OK

@api.route('/products/<product_id>/off-shelf')
@api.param('product_id', 'The Product identifier')
class OffshelfProduct(Resource):
    """
    mark a Product as off sell
    """
    @api.doc('offshelf_products')
    @api.response(404, 'Product not found')
    def put(self, product_id):
        """
        Offshelf a Product
        This endpoint will offshelf the Product
        """
        app.logger.info('Request to offshelf a Product')
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, 'Product with id [{}] was not found.'.format(product_id))

        product.is_on_shelf = False
        product.update()

        app.logger.info('Product with id [%s] is now offshelf', product.id)
        return product.serialize(), status.HTTP_200_OK

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

# def abort(error_code: int, message: str):
#     """Logs errors before aborting"""
#     app.logger.error(message)
#     api.abort(error_code, message)

def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Product.init_db(app)