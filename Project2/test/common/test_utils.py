import pytest
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../..')))
from common.utils import tokenize


@pytest.mark.parametrize("test_input, expected",
                         [("Test 123 .,|\\", ["test", "123"]),
                          ("Cats do NOT Like dogs", ["cat", "do", "not", "like", "dog"])])
def test_tokenize(test_input, expected):
    assert tokenize(test_input) == expected
