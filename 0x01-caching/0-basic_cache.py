#!/usr/bin/env python3
"""BasicCache module - implements a simple caching system
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache defines a caching system that stores key-value pairs without any
    eviction policy. It inherits from BaseCaching.

    Methods:
        put(key, item): Adds an item to the cache.
        get(key): Retrieves an item from the cache by key.
    """

    def __init__(self):
        """
        Initializes the cache by calling the parent class's constructor.
        """
        BaseCaching.__init__(self)

    def put(self, key, item):
        """
        Adds a key-value pair to the cache.

        Args:
            key: The key under which to store the item.
            item: The value to store in the cache.
        """
        if key is None or item is None:
            pass
        else:
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves the value associated with the given key from the cache.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the key, or None if not found or key is None.
        """
        if key is not None and key in self.cache_data.keys():
            return self.cache_data[key]
        return None
