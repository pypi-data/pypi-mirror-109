"""
DiffCalculus Package :-

- A Python 3.x Package that Implements Differentiation...
"""

from .__differentiate__ import differentiate, differentiateAtPoint, substitute
from sys import setrecursionlimit as __limit

__limit(20000)