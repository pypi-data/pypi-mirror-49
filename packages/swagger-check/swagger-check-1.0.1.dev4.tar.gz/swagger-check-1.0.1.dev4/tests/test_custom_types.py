"""
Tests of using custom types with the swaggerconformance package.
"""
import unittest
import os.path as osp
import json
import string

import responses
import hypothesis
import hypothesis.strategies as hy_st

import swaggercheck


TEST_SCHEMA_DIR = osp.relpath(
    osp.join(osp.dirname(osp.realpath(__file__)), "test_schemas/")
)
COLOUR_TYPE_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, "colour_custom_type.json")
SCHEMA_URL_BASE = "http://127.0.0.1:5000/api"
CONTENT_TYPE_JSON = "application/json"


class HexColourStrTemplate(
    swaggercheck.strategies.primitivestrategies.PrimitiveStrategy
):
    """Template for a hex colour value."""

    def __init__(self, swagger_definition, factory):
        super().__init__(swagger_definition, factory)
        self._enum = swagger_definition.enum

    def strategy(self):
        if self._enum:
            return hy_st.sampled_from(self._enum)

        strategy = hy_st.text(
            alphabet=list(set(string.hexdigits)), min_size=6, max_size=6
        )
        # Don't forget to add the leading `#`.
        strategy = strategy.map(lambda x: "#" + x)

        return strategy


class ColourObjTemplate(HexColourStrTemplate):
    """Template for a hex colour value."""

    def strategy(self):
        return super().strategy().map(Colour)


class SceneTemplate(
    swaggercheck.strategies.primitivestrategies.PrimitiveStrategy
):
    """Template for a Scene object."""

    def __init__(self, swagger_definition, factory):
        super().__init__(swagger_definition, factory)
        self._foreground = ColourObjTemplate(swagger_definition, factory)
        self._background = ColourObjTemplate(swagger_definition, factory)

    def strategy(self):
        return hy_st.builds(
            Scene, self._foreground.strategy(), self._background.strategy()
        )


class Colour:
    """Simple representation of a colour."""

    def __init__(self, value):
        if isinstance(value, str):
            self._int_value = int(value.lstrip("#"), base=16)
        elif isinstance(value, int):
            self._int_value = value
        else:
            raise AssertionError("Invalid Type")

    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, str):
            other = Colour(other)
        if not isinstance(other, Colour):
            return NotImplemented
        return self.int == other.int

    @property
    def int(self):
        """Get the colour as an integer."""
        return self._int_value

    @property
    def hex(self):
        """Get the colour as a hex string with leading ``#``."""
        return "#{0:06x}".format(self._int_value)


class ColourIntCodec(Colour):
    """Codec for translating between `Colour` and JSON."""

    def __init__(self, _, value, __):
        if isinstance(value, Colour):
            value = value.int
        super().__init__(value)

    def to_json(self):
        """Return the appropriate JSON representation of the `Colour` ."""
        return self.int


class Scene:
    """Object to contain subobjects for testing."""

    def __init__(self, foreground_colour, background_colour):
        self.foreground_colour = foreground_colour
        self.background_colour = background_colour

    def __eq__(self, other):
        if not isinstance(other, Scene):
            return NotImplemented
        return (
            self.foreground_colour == other.foreground_colour
            and self.background_colour == other.background_colour
        )


class SceneCodec(Scene):
    """Codec for translating between `Scene` and JSON."""

    def __init__(self, swagger_definition, value, factory):
        if isinstance(value, Scene):
            fore_value = value.foreground_colour
            back_value = value.background_colour
        elif isinstance(value, dict):
            fore_value = value["foreground colour"]
            back_value = value["background colour"]
        else:
            raise AssertionError("Invalid parameters")

        fore_def = swagger_definition.properties.get("foreground colour")
        back_def = swagger_definition.properties.get("background colour")
        super().__init__(
            factory.produce(fore_def, fore_value),
            factory.produce(back_def, back_value),
        )

    def to_json(self):
        """Return the appropriate JSON representation of the `Scene` ."""
        return {
            "foreground colour": self.foreground_colour.to_json(),
            "background colour": self.background_colour.to_json(),
        }


