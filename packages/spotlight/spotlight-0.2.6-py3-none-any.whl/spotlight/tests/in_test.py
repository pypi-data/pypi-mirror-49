from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class InTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.in_error = err.IN_ERROR.format(
            field=self.field,
            values="val0, val1, val2"
        )

    def test_in_rule_with_invalid_value_expect_error(self):
        input_values = {
            "test": "val3"
        }
        rules = {
            "test": "in:val0,val1,val2"
        }
        expected = self.in_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_in_rule_with_valid_value_expect_no_error(self):
        input_values = {
            "test": "val1"
        }
        rules = {
            "test": "in:val0,val1,val2",
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_in_rule_with_integer_expect_no_error(self):
        input_values = {
            "test": 1
        }
        rules = {
            "test": "in:1,2,3",
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_in_rule_with_bool_expect_no_error(self):
        input_values = {
            "test": True
        }
        rules = {
            "test": "in:true,false",
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
