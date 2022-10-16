"""
Models for YourResourceModel

All of the models are stored in this module

Models
------
Product - the schema used in the product store

Attributes:
----------
id: integer - the id of the product (primary key)
name: string - the name of the product
description: string - the description for the product
price: float - the price of the product
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import date

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    # Initialize the SQLAlchemy app
    Product.init_db(app)

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Product(db.Model):
    """
    Class that represents a YourResourceModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Float, default=0.0)


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

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]

            id=data.get("id","")
            if isinstance(id,int) or (id and type(eval(price)==int)):
                self.id=id
            else:
                raise DataValidationError(
                "Invalid Product: invalid type for id - should be in integera " 
                )

            self.description = data['description']

            price=data.get("price","")
            if isinstance(price,float) or (price and type(eval(price)==float)):
                self.price=price
            else:
                raise DataValidationError(
                "Invalid Product: invalid type for price - should be in float " 
                )

        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data - "
                "Error message: " + error
            )
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
    def find(cls, product_id:int):
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
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

       
        :param name: the name of the Products you want to match
        :type name: str

        :return: a collection of Products with that name
        :type: list
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
