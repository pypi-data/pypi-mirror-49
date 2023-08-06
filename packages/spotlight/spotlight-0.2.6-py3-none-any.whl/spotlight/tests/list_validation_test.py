from spotlight.tests.validator_test import ValidatorTest


class ListValidationTest(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}

    def test_list_validation_expect_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list.0.test2": ["The list.0.test2 field has to be at least 2 characters."],
            "list.1.test": [
                "The list.1.test field cannot be longer than 2 characters."
            ],
            "list.1.test2": ["The list.1.test2 field has to be at least 2 characters."],
            "list.2.test": [
                "The list.2.test field cannot be longer than 2 characters."
            ],
            "list.2.test2": ["The list.2.test2 field has to be at least 2 characters."],
        }
        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_flat_expect_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = [
            "The list.1.test field cannot be longer than 2 characters.",
            "The list.2.test field cannot be longer than 2 characters.",
            "The list.0.test2 field has to be at least 2 characters.",
            "The list.1.test2 field has to be at least 2 characters.",
            "The list.2.test2 field has to be at least 2 characters.",
        ]

        errors = self.validator.validate(input_values, rules, flat=True)

        self.assertEqual(expected, errors)

    def test_list_validation_expect_with_custom_message_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list.0.test2": ["The list.0.test2 field has to be at least 2 characters."],
            "list.1.test": ["Hey! The list.1.test field has to be at least 2 chars!"],
            "list.1.test2": ["The list.1.test2 field has to be at least 2 characters."],
            "list.2.test": ["Hey! The list.2.test field has to be at least 2 chars!"],
            "list.2.test2": ["The list.2.test2 field has to be at least 2 characters."],
        }

        new_message = "Hey! The {field} field has to be at least {max} chars!"
        messages = {"list.*.test.max": new_message}
        self.validator.overwrite_messages = messages

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_expect_with_custom_fields_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list.0.test2": ["The custom field has to be at least 2 characters."],
            "list.1.test": [
                "The list.1.test field cannot be longer than 2 characters."
            ],
            "list.1.test2": ["The custom field has to be at least 2 characters."],
            "list.2.test": [
                "The list.2.test field cannot be longer than 2 characters."
            ],
            "list.2.test2": ["The custom field has to be at least 2 characters."],
        }
        fields = {"list.*.test2": "custom"}
        self.validator.overwrite_fields = fields

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_expect_with_values_message_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "in:val1,val2,val3"}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list.0.test2": [
                "The list.0.test2 field must be one of the following values: piet, henk, jan."
            ],
            "list.1.test": [
                "The list.1.test field cannot be longer than 2 characters."
            ],
            "list.1.test2": [
                "The list.1.test2 field must be one of the following values: piet, henk, jan."
            ],
            "list.2.test": [
                "The list.2.test field cannot be longer than 2 characters."
            ],
            "list.2.test2": [
                "The list.2.test2 field must be one of the following values: piet, henk, jan."
            ],
        }
        new_values = "piet, henk, jan"
        values = {"list.*.test2": {"values": new_values}}
        self.validator.overwrite_values = values

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_required_expect_error(self):
        rules = {"list.*.test": "required|max:2", "list.*.test2": "min:2"}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list.0.test2": ["The list.0.test2 field has to be at least 2 characters."],
            "list.1.test": ["The list.1.test field is required."],
            "list.1.test2": ["The list.1.test2 field has to be at least 2 characters."],
            "list.2.test": [
                "The list.2.test field cannot be longer than 2 characters."
            ],
            "list.2.test2": ["The list.2.test2 field has to be at least 2 characters."],
        }

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_with_optional_field_expect_no_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        input_values = {"list": [{}, {}, {}]}
        expected = {}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_with_filled_field_expect_error(self):
        rules = {"list.*.test": "required|max:2", "list.*.test2": "min:2"}
        input_values = {"list": [{}, {}, {}]}
        expected = {
            "list.0.test": ["The list.0.test field is required."],
            "list.1.test": ["The list.1.test field is required."],
            "list.2.test": ["The list.2.test field is required."],
        }

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_with_nested_dict_expect_error(self):
        rules = {
            "players": "required|list|min:2",
            "hello": "required|dict",
            "hello.test": "required|string",
            "players.*.name": "required|min:3|max:25",
            "players.*.unit": "required|dict",
            "players.*.unit.name": "required|string|max:3",
        }
        input_values = {
            "hello": {"test": "piet"},
            "players": [
                {"name": "Test 1", "unit": {"name": "hoi"}},
                {"name": "Test 2", "unit": {"name": "hoi"}},
            ],
        }
        expected = {}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_with_empty_list_expect_no_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        input_values = {"list": []}
        expected = {}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_with_dict_expect_no_error(self):
        rules = {"list.*.test": "max:2", "list.*.test2": "min:2"}
        input_values = {"list": {}}
        expected = {}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_with_bool_expect_error(self):
        rules = {"list": "required|list"}
        input_values = {"list": True}
        expected = {"list": ["The list field must be a list."]}

        errors = self.validator.validate(input_values, rules)

        self.assertEqual(expected, errors)

    def test_list_validation_without_key_returns_no_error(self):
        rules = {
            "start_at": "string|min:10",
            "end_at": "string|min:10",
            "ticket_universe.size": "integer",
            "ticket_universe.positions.*": "string"
        }
        input_values = {
            "start_at": "2017:03:22",
            "end_at": "2028:03:26",
            "ticket_universe": {
                "size": 99,
                "positions": ["fixed:A", "ranged:1:2", "binary", "alpha", "numeric"]
            }
        }
        expected = {
        }
        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)


