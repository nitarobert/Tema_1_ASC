"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """
    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove item_idations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs['name']

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            for action in cart:
                if action["type"] == "add":
                    cnt = 0
                    while cnt < action["quantity"]:
                        if self.marketplace.add_to_cart(cart_id, action["product"]) == 0:
                            sleep(self.retry_wait_time)
                            cnt -= 1
                        cnt += 1

                if action["type"] == "remove":
                    for cnt in range (action["quantity"]):
                        self.marketplace.remove_from_cart(cart_id, action["product"])

            final_cart = self.marketplace.place_order(cart_id)
            with self.marketplace.print_lock:
                for prod in final_cart:
                    print(f"{self.name} bought {prod}")