class CustomTypeTestCase(unittest.TestCase):
    """Test that custom types can be registered and used correctly."""

    def test_colour_type_reg_for_fmt(self):
        """Test registering a template for a specific type/format works."""
        value_factory = swaggercheck.strategies.StrategyFactory()
        value_factory.register("string", "hexcolour", HexColourStrTemplate)
        self._run_test_colour_type(value_factory)

    def test_colour_type_default_fmt(self):
        """Test registering a default template for a type works."""
        value_factory = swaggercheck.strategies.StrategyFactory()
        value_factory.register_type_default("string", HexColourStrTemplate)
        self._run_test_colour_type(value_factory)

    @responses.activate
    def _run_test_colour_type(self, value_factory):
        """Test just to show how tests using multiple requests work."""

        def _get_request_callback(_):
            # Respond with the previously received body value.
            raw_val = json.loads(responses.calls[-1].request.body)["hexcolour"]
            int_val = int(raw_val.lstrip("#"), 16)
            return 200, {}, json.dumps({"intcolour": int_val})

        responses.add(
            responses.POST,
            SCHEMA_URL_BASE + "/example",
            json={"id": 1},
            content_type=CONTENT_TYPE_JSON,
        )
        responses.add(
            responses.PUT,
            SCHEMA_URL_BASE + "/example/1/hexcolour",
            content_type=CONTENT_TYPE_JSON,
            status=204,
        )

        responses.add_callback(
            responses.GET,
            SCHEMA_URL_BASE + "/example/1/intcolour",
            callback=_get_request_callback,
            content_type=CONTENT_TYPE_JSON,
        )

        client = swaggercheck.client.Client(COLOUR_TYPE_SCHEMA_PATH)
        post_operation = client.api.endpoints["/example"]["post"]
        put_operation = client.api.endpoints["/example/{int_id}/hexcolour"][
            "put"
        ]
        put_strategy = put_operation.parameters_strategy(value_factory)
        get_operation = client.api.endpoints["/example/{int_id}/intcolour"][
            "get"
        ]
        get_strategy = get_operation.parameters_strategy(value_factory)

        @hypothesis.settings(
            max_examples=50,
            suppress_health_check=[hypothesis.HealthCheck.too_slow],
        )
        @hypothesis.given(put_strategy, get_strategy)
        def single_operation_test(
            client, put_operation, get_operation, put_params, get_params
        ):
            """PUT an colour in hex, then GET it again as an int."""
            result = client.request(post_operation, {})
            assert (
                result.status in post_operation.response_codes
            ), "{} not in {}".format(
                result.status, post_operation.response_codes
            )

            int_id = result.body.id
            put_params["int_id"] = int_id
            result = client.request(put_operation, put_params)
            assert (
                result.status in put_operation.response_codes
            ), "{} not in {}".format(
                result.status, put_operation.response_codes
            )

            get_params["int_id"] = int_id
            result = client.request(get_operation, get_params)
            assert (
                result.status in get_operation.response_codes
            ), "{} not in {}".format(
                result.status, get_operation.response_codes
            )

            # Compare JSON representations of the data - as Python objects they
            # may contain NAN, instances of which are not equal to one another.
            out_data = result.body.intcolour
            in_data = int(put_params["payload"]["hexcolour"].lstrip("#"), 16)
            assert out_data == in_data, "{!r} != {!r}".format(
                out_data, in_data
            )

        single_operation_test(
            client, put_operation, get_operation
        )  # pylint: disable=E1120


