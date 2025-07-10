import pytest
from demo_calculator import add, multiply, Calculator


class TestAdd:
    """Test cases for the add function."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5
        assert add(10, 20) == 30
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add(-2, -3) == -5
        assert add(-10, 5) == -5
        assert add(10, -5) == 5
    
    def test_add_zero(self):
        """Test adding zero."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0
    
    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(2.5, 3.7) == 6.2
        assert add(1.1, 2.2) == pytest.approx(3.3)
    
    def test_add_large_numbers(self):
        """Test adding large numbers."""
        assert add(1000000, 2000000) == 3000000
    
    def test_add_mixed_types(self):
        """Test adding int and float."""
        assert add(5, 2.5) == 7.5
        assert add(3.7, 2) == 5.7
    
    def test_add_non_numeric_types(self):
        """Test add function with non-numeric types (duck typing)."""
        assert add("hello", "world") == "helloworld"
        assert add([1, 2], [3, 4]) == [1, 2, 3, 4]
        assert add("test", 123) == "test123"


class TestMultiply:
    """Test cases for the multiply function."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        assert multiply(3, 4) == 12
        assert multiply(5, 6) == 30
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert multiply(-3, 4) == -12
        assert multiply(3, -4) == -12
        assert multiply(-3, -4) == 12
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0
        assert multiply(0, 0) == 0
    
    def test_multiply_by_one(self):
        """Test multiplying by one."""
        assert multiply(5, 1) == 5
        assert multiply(1, 5) == 5
    
    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        assert multiply(2.5, 4.0) == 10.0
        assert multiply(1.5, 2.5) == pytest.approx(3.75)
    
    def test_multiply_mixed_types(self):
        """Test multiplying int and float."""
        assert multiply(3, 2.5) == 7.5
        assert multiply(2.5, 4) == 10.0
    
    def test_multiply_type_error_string(self):
        """Test that strings raise TypeError."""
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply("5", 3)
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply(5, "3")
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply("5", "3")
    
    def test_multiply_type_error_list(self):
        """Test that lists raise TypeError."""
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply([1, 2], 3)
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply(5, [1, 2])
    
    def test_multiply_type_error_none(self):
        """Test that None raises TypeError."""
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply(None, 5)
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply(5, None)
    
    def test_multiply_type_error_dict(self):
        """Test that dictionaries raise TypeError."""
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply({}, 5)
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply(5, {"key": "value"})
    
    def test_multiply_type_error_bool(self):
        """Test that booleans raise TypeError."""
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply(True, 5)
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            multiply(5, False)


class TestCalculator:
    """Test cases for the Calculator class."""
    
    def test_calculator_initialization(self):
        """Test calculator initialization."""
        calc = Calculator()
        assert calc.history == []
    
    def test_calculate_add_operation(self):
        """Test calculator add operation."""
        calc = Calculator()
        result = calc.calculate("add", 5, 3)
        assert result == 8
        assert len(calc.history) == 1
        assert calc.history[0] == "5 add 3 = 8"
    
    def test_calculate_multiply_operation(self):
        """Test calculator multiply operation."""
        calc = Calculator()
        result = calc.calculate("multiply", 4, 6)
        assert result == 24
        assert len(calc.history) == 1
        assert calc.history[0] == "4 multiply 6 = 24"
    
    def test_calculate_multiple_operations(self):
        """Test multiple operations maintain history."""
        calc = Calculator()
        calc.calculate("add", 2, 3)
        calc.calculate("multiply", 4, 5)
        calc.calculate("add", 10, -5)
        
        assert len(calc.history) == 3
        assert calc.history[0] == "2 add 3 = 5"
        assert calc.history[1] == "4 multiply 5 = 20"
        assert calc.history[2] == "10 add -5 = 5"
    
    def test_calculate_with_floats(self):
        """Test calculator with floating point numbers."""
        calc = Calculator()
        result = calc.calculate("add", 2.5, 3.7)
        assert result == 6.2
        assert calc.history[0] == "2.5 add 3.7 = 6.2"
    
    def test_calculate_unsupported_operation(self):
        """Test that unsupported operations raise ValueError."""
        calc = Calculator()
        with pytest.raises(ValueError, match="Unsupported operation"):
            calc.calculate("subtract", 5, 3)
        with pytest.raises(ValueError, match="Unsupported operation"):
            calc.calculate("divide", 10, 2)
        with pytest.raises(ValueError, match="Unsupported operation"):
            calc.calculate("invalid", 1, 2)
    
    def test_calculate_multiply_type_error_propagation(self):
        """Test that TypeError from multiply function propagates."""
        calc = Calculator()
        with pytest.raises(TypeError, match="Arguments must be numbers"):
            calc.calculate("multiply", "5", 3)
        
        # History should remain empty when operation fails
        assert len(calc.history) == 0
    
    def test_calculate_history_not_modified_on_error(self):
        """Test that history is not modified when operation fails."""
        calc = Calculator()
        calc.calculate("add", 1, 2)  # Successful operation
        
        # This should fail and not modify history
        with pytest.raises(ValueError):
            calc.calculate("invalid", 3, 4)
        
        assert len(calc.history) == 1
        assert calc.history[0] == "1 add 2 = 3"
    
    def test_multiple_calculator_instances(self):
        """Test that multiple calculator instances have separate histories."""
        calc1 = Calculator()
        calc2 = Calculator()
        
        calc1.calculate("add", 1, 2)
        calc2.calculate("multiply", 3, 4)
        
        assert len(calc1.history) == 1
        assert len(calc2.history) == 1
        assert calc1.history[0] == "1 add 2 = 3"
        assert calc2.history[0] == "3 multiply 4 = 12"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_very_large_numbers(self):
        """Test with very large numbers."""
        calc = Calculator()
        large_num = 10**100
        result = calc.calculate("add", large_num, 1)
        assert result == large_num + 1
    
    def test_very_small_numbers(self):
        """Test with very small floating point numbers."""
        calc = Calculator()
        small_num = 1e-10
        result = calc.calculate("multiply", small_num, 2)
        assert result == pytest.approx(2e-10)
    
    def test_negative_zero(self):
        """Test with negative zero."""
        calc = Calculator()
        result = calc.calculate("add", -0.0, 0.0)
        assert result == 0.0
    
    def test_infinity_handling(self):
        """Test behavior with infinity."""
        calc = Calculator()
        inf = float('inf')
        result = calc.calculate("add", inf, 1)
        assert result == inf
        
        result = calc.calculate("multiply", inf, 2)
        assert result == inf
    
    def test_nan_handling(self):
        """Test behavior with NaN."""
        calc = Calculator()
        nan = float('nan')
        result = calc.calculate("add", nan, 1)
        assert result != result  # NaN != NaN
        
        result = calc.calculate("multiply", nan, 2)
        assert result != result  # NaN != NaN


class TestCalculatorAdvanced:
    """Advanced test cases for Calculator class."""
    
    def test_calculator_state_isolation(self):
        """Test that calculator instances don't share state."""
        calc1 = Calculator()
        calc2 = Calculator()
        
        calc1.calculate("add", 1, 1)
        calc1.calculate("multiply", 2, 2)
        
        calc2.calculate("add", 10, 10)
        
        assert len(calc1.history) == 2
        assert len(calc2.history) == 1
        assert calc1.history != calc2.history
    
    def test_calculator_history_order(self):
        """Test that history maintains chronological order."""
        calc = Calculator()
        
        operations = [
            ("add", 1, 2),
            ("multiply", 3, 4),
            ("add", 5, 6),
            ("multiply", 7, 8)
        ]
        
        expected_results = [3, 12, 11, 56]
        
        for i, (op, a, b) in enumerate(operations):
            result = calc.calculate(op, a, b)
            assert result == expected_results[i]
        
        # Verify history order
        assert calc.history[0] == "1 add 2 = 3"
        assert calc.history[1] == "3 multiply 4 = 12"
        assert calc.history[2] == "5 add 6 = 11"
        assert calc.history[3] == "7 multiply 8 = 56"
    
    def test_calculator_complex_workflow(self):
        """Test a complex calculation workflow."""
        calc = Calculator()
        
        # Simulate a complex calculation sequence
        a = calc.calculate("add", 10, 5)        # 15
        b = calc.calculate("multiply", a, 2)    # 30
        c = calc.calculate("add", b, -5)        # 25
        d = calc.calculate("multiply", c, 0)    # 0
        e = calc.calculate("add", d, 100)       # 100
        
        assert a == 15
        assert b == 30
        assert c == 25
        assert d == 0
        assert e == 100
        
        assert len(calc.history) == 5
        assert calc.history[-1] == "0 add 100 = 100"
    
    def test_calculator_error_recovery(self):
        """Test calculator behavior after errors."""
        calc = Calculator()
        
        # Successful operation
        calc.calculate("add", 1, 2)
        
        # Failed operation (should not affect history)
        with pytest.raises(ValueError):
            calc.calculate("invalid", 3, 4)
        
        # Another failed operation
        with pytest.raises(TypeError):
            calc.calculate("multiply", "hello", 5)
        
        # Another successful operation
        calc.calculate("multiply", 3, 4)
        
        # History should only contain successful operations
        assert len(calc.history) == 2
        assert calc.history[0] == "1 add 2 = 3"
        assert calc.history[1] == "3 multiply 4 = 12"


