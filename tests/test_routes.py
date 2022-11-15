"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
#from unittest.mock import MagicMock, patch

from urllib.parse import quote_plus
from service import app
from service.models import db, init_db, Product
from service.common import status  # HTTP Status Codes
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb")
BASE_URL = "/products"

######################################################################
#  T E S T   C A S E S
######################################################################


class TestProductServer(TestCase):
    """ Product Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_products(self, count):
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(
                BASE_URL, json=test_product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                             "Could not create test product")
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    # ######################################################################
    # #  P L A C E   T E S T   C A S E S   H E R E
    # ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Product REST API Service")

    def test_health(self):
        """It should be health"""
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

    def test_get_products(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_get_product_list_by_name(self):
        """It should Query Product by Name"""
        products = self._create_products(10)
        test_name = products[0].name
        name_products = [
            product for product in products if product.name == test_name]
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertNotEqual(len(data), len(name_products))
        # check the data
        for product in data:
            self.assertEqual(product["name"], test_name)

    def test_get_product_with_price(self):
        """Query Products by price"""
        test_product = ProductFactory()
        logging.debug(test_product)
        resp = self.client.post(
            BASE_URL, json=test_product.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        test_product = resp.get_json()

        resp = self.client.get(
            BASE_URL,
            query_string="price={}".format(test_product['price'])
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["name"], test_product['name'])
        self.assertEqual(data[0]["description"], test_product['description'])
        self.assertEqual(data[0]["price"], test_product['price'])

    def test_get_product_with_description(self):
        """Query Products by description"""
        test_product = ProductFactory()
        logging.debug(test_product)
        resp = self.client.post(
            BASE_URL, json=test_product.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        test_product = resp.get_json()

        resp = self.client.get(
            BASE_URL,
            query_string=f"description={test_product['description']}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["name"], test_product['name'])
        self.assertEqual(data[0]["description"], test_product['description'])
        self.assertEqual(data[0]["price"], test_product['price'])

    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(new_product["price"], test_product.price)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(new_product["price"], test_product.price)

    def test_update_product(self):
        """It should Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        logging.debug(new_product)
        new_product["name"] = "unknown_class"
        response = self.client.put(
            f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["name"], "unknown_class")

    def test_read_product_success(self):
        """It should Get an existing Product"""
        product = ProductFactory()
        product.create()
        url = "{}/{}".format(BASE_URL, product.id)

        resp = self.client.get(url)
        data = resp.get_json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], product.name)

    def test_delete_product(self):
        """It should Delete an existing Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_action(self):
        """It should change the like_num of an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        test_product.like_num = 0
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.get_json()["id"]

        # like the product
        response = self.client.put(f"{BASE_URL}/{product_id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["like_num"], 1)
        response = self.client.put(f"{BASE_URL}/{product_id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["like_num"], 2)

        # unlike the product
        response = self.client.put(f"{BASE_URL}/{product_id}/unlike")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["like_num"], 1)
        response = self.client.put(f"{BASE_URL}/{product_id}/unlike")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["like_num"], 0)
        response = self.client.put(f"{BASE_URL}/{product_id}/unlike")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["like_num"], -1)

    def test_on_shelf_action(self):
        """It should change the is_on_shelf of an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        test_product.is_on_shelf = False
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.get_json()["is_on_shelf"], False)
        product_id = response.get_json()["id"]

        # on shelf the product
        response = self.client.put(f"{BASE_URL}/{product_id}/on-shelf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["is_on_shelf"], True)

        # off shelf the product
        response = self.client.put(f"{BASE_URL}/{product_id}/off-shelf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["is_on_shelf"], False)

     ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################

    def test_read_product_not_found(self):
        """It should not Get a Product with bad id"""
        resp = self.client.get("{}/999".format(BASE_URL))

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product_no_data(self):
        """It should not Create a Product with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """It should not Create a Product with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_bad_price(self):
        """It should not Create a Product with bad price data"""
        test_product = ProductFactory()
        logging.debug(test_product)
        # change price to a string
        test_product.price = "price"
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_no_content_type(self):
        """It should not update a product with no content type"""
        response = self.client.put(BASE_URL+"/1")
        self.assertEqual(response.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_update_product_wrong_content_type(self):
        """It should not update a product with wrong content type"""
        response = self.client.put(
            BASE_URL+"/1", content_type='<p>hello boy</p>')
        self.assertEqual(response.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_update_product_non_existing(self):
        """It should not update an non-existing Product"""
        # make sure product not exist
        test_product = ProductFactory()
        test_product.id = 4567486
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # update the product
        response = self.client.put(
            f"{BASE_URL}/{test_product.id}", json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_action_on_product_non_existing(self):
        """It should not update an non-existing Product"""
        # make sure product not exist
        test_product = ProductFactory()
        test_product.id = 4567486
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.put(f"{BASE_URL}/{test_product.id}/like")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.put(f"{BASE_URL}/{test_product.id}/unlike")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_on_shelf_action_on_product_non_existing(self):
        """It should not update an non-existing Product"""
        # make sure product not exist
        test_product = ProductFactory()
        test_product.id = 4567486
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.put(f"{BASE_URL}/{test_product.id}/on-shelf")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.put(f"{BASE_URL}/{test_product.id}/off-shelf")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
