"""
Tests for the swaggerconformance package.

General strategy is to run validation of a schema set to use a specific URL as
the remote host, and then intercept the requests to that remot API using the
responses package.
Typically, there's no need to validate that the data caught actually matches
the constraints of the schema in these tests - the `pyswagger` module used to
drive the API does all the validation of input required for us.
"""
import unittest
import unittest.mock
import re
import os.path as osp
import json
import urllib

import responses
import hypothesis

import swaggercheck
import swaggercheck.response


TEST_SCHEMA_DIR = osp.relpath(
    osp.join(osp.dirname(osp.realpath(__file__)), "test_schemas/")
)
TEST_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, "test_schema.json")
FULL_PUT_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, "full_put_schema.json")
ALL_CONSTRAINTS_SCHEMA_PATH = osp.join(
    TEST_SCHEMA_DIR, "all_constraints_schema.json"
)
PETSTORE_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, "petstore.json")
UBER_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, "uber.json")
MIRROR_REQS_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, "mirror_requests.json")
SCHEMA_URL_BASE = "http://127.0.0.1:5000/api"
CONTENT_TYPE_JSON = "application/json"


def _respond_to_method(method, path, response_json, status, content_type):
    url_re = re.compile(SCHEMA_URL_BASE + path + "$")
    responses.add(
        method,
        url_re,
        json=response_json,
        status=status,
        content_type=content_type,
    )


def respond_to_get(
    path, response_json=None, status=200, content_type=CONTENT_TYPE_JSON
):
    """Respond to a GET request to the provided path."""
    _respond_to_method(
        responses.GET, path, response_json, status, content_type
    )


def respond_to_post(
    path, response_json=None, status=200, content_type=CONTENT_TYPE_JSON
):
    """Respond to a POST request to the provided path."""
    _respond_to_method(
        responses.POST, path, response_json, status, content_type
    )


def respond_to_put(
    path, response_json=None, status=200, content_type=CONTENT_TYPE_JSON
):
    """Respond to a PUT request to the provided path."""
    _respond_to_method(
        responses.PUT, path, response_json, status, content_type
    )


def respond_to_delete(
    path, response_json=None, status=200, content_type=CONTENT_TYPE_JSON
):
    """Respond to a DELETE request to the provided path."""
    _respond_to_method(
        responses.DELETE, path, response_json, status, content_type
    )


class APITemplateTestCase(unittest.TestCase):
    """Simple tests working with the `schema.Api` class directly."""

    def setUp(self):
        self.client = swaggercheck.client.Client(TEST_SCHEMA_PATH)

    def tearDown(self):
        # No teardown of test fixtures required.
        pass

    def test_schema_parse(self):
        """Test we can parse an API schema, and find all the endpoints."""
        api_template = swaggercheck.schema.Api(self.client)
        expected_endpoints = {"/schema", "/apps", "/apps/{appid}"}
        self.assertSetEqual(
            set(api_template.endpoints.keys()), expected_endpoints
        )

    @responses.activate
    def test_endpoint_manually(self):
        """Test we can make a request against an endpoint manually."""
        api_template = swaggercheck.schema.Api(self.client)

        # Find the template GET operation on the /apps/{appid} endpoint.
        app_id_get_op = None
        for operation_template in api_template.operations():
            if (
                operation_template.method == "get"
                and operation_template.path == "/apps/{appid}"
            ):
                self.assertIsNone(app_id_get_op)
                app_id_get_op = operation_template
        self.assertIsNotNone(app_id_get_op)

        # The operation takes two parameters, 'appid', which is a string and
        # the special 'X-Fields' header parameter.
        self.assertSetEqual(
            set(app_id_get_op.parameters.keys()), {"appid", "X-Fields"}
        )
        self.assertEqual(app_id_get_op.parameters["appid"].type, "string")

        # Send an example parameter in to the endpoint manually, catch the
        # request, and respond.
        params = {"appid": "test_string"}
        respond_to_get(
            "/apps/test_string",
            response_json={"name": "abc", "data": {}},
            status=200,
        )
        result = self.client.request(app_id_get_op, params)
        self.assertEqual(result.status, 200)
        self.assertEqual(json.loads(result.raw.decode("utf-8")), result.body)

    def test_operation_access(self):
        """Test access to operations by ID or path."""
        api_template = swaggercheck.schema.Api(self.client)
        self.assertEqual(
            api_template.endpoints["/apps/{appid}"]["get"],
            api_template.operation("get_apps_resource"),
        )


