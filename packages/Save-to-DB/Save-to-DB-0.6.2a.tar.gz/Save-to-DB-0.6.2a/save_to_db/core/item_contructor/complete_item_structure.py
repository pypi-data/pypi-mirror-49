from collections import defaultdict
from .merge_items import merge_items
from ..item_base import ItemBase
from save_to_db.exceptions import (MultipleItemsMatch,
                                   ItemMustHaveTheSameIdentity,)


def complete_item_structure(item):
    """ Takes an item, completes reverse relationships inside it and
    return a dictionary like this:
    
        .. code-block:: Python
            
            {
                item_cls: [item_instance, ...],
                ...
            }
            
    Where keys are a subclasses of :py:class:`~.item.Item` and values are
    instances of that class.
    """
    top_item = item
    structure = defaultdict(list)  # item class to a list of instances
    __add_flat_item_to_structure(top_item, structure)
    
    # merging items and checking collisions
    
    all_items = []
    default_items = defaultdict(list)
    processed_items = []
    def add_to_all_items(item, is_default=False):
        nonlocal all_items, default_items, processed_items
        if item in processed_items:
            return
        processed_items.append(item)
        
        if item.is_single_item():
            all_items.append(item)
            if is_default:
                default_items[type(item)].append(item)
                for value in item.data.values():
                    if isinstance(value, ItemBase):
                        add_to_all_items(value, is_default=True)
            return
        
        for default in item.data.values():
            if isinstance(default, ItemBase):
                add_to_all_items(default, is_default=True)
        
        for inner_item in item:
            add_to_all_items(inner_item, is_default=True)
    
    
    add_to_all_items(top_item)  # can be a bulk item, need for defaults
    for items in structure.values():
        for item in items:
            add_to_all_items(item)

    for item_cls in structure.keys():
        if item_cls.allow_merge_items:
            merge_items(top_item,
                        structure[item_cls], default_items[item_cls],
                        all_items)
        else:
            __check_item_collisions(structure[item_cls])
     
    return structure


def __add_flat_item_to_structure(item, structure):
    
    if item.is_single_item():
        if item in structure[type(item)]:
            return
        structure[type(item)].append(item)
        
        for key, relation in item.relations.items():
            if key not in item or item[key] is None:
                continue
            
            __add_flat_item_to_structure(item[key], structure)
            
            # setting reverse relations
            reverse_key = relation['reverse_key']
            if reverse_key is None:
                continue
            
            that_item = item[key]
            is_one_to_x = relation['relation_type'].is_one_to_x()
 
            if that_item.is_single_item():
                if is_one_to_x:
                    if relation['reverse_key'] in that_item:
                        that_item_reverse = that_item[relation['reverse_key']]
                        if  that_item_reverse is not item and \
                                that_item_reverse is not None:
                         
                            raise ItemMustHaveTheSameIdentity(
                                'Key: {}'.format(reverse_key))
                            
                    that_item[relation['reverse_key']] = item
                else:
                    that_item[relation['reverse_key']].add(item)
            else:
                for inner_item in that_item.bulk:
                    if is_one_to_x:
                        if reverse_key in inner_item and \
                                inner_item[reverse_key] is not item and \
                                inner_item[reverse_key] is not None:
                            raise ItemMustHaveTheSameIdentity(
                                'Key: {}'.format(reverse_key))
                        
                        inner_item[reverse_key] = item
                    else:
                        pass
#                         inner_item[reverse_key].add(item)
            
    else:
        # bulk item can be added (using this function) only once at the
        # beginning
        for inner_item in item.bulk:
            __add_flat_item_to_structure(inner_item, structure)


def __check_item_collisions(item_list):
    if not item_list:
        return
    
    # `item_list` must contain items of the same class
    getter_groups = item_list[0].getters
    
    if not getter_groups:
        return
    
    for left_item in item_list:
        for right_item in item_list:
            if left_item is right_item:
                continue
             
            for getters in getter_groups:
                same_by_group = True
                for key in getters:
                    if key not in left_item.data or key not in right_item.data \
                            or left_item[key] is None or \
                            left_item[key] != right_item[key]:
                        same_by_group = False
                        break
      
                     
                if same_by_group:
                    raise MultipleItemsMatch(None, left_item, right_item,
                                             getters)