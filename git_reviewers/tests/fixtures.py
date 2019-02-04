import copy
import json
from typing import Dict, Any

PHAB_DEFAULT: Dict[str, Dict[str, Any]] = {
    'response': {
        'data': []
    }
}

PHAB_ACTIVATED = copy.deepcopy(PHAB_DEFAULT)
PHAB_ACTIVATED['response']['data'] = \
    [{'fields': {'roles': ['activated']}}]

PHAB_DISABLED = copy.deepcopy(PHAB_DEFAULT)
PHAB_DISABLED['response']['data'] = \
    [{'fields': {'roles': ['disabled']}}]

PHAB_DEFAULT_DATA = json.dumps(PHAB_DEFAULT).encode("utf-8")
PHAB_ACTIVATED_DATA = json.dumps(PHAB_ACTIVATED).encode("utf-8")
PHAB_DISABLED_DATA = json.dumps(PHAB_DISABLED).encode("utf-8")
