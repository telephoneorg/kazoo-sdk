import logging
import json
from collections import OrderedDict

from .client import Client


VERSION = '0.2.4'


# monkey-patch json to deserialize into ordered dictionaries, to preserve the
# order of keys in json objects.

# Some kazoo configs rely on this behavior!

json._default_decoder = json.JSONDecoder(
    object_hook=None,
    object_pairs_hook=OrderedDict
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