class ValueCodecTestCase(unittest.TestCase):
    """Test that custom types can be mapped to/from and used correctly."""

    def test_colour_int_codec(self):
        """Generate `Colour` objects and translate them to `int` at the point
        of building the JSON body, so the test only accesses `Colour` objects.
        """
        value_factory = swaggercheck.strategies.StrategyFactory()
        value_factory.register("integer", "intcolour", ColourObjTemplate)

        codec = swaggercheck.codec.CodecFactory()
        codec.register("integer", "intcolour", ColourIntCodec)

        self._run_test_colour_type(codec, value_factory)

    def test_colour_int_codec_with_hex(self):
        """Generating hex strings for '`intcolour`' fields still means they are
        converted to `Colour` objects and then to `int` inside the JSON.
        """
        value_factory = swaggercheck.strategies.StrategyFactory()
        value_factory.register("integer", "intcolour", HexColourStrTemplate)

        codec = swaggercheck.codec.CodecFactory()
        codec.register("integer", "intcolour", ColourIntCodec)

        self._run_test_colour_type(codec, value_factory)

    @responses.activate
    def _run_test_colour_type(self, codec, value_factory):
        """Test just to show how tests using multiple requests work."""

        def _get_request_callback(_):
            # Respond with the previously received body value.
            int_val = json.loads(responses.calls[-1].request.body)["intcolour"]
            assert isinstance(int_val, int)
            return 200, {}, json.dumps({"intcolour": int_val})

        responses.add(
            responses.PUT,
            SCHEMA_URL_BASE + "/example/1/intcolour",
            content_type=CONTENT_TYPE_JSON,
            status=204,
        )
        responses.add_callback(
            responses.GET,
            SCHEMA_URL_BASE + "/example/1/intcolour",
            callback=_get_request_callback,
            content_type=CONTENT_TYPE_JSON,
        )

        client = swaggercheck.client.Client(COLOUR_TYPE_SCHEMA_PATH, codec)
        put_operation = client.api.endpoints["/example/{int_id}/intcolour"][
            "put"
        ]
        put_strategy = put_operation.parameters_strategy(value_factory)
        get_operation = client.api.endpoints["/example/{int_id}/intcolour"][
            "get"
        ]

        @hypothesis.settings(
            max_examples=50,
            suppress_health_check=[hypothesis.HealthCheck.too_slow],
        )
        @hypothesis.given(put_strategy)
        def single_operation_test(
            client, put_operation, get_operation, put_params
        ):
            """PUT an colour in hex, then GET it again as an int."""
            put_params["int_id"] = 1
            result = client.request(put_operation, put_params)
            assert (
                result.status in put_operation.response_codes
            ), "{} not in {}".format(
                result.status, put_operation.response_codes
            )

            result = client.request(get_operation, {"int_id": 1})
            assert (
                result.status in get_operation.response_codes
            ), "{} not in {}".format(
                result.status, get_operation.response_codes
            )

            out_data = result.body.intcolour
            assert isinstance(out_data, Colour)
            in_data = put_params["payload"]["intcolour"]
            assert out_data == in_data, "{!r} != {!r}".format(
                out_data, in_data
            )

        single_operation_test(
            client, put_operation, get_operation
        )  # pylint: disable=E1120


class ObjectCodecTestCase(unittest.TestCase):
    """Test that custom types can be mapped to/from and used correctly."""

    def test_scene_codec(self):
        """Test that JSON objects can be converted at both test edges."""
        value_factory = swaggercheck.strategies.StrategyFactory()
        value_factory.register("integer", "intcolour", ColourObjTemplate)
        value_factory.register("object", "scene", SceneTemplate)

        codec = swaggercheck.codec.CodecFactory()
        codec.register("integer", "intcolour", ColourIntCodec)
        codec.register("object", "scene", SceneCodec)

        self._run_test_colour_type(codec, value_factory)

    @responses.activate
    def _run_test_colour_type(self, codec, value_factory):
        """Test just to show how tests using multiple requests work."""

        def _get_request_callback(_):
            # Respond with the previously received body value.
            return 200, {}, responses.calls[-1].request.body

        responses.add(
            responses.PUT,
            SCHEMA_URL_BASE + "/scenes/1",
            content_type=CONTENT_TYPE_JSON,
            status=204,
        )
        responses.add_callback(
            responses.GET,
            SCHEMA_URL_BASE + "/scenes/1",
            callback=_get_request_callback,
            content_type=CONTENT_TYPE_JSON,
        )

        client = swaggercheck.client.Client(COLOUR_TYPE_SCHEMA_PATH, codec)
        put_operation = client.api.endpoints["/scenes/{int_id}"]["put"]
        put_strategy = put_operation.parameters_strategy(value_factory)
        get_operation = client.api.endpoints["/scenes/{int_id}"]["get"]

        @hypothesis.settings(
            max_examples=50,
            suppress_health_check=[hypothesis.HealthCheck.too_slow],
        )
        @hypothesis.given(put_strategy)
        def single_operation_test(
            client, put_operation, get_operation, put_params
        ):
            """PUT a scene object, then GET it again as a scene object."""
            put_params["int_id"] = 1
            result = client.request(put_operation, put_params)
            assert (
                result.status in put_operation.response_codes
            ), "{} not in {}".format(
                result.status, put_operation.response_codes
            )

            result = client.request(get_operation, {"int_id": 1})
            assert (
                result.status in get_operation.response_codes
            ), "{} not in {}".format(
                result.status, get_operation.response_codes
            )

            out_data = result.body
            self.assertIsInstance(out_data, Scene)
            in_data = put_params["payload"]
            self.assertIsInstance(in_data, Scene)
            assert out_data == in_data, "{!r} != {!r}".format(
                out_data, in_data
            )

        single_operation_test(
            client, put_operation, get_operation
        )  # pylint: disable=E1120


if __name__ == "__main__":
    unittest.main()
