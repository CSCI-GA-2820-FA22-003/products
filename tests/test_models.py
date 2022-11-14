import os
import logging
import unittest
from service.models import Product, DataValidationError, db
from service import app
from tests.factories import ProductFactory
import constant

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods


class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(id=85265765, name="airPods",
                          description="headphone developed by Apple", price=149)
        self.assertEqual(str(product), "<Product airPods id=[85265765]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, 85265765)
        self.assertEqual(product.name, "airPods")
        self.assertEqual(product.description, "headphone developed by Apple")
        self.assertEqual(product.price, 149)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(id=85265765, name="airPods",
                          description="headphone developed by Apple", price=149)
        self.assertTrue(product is not None)
        self.assertEqual(product.id, 85265765)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should Read a product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        logging.debug(product)
        self.assertIsNotNone(product.id)
        # Change it an save it
        product.name = "airPods2"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.name, "airPods2")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].name, "airPods2")

    def test_update_a_product_without_id(self):
        """It should not update a Product without id"""
        product = ProductFactory()
        logging.debug(product)
        product.create()
        product.id = None
        self.assertIsNone(product.id)
        # save it
        self.assertRaises(DataValidationError, product.update)

    def test_delete_a_product(self):
        """It should Delete a Products"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        # Create 5 Products
        for _ in range(5):
            product = ProductFactory()
            product.create()
        # See if we get back 5 products
        products = product.all()
        self.assertEqual(len(products), 5)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_or_404_found(self):
        """It should Find or return 404 not found"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()

        product = product.find_or_404(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.description, products[1].description)
        self.assertEqual(product.price, products[1].price)

    def test_find_by_price(self):
        """Find a Product by Price"""
        Product(name="K8S", description="Service", price=100).create()
        Product(name="REST", description="Requirement", price=50).create()
        products = Product.find_by_price(50)
        self.assertEqual(products[0].name, "REST")
        self.assertEqual(products[0].description, "Requirement")
        self.assertEqual(products[0].price, 50)

    def test_find_by_description(self):
        """Find a Product by Description"""
        Product(name="K8S", description="Good Service", price=100).create()
        Product(name="REST", description="Requirement", price=50).create()
        products = Product.find_by_description("Service")
        self.assertEqual(products[0].name, "K8S")
        self.assertEqual(products[0].description, "Good Service")
        self.assertEqual(products[0].price, 100)

    def test_serialize_a_product(self):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("description", data)
        self.assertEqual(data["description"], product.description)
        self.assertIn("price", data)
        self.assertEqual(data["price"], product.price)

    def test_deserialize_a_product(self):
        """It should de-serialize a Project"""
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.price, data["price"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        data = {"id": 1, "name": "jewelry", "description": "diamond"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)
        data = 1234
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_price(self):
        """It should not deserialize a bad price attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["price"] = "12345"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_too_long_name(self):
        """It should not deserialize a too long name attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["name"] = 's' * (constant.LENGTH_MAX_PRODUCT_NAME + 1)
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_too_long_desc(self):
        """It should not deserialize a too long desc attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["description"] = "s" * (constant.LENGTH_MAX_PRODUCT_DESC + 1)
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)
