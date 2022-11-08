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
import constant
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    # Initialize the SQLAlchemy app
    Product.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


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
        db.String(constant.LENGTH_MAX_PRODUCT_DESC), nullable=True)
    price = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return "<Product %r id=[%s]>" % (self.name, self.id)

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
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            if (len(self.name) > constant.LENGTH_MAX_PRODUCT_NAME):
                raise DataValidationError(
                    "Invalid Product: Too long name string: "
                )
            self.description = data.get('description', '')
            if (len(self.description) > constant.LENGTH_MAX_PRODUCT_DESC):
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
        :type prodcut_id: int
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
    def find_by_attribute(cls, **kwargs) -> list:
        """Returns all Products with the given name
        :param name: the name of the Products you want to match
        :type name: str
        :return: a collection of Products with that name
        :type: list
        """
        # cls.query.filter(cls.name == name)
        # logger.info("Processing name query for %s ...", name)
        logger.info("Processing name query for %s ...", kwargs.get("description", ""))
        res = cls.query
        if kwargs.get("id") is not None:
            res = res.filter(Product.id == kwargs.get("id"))
        if kwargs.get("name") is not None:
            res = res.filter(Product.name == kwargs.get("name"))
        if kwargs.get("description") is not None:
            res = res.filter(Product.description == kwargs.get("description"))
        if kwargs.get("price") is not None:
            res = res.filter(Product.price == kwargs.get("price"))
        # return cls.query.filter(Product.name == kwargs.get("name")).filter(Product.description == kwargs.get("description"))
        return res