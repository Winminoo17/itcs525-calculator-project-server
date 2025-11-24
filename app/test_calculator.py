import pytest
from app.dependencies import expand_percent
from app.schemas import ExpressionIn

def test_add_percent():
    """Test addition where B% means 'B percent of A'."""
    e = ExpressionIn(expr="5 + 10%")
    assert e.expand_percent() == "5 + ((10/100)*5)"

def test_subtract_percent():
    """Test subtraction where B% means 'B percent of A'."""
    e = ExpressionIn(expr="20 - 30%")
    assert e.expand_percent() == "20 - ((30/100)*20)"

def test_multiply_percent():
    """Test multiplication where B% means 'B divided by 100'."""
    e = ExpressionIn(expr="15 * 25%")
    assert e.expand_percent() == "15 * (25/100)"

def test_divide_percent():
    """Test division where B% means 'B divided by 100'."""
    e = ExpressionIn(expr="40 / 50%")
    assert e.expand_percent() == "40 / (50/100)"

def test_multiple_operations():
    """Test ExpressionIns with multiple A op B% operations."""
    e = ExpressionIn(expr="3 * 4% + 2 / 1%")
    assert e.expand_percent() == "3 * (4/100) + 2 / (1/100)"

def test_standalone_100_percent():
    """Test standalone percentage (100%)."""
    e = ExpressionIn(expr="100%")
    assert e.expand_percent() == "(100/100)"

def test_two_standalone_percents():
    """Test ExpressionIn with two standalone percentages."""
    e = ExpressionIn(expr="10% + 20%")
    assert e.expand_percent() == "(10/100) + (20/100)"

