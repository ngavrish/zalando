"""
Smoke Tests collection.

Scenarios:
 - Login/Logout/Login
 - Creating new Order, Dispatchin, Undispatching, Removing
 - Click through available Daily Reports through the last month and validate their content container loaded successfully

"""
import time
from datetime import datetime

import pytest


@pytest.mark.usefixtures('tearupdown')
@pytest.mark.parametrize(('Name', 'Steps', "user", "search_item"),
                         [('Add item to wishlist',
                           ["- Go to zalando website www.zalando.de",
                            "- Go to the Search box and search for article DK151H09R-Q11",
                            "- Add it to the cart",
                            "- Go to the cart and change the quantity to 2",
                            "- Move the items from the basket to the wishlist."],

                           {"username": "nikikikita@gmail.com", "password": "abcABC123"},
                           "DK151H09R-Q11")])
def test_wishlist(Name, Steps, user, search_item):
    pytest.search.search_by_code(search_item)
    pytest.sellable_item.add2cart()
    pytest.page.goto_cart()
    pytest.cart.change_quantity(2)
    pytest.cart.add2wishlist(user)
    pytest.cart.validate_cart_empty()
    pytest.page.goto_wishlist()
    pytest.wishlist.validate_sellable_item(None)
    pytest.wishlist.clear_items()

