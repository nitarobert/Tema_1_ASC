"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from dataclasses import dataclass
from threading import Lock
import logging
from logging.handlers import RotatingFileHandler

from tema.product import Product


LOG_HANDLER = RotatingFileHandler('marketplace.log', maxBytes=10000, backupCount=5)
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s: '
                              '%(message)s -- %(filename)s::%(funcName)s'''
                              ' line     %(lineno)d', '%b %d %H:%M:%S')
FORMATTER.converter = time.gmtime
LOG_HANDLER.setFormatter(FORMATTER)
LOGGER = logging.getLogger()
LOGGER.addHandler(LOG_HANDLER)
LOGGER.setLevel(10)


@dataclass(init=True, repr=True, order=False, frozen=True)
class Item:
    """
    An item is a product object - contains both the product and
    product`s producer_id
    """
    product: Product
    producer_id: int


class Marketplace:
    """
    Class that represents the Marketplace.
    """
    FIRST_ID = "0"

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.avb_products, self.producer_ids, self.carts_ids = [] , [] , []
        self.published_products_count, self.carts = {} , {}
        self.avb_products_lock, self.print_lock = Lock() , Lock()

        LOGGER.info("\n\n%s\n", 'Starting a new test')

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        if not self.producer_ids:
            self.producer_ids.append(self.FIRST_ID)
            LOGGER.debug(f"First producer`s id is {self.FIRST_ID}" )
            return self.FIRST_ID

        last_id = self.producer_ids[-1]
        self.producer_ids.append(f"{int(last_id)+1}")
        LOGGER.debug(f"Producer`s id is {self.producer_ids[-1]}")
        return self.producer_ids[-1]

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        producer_id = int(producer_id)
        LOGGER.debug(f"Producer`s id is {producer_id}")

        if producer_id not in self.published_products_count:
            self.published_products_count[producer_id] = 0

        if self.published_products_count[producer_id] < self.queue_size_per_producer:
            self.published_products_count[producer_id] += 1
            cnt_item = Item(product, producer_id)
            self.avb_products.append(cnt_item)
            LOGGER.debug(f"Published item is {product} {producer_id}")
            return True

        LOGGER.debug("%s", 'Can`t Publish')
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        if not self.carts_ids:
            self.carts_ids.append(self.FIRST_ID)
            self.carts[int(self.FIRST_ID)] = []
            LOGGER.debug("First cart`s id is %s", self.FIRST_ID)
            return self.FIRST_ID

        last_id = int(self.carts_ids[-1])
        self.carts_ids.append(str(last_id + 1))
        self.carts[last_id + 1] = []
        LOGGER.debug(f"Cart`s id is {last_id + 1}")
        return str(last_id + 1)

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        cart_id = int(cart_id)
        cnt = 0

        with self.avb_products_lock:
            for item in self.avb_products:
                if item.product == product:
                    self.avb_products.remove(item)
                    self.published_products_count[item.producer_id] -= 1
                    self.carts[cart_id].append(item)
                    cnt = 1
                    LOGGER.debug(f"Added item is {item.product} {item.producer_id}")
                    break

        if not cnt:
            return False

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        cart_id = int(cart_id)

        with self.avb_products_lock:
            for item in self.carts[cart_id]:
                if item.product == product:
                    self.carts[cart_id].remove(item)
                    self.published_products_count[item.producer_id] += 1
                    self.avb_products.append(item)
                    LOGGER.debug(f"Returned item is {item.product} {item.producer_id}")
                    return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        LOGGER.debug(f"Place order for cart {cart_id}")
        return [i.product for i in self.carts[int(cart_id)]]
