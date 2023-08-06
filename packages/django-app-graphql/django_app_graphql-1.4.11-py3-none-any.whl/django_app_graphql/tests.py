import json
import os
import unittest
from typing import Any, Dict, Union, Tuple, Optional

from django import test as django_test
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings.SETTING_DIR)
# import django
# django.setup()


from graphene.test import Client
from graphene_django.utils.testing import GraphQLTestCase
from requests import Response

from django_app_graphql import schema


class AbstractGraphQLTest(GraphQLTestCase):
    """
    An abstract class that can be used to perform tests on a graphql server.
    To perform tests, just do the following:

    .. code-block:: python

        from django_app_graphql import tests
        class MyGraphQLTests(tests.AbstractGraphQLTest):

            def test_foobar_query():
                # your test

    Generally speaking there are 3 ways of performing query: linear, chaining or standard

    Linear testing is when you in one command perform a grpahql query and then check the satisfaction of an assertion:

    .. code-block :: python

        self.assert_query_data_equal("foobar(5) { id }") # perform a grpahql query and check the result

    Chaining testing is when you first perform the query and then check the satisfaction of an assertion:

    .. code-block :: python

        result, response = self.do_query("foobar(5) { id }") # perform query
        self.assert_query_data_equal(result) # check the result

    Linear is quick, but chaining tsting allows you to check multiple assertions in one batch.

    Finally, you can also use the stnadard function provided by the GraphQLTestCase itself, namely:

    .. code-block :: python

        body, response = self.do_query("foobar(5) { id }")
        self.assertResdponseNoErrors(response)

    """

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def ask_to_graphql(self, query: Union[str, Dict[str, any]], arguments: Dict[str, any] = None) -> Tuple[Dict[str, any], Optional[Response]]:
        if isinstance(query, Dict):
            return query, None
        elif isinstance(query, str):
            pass
        else:
            raise TypeError(f"query should either be a dictionary or a string!")

        query = f"""
        query {{
            {query}
        }}
        """
        if arguments is None:
            arguments = {}
        http_response = self.query(query, input_data=arguments)
        if http_response.status_code != 200:
            raise ValueError(
                f"graphQL response was encapsulated in a http response whose status code is {http_response.status_code}")
        body = bytes.decode(http_response.content, http_response.charset)
        body = json.loads(body)
        assert 'data' in body, "GraphQL output should return 'data', but this call did not."
        assert 'errors' not in body, f"Got graphQL errors: {body}"
        assert body['data'] is not None, f"data payload is None. Output={body}"
        return body['data'], http_response

    def assert_data_equal(self, query: Union[str, Dict[str, any]], expected, context=None):
        """
        Check if the whole returned value of a graphql query/mutation is exactly as the one provided by the user

        :param query: either a strijng, repersenting the query that we need to perform or a a dictionary,
            representing the (assumed) output of do_query/do_mutation.
        :param expected: expected data value
        :param context: variables
        :return:
        """
        output, response = self.ask_to_graphql(query, context)
        assert output == expected, f"expected={expected} actual={output}"

    def assert_data_contains_key(self, query: Union[str, Dict[str, any]], key: str, context=None):
        output, response = self.ask_to_graphql(query, context)
        assert key in output, f"key {key} is not present in the graphql output (keys are {list(output.keys())})"

    def assert_data_key_value(self, query: Union[str, Dict[str, any]], key: str, value: Any, context=None):
        output, response = self.ask_to_graphql(query, context)
        assert key in output, f"""key "{key}" is not present in output (keys are {list(output.keys())})"""
        assert output[key] is not None, f"value associated to {key} is None"
        assert output[key] == value, f"value associated to {key}: expected={value} actual={output[key]}"




# Create your tests here.