class TestParameterizedTests:
    """Parameterized tests for comprehensive coverage."""
    
    @pytest.mark.parametrize("a, b, expected", [
        (0, 0, 0),
        (1, 1, 2),
        (-1, -1, -2),
        (100, 200, 300),
        (3.14, 2.86, 6.0),
        (-10, 10, 0),
        (1e6, 1e6, 2e6),
    ])
    def test_add_parameterized(self, a, b, expected):
        """Parameterized test for add function."""
        result = add(a, b)
        if isinstance(expected, float):
            assert result == pytest.approx(expected)
        else:
            assert result == expected
    
    @pytest.mark.parametrize("a, b, expected", [
        (0, 0, 0),
        (1, 1, 1),
        (-1, -1, 1),
        (2, 3, 6),
        (5, -2, -10),
        (-3, -4, 12),
        (0.5, 4, 2.0),
        (1e3, 1e3, 1e6),
    ])
    def test_multiply_parameterized(self, a, b, expected):
        """Parameterized test for multiply function."""
        result = multiply(a, b)
        if isinstance(expected, float):
            assert result == pytest.approx(expected)
        else:
            assert result == expected
    
    @pytest.mark.parametrize("operation, a, b, expected", [
        ("add", 1, 2, 3),
        ("add", -1, -2, -3),
        ("multiply", 3, 4, 12),
        ("multiply", -2, 5, -10),
        ("add", 0, 0, 0),
        ("multiply", 0, 100, 0),
    ])
    def test_calculator_parameterized(self, operation, a, b, expected):
        """Parameterized test for Calculator.calculate method."""
        calc = Calculator()
        result = calc.calculate(operation, a, b)
        assert result == expected
        assert len(calc.history) == 1
        assert calc.history[0] == f"{a} {operation} {b} = {expected}"


class TestPerformanceAndBounds:
    """Test performance characteristics and boundary conditions."""
    
    def test_large_history(self):
        """Test calculator with large history."""
        calc = Calculator()
        
        # Perform many operations
        for i in range(100):
            calc.calculate("add", i, i + 1)
        
        assert len(calc.history) == 100
        assert calc.history[0] == "0 add 1 = 1"
        assert calc.history[-1] == "99 add 100 = 199"
    
    def test_precision_limits(self):
        """Test floating point precision limits."""
        calc = Calculator()
        
        # Test with numbers at the limit of float precision
        small = 1e-15
        result = calc.calculate("add", 1.0, small)
        
        # Due to floating point precision, this might not be exactly 1.0 + 1e-15
        assert result >= 1.0
        assert result <= 1.0 + 1e-14
    
    def test_extreme_values(self):
        """Test with extreme values."""
        calc = Calculator()
        
        # Test with maximum float value
        max_val = 1.7976931348623157e+308
        result = calc.calculate("multiply", max_val, 0.5)
        assert result == max_val * 0.5
        
        # Test with minimum positive float value
        min_val = 2.2250738585072014e-308
        result = calc.calculate("multiply", min_val, 2.0)
        assert result == min_val * 2.0