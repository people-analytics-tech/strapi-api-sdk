from typing import Literal


class QueryBuilder(object):
    """Query builder - for constructing advanced Strapi queries"""

    def __init__(self):
        self._query: list = [""]
        self._sort_fields: list = []
        self._current_field: str = ""

    def field(self, field: str):
        """Sets the field to operate on
        :param field: field (str) to operate on
        """
        self._current_field = field
        self._query.append(f"filters[{field}]")
        return self

    def _add_condition(self, operator = None, value = None, values = None, operand = None):
        """Adds a condition with the given operator and value
        :param operator: operator (str)
        :param value: value to match
        """
        if value:
            self._query[-1] += f"[{operator}]={value}"
            
        if values:
            for enum, value in enumerate(values):
                self._query[-1] += f"&filters[{self._current_field}][{operator}][{enum}]={value}"
                
        if operand:
            for enum, value in enumerate(values):
                self._query[-1] += f"&filters[{operand}][{enum}][{self._current_field}]{value}"
                
        return self

    def equal(self, value):
        """Adds a condition for equality
        :param value: value to match for equality
        """
        return self._add_condition("$eq", value)

    def equal_case_insensitive(self, value):
        """Adds a case-insensitive condition for equality
        :param value: value to match for equality (case-insensitive)
        """
        return self._add_condition("$eqi", value)

    def not_equal(self, value):
        """Adds a condition for not equal
        :param value: value to check for inequality
        """
        return self._add_condition("$ne", value)

    def not_equal_case_insensitive(self, value):
        """Adds a case-insensitive condition for not equal
        :param value: value to check for inequality (case-insensitive)
        """
        return self._add_condition("$nei", value)

    def less_than(self, value):
        """Adds a condition for less than
        :param value: value to compare for less than
        """
        return self._add_condition("$lt", value)

    def less_than_or_equal_to(self, value):
        """Adds a condition for less than or equal to
        :param value: value to compare for less than or equal to
        """
        return self._add_condition("$lte", value)

    def greater_than(self, value):
        """Adds a condition for greater than
        :param value: value to compare for greater than
        """
        return self._add_condition("$gt", value)

    def greater_than_or_equal_to(self, value):
        """Adds a condition for greater than or equal to
        :param value: value to compare for greater than or equal to
        """
        return self._add_condition("$gte", value)

    def in_array(self, values: list):
        """Adds a condition for included in an array
        :param values: list of values to check for inclusion
        """
        return self._add_condition("$in", values=values)

    def not_in_array(self, values: list):
        """Adds a condition for not included in an array
        :param values: list of values to check for exclusion
        """
        return self._add_condition("$notIn", values=values)

    def contains(self, value):
        """Adds a condition for contains
        :param value: value to check for containment
        """
        return self._add_condition("$contains", value)

    def not_contains(self, value):
        """Adds a condition for not contains
        :param value: value to check for non-containment
        """
        return self._add_condition("$notContains", value)

    def contains_case_insensitive(self, value):
        """Adds a case-insensitive condition for contains
        :param value: value to check for containment (case-insensitive)
        """
        return self._add_condition("$containsi", value)

    def not_contains_case_insensitive(self, value):
        """Adds a case-insensitive condition for not contains
        :param value: value to check for non-containment (case-insensitive)
        """
        return self._add_condition("$notContainsi", value)

    def null(self):
        """Adds a condition for null"""
        return self._add_condition("$null", "")

    def not_null(self):
        """Adds a condition for not null"""
        return self._add_condition("$notNull", "")

    def between(self, start, end):
        """Adds a condition for between
        :param start: start value for the range
        :param end: end value for the range
        """
        return self._add_condition("$between", f"{start},{end}")

    def starts_with(self, value):
        """Adds a condition for starts with
        :param value: value to check for starting with
        """
        return self._add_condition("$startsWith", value)

    def starts_with_case_insensitive(self, value):
        """Adds a case-insensitive condition for starts with
        :param value: value to check for starting with (case-insensitive)
        """
        return self._add_condition("$startsWithi", value)

    def ends_with(self, value):
        """Adds a condition for ends with
        :param value: value to check for ending with
        """
        return self._add_condition("$endsWith", value)

    def ends_with_case_insensitive(self, value):
        """Adds a case-insensitive condition for ends with
        :param value: value to check for ending with (case-insensitive)
        """
        return self._add_condition("$endsWithi", value)

    def sort(self, field: str, order: Literal["asc", "desc"] = "asc"):
        """Sets sorting on a field
        :param field: field to sort on
        :param order: sorting order, "asc" for ascending, "desc" for descending
        """
        self._sort_fields.append(f"{field}:{order}")
        return self

    def OR(self, conditions):
        """Adds a condition for "or" expression
        :param conditions: list of conditions to join with "or"
        """
        conditions_str = conditions.split("[")
        return self._add_condition(operand="$or", values=conditions_str)

    def AND(self, conditions):
        """Adds a condition for "and" expression
        :param conditions: list of conditions to join with "and"
        """
        conditions_str = ",".join(conditions)
        return self._add_condition("$and", f"[{conditions_str}]")

    def NOT(self, condition):
        """Adds a condition for "not" expression
        :param condition: condition to negate with "not"
        """
        return self._add_condition("$not", f"[{condition}]")

    def __str__(self):
        """String representation of the query object"""
        
        query_string = "&".join(self._query)
        
        if self._sort_fields:
            sort_string = "&".join([f"sort[{i}]={field}" for i, field in enumerate(self._sort_fields)])
            query_string = f"{query_string}&{sort_string}"
        
        return query_string
