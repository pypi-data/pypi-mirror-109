import unittest

from typing import Any

class GtsamTestCase(unittest.TestCase):
    """TestCase class with GTSAM assert utils."""

    """ AssertEqual function that prints out actual and expected if not equal.

        Usage:
            self.gtsamAssertEqual(actual,expected)
        Keyword Arguments:
            tol {float} -- tolerance passed to 'equals', default 1e-9
    """
    def gtsamAssertEquals(self, actual: Any, expected: Any, tol=1e-9): ...
        
    """ Performs a round-trip using pickle and asserts equality.

        Usage:
            self.assertEqualityOnPickleRoundtrip(obj)
        Keyword Arguments:
            tol {float} -- tolerance passed to 'equals', default 1e-9
    """
    def assertEqualityOnPickleRoundtrip(self, obj: object, tol=1e-9) -> None: ...
