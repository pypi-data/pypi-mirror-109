#!/usr/bin/env python3

import operator

from functools import reduce, wraps
from typing import Any, Generator


class Tree(object):
    """A class to lazily iterate a dictionary for path matching.

    Attributes
    -----------
    branch : list
        list of dictionary path, value matches
    limb : list
        list of matching list paths
    path : str
        string to search
    source : dict
        dictionary to search
    tree : list
        list of possible paths from source dictionary

    Methods
    -------
    get(str):
        Sets the string for which to search

    from_dict(dict):
        Sets the dictionary to search and returns matches
    """

    def __init__(
        self, branch=None, limb=None, path=None, source=None, tree=None
    ) -> None:
        self.branch = branch
        self.limb = limb
        self.path = path
        self.source = source
        self.tree = tree

    def _set_branch(func):
        """Decorator for from_dict() to set and return list of kv matches."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            self, _ = args
            result = func(*args, **kwargs)
            branch = self._get_branch(self.limb)
            self.__dict__.__setitem__("branch", branch)
            return branch

        return wrapper

    def _set_dict(func):
        """Decorator for from_dict() to set the source dictionary."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            self, value = args
            if not isinstance(value, dict):
                raise TypeError("The from_dict() argument must be type dict")
            if not value:
                raise ValueError("The from_dict() argument must not be empty.")

            self.__dict__.__setitem__("source", value)
            result = func(*args, **kwargs)
            return result

        return wrapper

    def _set_limb(func):
        """Decorator for from_dict() to set matching paths."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            self, _ = args
            if self.path is None:
                raise ValueError("Use the get() method before calling from_dict().")

            result = func(*args, **kwargs)
            limb = [
                x for x in self.tree if all(item in x for item in self.path.split("."))
            ]
            self.__dict__.__setitem__("limb", limb)
            return result

        return wrapper

    def _set_path(func):
        """Decorator for get() to set the search string."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != 2:
                raise ValueError("The get() method requires a string value.")
            self, value = args
            self.__dict__.__setitem__("path", value)
            result = func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    def _set_tree(func):
        """Decorator for from_dict() to set iterated paths."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            self, _ = args
            result = func(*args, **kwargs)

            tree = self._split_dict(self.source)
            self.__dict__.__setitem__("tree", list(tree))
            return result

        return wrapper

    def _get_branch(self, limbs: list) -> list:
        """Get matches by kv."""
        return [({"path": ".".join(x), "value": self._get_twig(x)}) for x in limbs]

    def _get_twig(self, path: str) -> Any:
        """Get the value for the given path."""
        return reduce(operator.getitem, path, self.source)

    def _split_dict(self, tree_dict: dict, pos: list = []) -> Generator:
        """Lazy iterator to split the dict into unique paths."""
        for x, y in tree_dict.items():
            if isinstance(y, dict):
                yield from self._split_dict(y, pos + [x])
            yield pos + [x]
        return

    @_set_path
    def get(self, value):
        """
        Set the lazy path to match.

        Parameters
        -----------
            value : str
                A Dot-delimited path to match

        Returns
        -------
            None
        """
        return self

    @_set_branch
    @_set_limb
    @_set_tree
    @_set_dict
    def from_dict(self, value) -> list:
        """
        Set the source dictionary.

        Parameters
        -----------
            value : dict
                The dictionary to iterate for string matches

        Returns
        -------
            branch : list
                The list of kv matches
        """