class BasicConformanceAPITestCase(unittest.TestCase):
    """Tests of the basic conformance testing API itself."""

    @responses.activate
    def test_content_type_header_with_parameters(self):
        """Content type header parameters should be allowed."""
        content_type_extra = "application/json; charset=utf-8"
        respond_to_get("/schema")
        respond_to_get(
            "/apps",
            response_json=[{"name": "test"}],
            content_type=content_type_extra,
        )
        respond_to_get(
            r"/apps/.+", status=404, content_type=content_type_extra
        )
        respond_to_put(
            r"/apps/.+", status=204, content_type=content_type_extra
        )
        respond_to_delete(
            r"/apps/.+", status=204, content_type=content_type_extra
        )

        swaggercheck.api_conformance_test(TEST_SCHEMA_PATH, cont_on_err=False)


class ParameterTypesTestCase(unittest.TestCase):
    """Tests to cover all the options/constraints on parameters."""

    @responses.activate
    def test_full_put(self):
        """A PUT request containing all different parameter types."""
        # Handle all the basic endpoints.
        respond_to_get("/example")
        respond_to_delete("/example", status=204)
        respond_to_put(r"/example/-?\d+", status=204)

        # Now just kick off the validation process.
        swaggercheck.api_conformance_test(
            FULL_PUT_SCHEMA_PATH, cont_on_err=False
        )

    @responses.activate
    def test_all_constraints(self):
        """A PUT request containing all parameter constraint combinations."""
        # Handle all the basic endpoints.
        respond_to_get("/schema")
        respond_to_put(r"/example/-?\d+", status=204)

        # Now just kick off the validation process.
        swaggercheck.api_conformance_test(
            ALL_CONSTRAINTS_SCHEMA_PATH, cont_on_err=False
        )


class ExternalExamplesTestCase(unittest.TestCase):
    """Tests of API specs from external sources to get coverage."""

    @responses.activate
    def test_swaggerio_petstore(self):
        """The petstore API spec from the swagger.io site is handled."""
        # Example responses matching the required models.
        pet = {
            "id": 0,
            "category": {"id": 0, "name": "string"},
            "name": "doggie",
            "photoUrls": ["string"],
            "tags": [{"id": 0, "name": "string"}],
            "status": "available",
        }
        pets = [pet]
        inventory = {"additionalProp1": 0, "additionalProp2": 0}
        order = {
            "id": 0,
            "petId": 0,
            "quantity": 0,
            "shipDate": "2017-03-21T23:13:44.949Z",
            "status": "placed",
            "complete": True,
        }
        api_response = {"code": 0, "type": "string", "message": "string"}
        user = {
            "id": 0,
            "username": "string",
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "phone": "string",
            "userStatus": 0,
        }

        # Handle all the basic endpoints.
        respond_to_get("/pet")
        respond_to_post("/pet")
        respond_to_put("/pet")
        respond_to_get(r"/pet/-?\d+", response_json=pet)
        respond_to_delete(r"/pet/-?\d+")
        respond_to_post(r"/pet/-?\d+", response_json=api_response)
        respond_to_post(r"/pet/-?\d+/uploadImage", response_json=api_response)
        respond_to_get("/pet/findByStatus", response_json=pets)
        respond_to_get(r"/pet/findByStatus\?status=.*", response_json=pets)
        respond_to_get("/pet/findByTags", response_json=pets)
        respond_to_get(r"/pet/findByTags\?tags=.*", response_json=pets)
        respond_to_get("/store")
        respond_to_get("/store/inventory", response_json=inventory)
        respond_to_post("/store/order", response_json=order)
        respond_to_get(r"/store/order/-?\d+", response_json=order)
        respond_to_delete(r"/store/order/-?\d+")
        respond_to_get("/user")
        respond_to_post("/user")
        respond_to_delete("/user")
        respond_to_get(r"/user/(?!login).+", response_json=user)
        respond_to_put(r"/user/(?!login).+")
        respond_to_delete(r"/user/(?!login).+")
        respond_to_get(
            r"/user/login\?username=.*&password=.*", response_json="example"
        )
        respond_to_get("/user/logout")
        respond_to_post("/user/createWithArray")
        respond_to_post("/user/createWithList")
        respond_to_put(r"/example/-?\d+")

        # Now just kick off the validation process.
        swaggercheck.api_conformance_test(
            PETSTORE_SCHEMA_PATH, cont_on_err=False
        )

    @responses.activate
    def test_openapi_uber(self):
        """An example Uber API spec from the OpenAPI examples is handled."""
        profile = {
            "first_name": "steve",
            "last_name": "stevenson",
            "email": "example@stevemail.com",
            "picture": "http://steve.com/stevepic.png",
            "promo_code": "12341234",
        }
        activities = {
            "offset": 123,
            "limit": 99,
            "count": 432,
            "history": [{"uuid": 9876543210}],
        }
        product = {
            "product_id": "example",
            "description": "it's a product",
            "display_name": "bestproductno1",
            "capacity": "4 hippos",
            "image": "http://hippotransports.com/hippocar.png",
        }
        products = [product]
        price_estimate = {
            "product_id": "example",
            "currency_code": "gbp",
            "display_name": "it's a product",
            "estimate": "123.50",
            "low_estimate": 123,
            "high_estimate": 124,
            "surge_multiplier": 22.2,
        }
        price_estimates = [price_estimate]

        # Handle all the basic endpoints.
        respond_to_get(r"/estimates/price\?.*", response_json=price_estimates)
        respond_to_get(r"/estimates/time\?.*", response_json=products)
        respond_to_get(r"/history\?.*", response_json=activities)
        respond_to_get("/me", response_json=profile)
        respond_to_get(r"/products\?.*", response_json=products)

        # Now just kick off the validation process.
        swaggercheck.api_conformance_test(UBER_SCHEMA_PATH, cont_on_err=False)


