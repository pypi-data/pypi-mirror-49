""" This module contains exceptions that are raise when there is an error
processing an item.
"""

class ItemProcessError(Exception):
    """ General exception for processing instances of
    :py:class:`~save_to_db.core.item_base.ItemBase` class.
    """


class ItemsNotTheSame(ItemProcessError):
    """ Raised when trying to merge items that cannot be merged during
    processing items in a bulk item that can potentially refer to
    the same record in a database.
    """

class ItemMustHaveTheSameIdentity(ItemProcessError):
    """ Raised when using "x-to-one" relationship, the item on the "one" side
    turns out to be different, for example:
    
    .. code-block:: Python
    
        item_one = ItemsOne(description='first')
        bulk_two = item['two_one_many']
        # the generated item must have reverse
        # relationship thorugh `one_x_1` field to the `item_one`
        item_two = bulk_two.gen(description='second')
        # but we set another item
        item_one['two_one_many'][0]['one_x_1'] = ItemsOne(description='third')
        
        # next line will set up the reverse relationship and raise the
        # exception
        item_one.process()
    """