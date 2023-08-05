"""
Provides a codec for converting between JSON representations of objects and
the objects themselves.
"""
import logging

from pyswagger.primitives import SwaggerPrimitive
from pyswagger.primitives._int import validate_int, create_int
from pyswagger.primitives._float import validate_float, create_float

from .schema import Primitive

# pyswagger and requests make INFO level logs regularly by default, so lower
# their logging levels to prevent the spam.
logging.getLogger("pyswagger").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

__all__ = ["CodecFactory"]


log = logging.getLogger(__name__)


class CodecFactory:
    """Produces codecs that encode objects as JSON and decode JSON back into
    objects.
    """

    def __init__(self):
        self._factory = SwaggerPrimitive()

        # Pyswagger doesn't support integers or floats without a 'format', even
        # though it does seem valid for a spec to not have one.
        # We work around this by adding support for these types without format.
        # See here: https://github.com/mission-liao/pyswagger/issues/65
        self._factory.register("integer", None, create_int, validate_int)
        self._factory.register("number", None, create_float, validate_float)

    def register(self, type_str, format_str, creator):
        """Register a new creator for objects of the given type and format.

        The ``creator`` parameter must be a `callable` which takes the
        following paramters in order:

        - `schema.Primitive` - the Swagger schema for the object being handled.
        - The value to use to build the object - may be the applicable portion
          of JSON after `json.loads` processing, or any supported input value
          for the relevant object.
        - `CodecFactory` - this factory, to be used to generate child objects
          if required, by calling the ``produce`` method on it.

        :param type_str: The Swagger schema type to register for.
        :type type_str: str
        :param format_str: The Swagger schema format to register for.
        :type format_str: str
        :param creator: The callable to create an object of the desired type.
        :type creator: callable
        """
        # Map from the internal pyswagger call and paramters to the one we want
        # to expose to users.

        def internal_creator(obj, val, ctx):
            return creator(Primitive(obj), val, self)

        self._factory.register(type_str, format_str, internal_creator)

    def produce(self, swagger_definition, value):
        """Construct an object with the given value, represented by the given
        schema portion using the registered type/format mappings.

        :param swagger_definition: The Swagger schema type to register for.
        :type swagger_definition: schema.Primitive
        :param value: The value to use to build the object - may be the
                      applicable portion of JSON after `json.loads` processing,
                      or any supported input value for the relevant object.
        """
        return self._factory.produce(
            swagger_definition._pyswagger_definition,  # pylint: disable=protected-access
            value,
        )

    @property
    def _pyswagger_factory(self):
        """The underlying pyswagger primitive factory - useful elsewhere
        internally but not expected to be referenced external to the package.

        :rtype: pyswagger.primitives.SwaggerPrimitive
        """
        return self._factory