class MultiRequestTestCase(unittest.TestCase):
    """Test that multiple requests can be handled as part of single test."""

    @responses.activate
    def test_put_get_combined(self):
        """Test just to show how tests using multiple requests work."""

        def _get_request_callback(_):
            # Respond with the previously received body value.
            new_body = json.loads(responses.calls[-1].request.body)
            new_body["name"] = "example"
            return 200, {}, json.dumps(new_body)

        respond_to_put(r"/apps/.*", status=204)

        responses.add_callback(
            responses.GET,
            re.compile(SCHEMA_URL_BASE + "/apps/"),
            callback=_get_request_callback,
            content_type=CONTENT_TYPE_JSON,
        )

        my_val_factory = swaggercheck.strategies.StrategyFactory()
        client = swaggercheck.client.Client(TEST_SCHEMA_PATH)
        put_operation = client.api.endpoints["/apps/{appid}"]["put"]
        put_strategy = put_operation.parameters_strategy(my_val_factory)
        get_operation = client.api.endpoints["/apps/{appid}"]["get"]
        get_strategy = get_operation.parameters_strategy(my_val_factory)

        @hypothesis.settings(
            max_examples=50,
            suppress_health_check=[hypothesis.HealthCheck.too_slow],
        )
        @hypothesis.given(put_strategy, get_strategy)
        def single_operation_test(
            client, put_operation, get_operation, put_params, get_params
        ):
            """PUT an app, then get it again."""
            result = client.request(put_operation, put_params)
            assert (
                result.status in put_operation.response_codes
            ), "{} not in {}".format(
                result.status, put_operation.response_codes
            )

            get_params["appid"] = put_params["appid"]
            result = client.request(get_operation, get_params)

            # Compare JSON representations of the data - as Python objects they
            # may contain NAN, instances of which are not equal to one another.
            out_data = json.dumps(result.body.data, sort_keys=True)
            in_data = json.dumps(put_params["payload"]["data"], sort_keys=True)
            assert out_data == in_data, "{!r} != {!r}".format(
                out_data, in_data
            )

        single_operation_test(
            client, put_operation, get_operation
        )  # pylint: disable=E1120


class ResponseTestCase(unittest.TestCase):
    """Test the Response class."""

    def test_insensitive_headers(self):
        """
        Verify that headers are case insensitive (See http://www.ietf.org/rfc/rfc2616.txt)...

             'Each header field consists of a name followed by a colon (":") and the field value.
              Field names are case-insensitive.'
        """
        raw_response = unittest.mock.Mock()
        content_type = "application/json"
        raw_response.header = {"content-type": [content_type]}
        response = swaggercheck.response.Response(raw_response)
        assert response.headers["CoNTenT-tyPe"] == [content_type]


if __name__ == "__main__":
    unittest.main()
