"""
Models for Product
All of the models are stored in this module
Models
------
Product - the schema used in the product store
Attributes:
----------
id: integer - the id of the product (primary key)
name: string - the name of the product
description: string - the description for the product
price: integer - the price of the product
"""
import logging
from service.common import constant
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    # Initialize the SQLAlchemy app
    Product.init_db(app)


class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""


class DataValidationError(Exception):
    """Custom Exception with data validation fails"""


class Product(db.Model):
    """
    Class that represents a Product
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(constant.LENGTH_MAX_PRODUCT_NAME), nullable=False)
    description = db.Column(
        db.String(constant.LENGTH_MAX_PRODUCT_DESC))
    price = db.Column(db.Integer, default=0, nullable=False)
    like_num = db.Column(db.Integer, default=0)
    is_on_shelf = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Product from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Product into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "like_num": self.like_num,
            "is_on_shelf": self.is_on_shelf
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            if len(self.name) > constant.LENGTH_MAX_PRODUCT_NAME:
                raise DataValidationError(
                    "Invalid Product: Too long name string: "
                )
            self.description = data.get('description', '')
            if len(self.description) > constant.LENGTH_MAX_PRODUCT_DESC:
                raise DataValidationError(
                    "Invalid Product: Too long description string: "
                )
            if isinstance(data['price'], float) or isinstance(data['price'], int):
                self.price = data['price']
            else:
                raise DataValidationError(
                    "Invalid Product: invalid type for price: "
                    + str(type(data['price'] + " instead of [int/float]"))
                )
            self.like_num = data.get('like_num', 0)
            self.is_on_shelf = data.get('is_on_shelf', True)
        except KeyError as error:
            raise DataValidationError(
                "Invalid product: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data. " +
                "Error: " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app: Flask):
        """ Initializes the database session

        :param app: the Flask app
        :type data: Flask
        """
        logger.info("Initializing database")
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        # db.drop_all()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """ Returns all of the products in the database """
        logger.info("Processing all products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """ Finds a Product by it's ID
        :param: product_id: the id of the Product to find
        :type: product_id: int
        :return: an instance with the product_id, or None if not found
        :rtype: Product
        """
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id: int):
        """Find a Product by it's id
        :param product_id: the id of the Product to find
        :type product_id: int
        :return: an instance with the product_id, or 404_NOT_FOUND if not found
        :rtype: Product
        """
        logger.info("Processing lookup or 404 for id %s ...", product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Products with the given name
        :param name: the name of the Products you want to match
        :type name: str
        :return: a collection of Products with that name
        :type: list
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_price(cls, price: int) -> list:
        """Returns all Products whose price are lower or equal to the given price
        :param price: the price of the Products you want to match
        :type price: int
        :return: a collection of Products with lower or equal price
        :rtype: list
        """
        logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price <= price)

    @classmethod
    def find_by_description(cls, description: str) -> list:
        """Returns all Products with the given description
        :param description: the description of the Products you want to match
        :type description: str
        :return: a collection of Products with that description
        :rtype: list
        """
        logger.info("Processing description query for %s ...", description)
        return cls.query.filter(cls.description.like(f"%{description}%"))
