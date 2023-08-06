import os
from typing import List
import re
from hestia_earth.utils.tools import flatten, safe_parse_float, list_sum
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_term_match

from hestia_earth.validation.geojson import get_geojson_area
from hestia_earth.validation.gee import is_enabled, get_region_id
from hestia_earth.validation.utils import (
    update_error_path, _filter_list_errors, _next_error, _same_properties, _value_average,
    _find_linked_node, _list_has_props, _is_before_today, run_model_from_node
)


def validate_date_lt_today(node: dict, key: str):
    return node.get(key) is None or _is_before_today(node.get(key)) or {
        'level': 'error',
        'dataPath': f".{key}",
        'message': "must be lower than today's date"
    }


def validate_list_date_lt_today(node: dict, list_key: str, node_keys: list):
    def validate(values):
        index = values[0]
        value = values[1]
        errors = list(map(lambda key: {'key': key, 'error': validate_date_lt_today(value, key)}, node_keys))
        return _filter_list_errors(
            [update_error_path(error['error'], list_key, index) for error in errors if error['error'] is not True]
        )

    return _filter_list_errors(flatten(map(validate, enumerate(node.get(list_key, [])))))


def validate_dates(node: dict):
    start = node.get('startDate')
    end = node.get('endDate')
    return start is None or end is None or (len(start) <= 7 and len(end) <= 7 and end >= start) or end > start


def validate_list_dates(node: dict, list_key: str):
    def validate(values):
        value = values[1]
        index = values[0]
        return validate_dates(value) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].endDate",
            'message': 'must be greater than startDate'
        }

    return _filter_list_errors(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_list_dates_length(node: dict, list_key: str):
    def validate(values):
        value = values[1]
        index = values[0]
        expected = len(value.get('value'))
        return len(value.get('dates')) == expected or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].dates",
            'message': 'must contain ' + str(expected) + (' values' if expected > 1 else ' value')
        }

    results = list(map(validate, enumerate(_list_has_props(node.get(list_key), ['dates', 'value']))))
    return next((x for x in results if x is not True), True)


def _compare_min_max(value1, value2): return value1 <= value2


def _compare_list_min_max(list1: list, list2: list):
    def compare_enum(index: int):
        valid = _compare_min_max(list1[index], list2[index])
        return True if valid is True else index

    return len(list1) != len(list2) or \
        next((x for x in list(map(compare_enum, range(len(list1)))) if x is not True), True)


def validate_list_min_max(node: dict, list_key: str):
    def validate(values):
        value = values[1]
        index = values[0]
        min = value.get('min', 0)
        max = value.get('max', 0)
        skip_compare = (
            isinstance(min, list) and not isinstance(max, list)
        ) or (
            isinstance(max, list) and not isinstance(min, list)
        )
        compare_lists = isinstance(min, list) and isinstance(max, list)
        is_valid = True if skip_compare else \
            _compare_list_min_max(min, max) if compare_lists else _compare_min_max(min, max)
        return is_valid is True or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].max",
            'message': 'must be greater than min'
        }

    return _next_error(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_list_duplicates(node: dict, list_key: str, props: List[str]):
    def validate(values):
        value = values[1]
        index = values[0]
        values = node[list_key].copy()
        values.pop(index)
        duplicates = list(filter(_same_properties(value, props), values))
        return len(duplicates) == 0 or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}]",
            'message': f"Duplicates found. Please make sure there is only one entry with the same {', '.join(props)}"
        }

    return _next_error(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_list_term_percent(node: dict, list_key: str):
    def soft_validate(index: int, value): return 0 <= value and value <= 1 and {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'may be between 0 and 100'
        }

    def hard_validate(index: int, value): return (0 <= value and value <= 100) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'should be between 0 and 100 (percentage)'
        }

    def validate(values):
        index = values[0]
        value = values[1]
        units = value.get('term', {}).get('units', '')
        value = _value_average(value, None)
        return units != '%' or value is None or type(value) == str or \
            soft_validate(index, value) or hard_validate(index, value)

    return _filter_list_errors(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_region(node: dict, region_key='region'):
    country = node.get('country', {})
    region_id = node.get(region_key, {}).get('@id', '')
    return region_id[0:8] == country.get('@id') or {
        'level': 'error',
        'dataPath': f".{region_key}",
        'message': 'must be within the country',
        'params': {
            'country': country.get('name')
        }
    }


def validate_country(node: dict):
    country_id = node.get('country', {}).get('@id', '')
    # handle additional regions used as country, like region-world
    is_region = country_id.startswith('region-')
    return is_region or bool(re.search(r'GADM-[A-Z]{3}', country_id)) or {
        'level': 'error',
        'dataPath': '.country',
        'message': 'must be a country'
    }


def need_validate_coordinates(node: dict): return is_enabled() and 'latitude' in node and 'longitude' in node


def validate_coordinates(node: dict, region_key='region'):
    latitude = node.get('latitude')
    longitude = node.get('longitude')
    country = node.get('country', {})
    region = node.get(region_key)
    gadm_id = region.get('@id') if region else country.get('@id')
    id = get_region_id(gadm_id, latitude=latitude, longitude=longitude)
    return gadm_id == id or {
        'level': 'error',
        'dataPath': f".{region_key}" if region else '.country',
        'message': 'does not contain latitude and longitude',
        'params': {
            'gadmId': id
        }
    }


def need_validate_area(node: dict): return 'area' in node and 'boundary' in node


def validate_area(node: dict):
    try:
        area = get_geojson_area(node.get('boundary'))
        return area == round(node.get('area'), 1) or {
            'level': 'error',
            'dataPath': '.area',
            'message': f"must be equal to boundary (~{area})"
        }
    except KeyError:
        # if getting the geojson fails, the geojson format is invalid
        # and the schema validation step will detect it
        return True


N_A_VALUES = [
    '#n/a',
    '#na',
    'n/a',
    'na',
    'n.a',
    'nodata',
    'no data'
]


def validate_empty_fields(node: dict):
    keys = list(filter(lambda key: isinstance(node.get(key), str), node.keys()))

    def validate(key: str):
        return not node.get(key).lower() in N_A_VALUES or {
            'level': 'warning',
            'dataPath': f".{key}",
            'message': 'may not be empty'
        }

    return _filter_list_errors(list(map(validate, keys)), False)


def validate_linked_source_privacy(node: dict, key: str, nodes: list):
    related_source = _find_linked_node(nodes, node.get(key, {}))
    node_privacy = node.get('dataPrivate')
    related_source_privacy = related_source.get('dataPrivate') if related_source else None
    return related_source_privacy is None or node_privacy == related_source_privacy or {
        'level': 'error',
        'dataPath': '.dataPrivate',
        'message': 'should have the same privacy as the related source',
        'params': {
            'dataPrivate': node_privacy,
            key: {
                'dataPrivate': related_source_privacy
            }
        }
    }


def _property_default_value(term_id: str, property: dict):
    # load the term defaultProperties and find the matching property
    term = download_hestia(term_id)
    return safe_parse_float(
        find_term_match(term.get('defaultProperties', []), property.get('term', {}).get('@id')).get('value')
    )


def value_difference(value: float, expected_value: float):
    """
    Get the difference in percentage between a value and the expected value.

    Parameters
    ----------
    value : float
        The value to check.
    expected_value : float
        The expected value.

    Returns
    -------
    bool
        The difference in percentage between the value and the expected value.
    """
    return 0 if expected_value == 0 else round(abs(value - expected_value) / expected_value, 4)


def is_value_different(value: float, expected_value: float, delta: float = 0.05) -> bool:
    """
    Check the difference in percentage between a value and the expected value.

    Parameters
    ----------
    value : float
        The value to check.
    expected_value : float
        The value it should be close to.
    delta : float
        The accepted difference between the value and the expected one. Defaults to `5%`.

    Returns
    -------
    bool
        `True` if the value is within the percentage of the expected value, `False` otherwise.
    """
    return value_difference(value, expected_value) > delta


def validate_properties_default_value(node: dict, list_key: str, properties_key: str):
    def validate_properties(term_id: str, values: list):
        index = values[0]
        prop = values[1]
        value = safe_parse_float(prop.get('value'))
        default_value = _property_default_value(term_id, prop)
        delta = value_difference(value, default_value)
        return delta < 0.25 or {
            'level': 'warning',
            'dataPath': f".{properties_key}[{index}].value",
            'message': 'should be within percentage of default value',
            'params': {
                'current': value,
                'default': default_value,
                'percentage': delta * 100
            }
        }

    def validate_nodes(values):
        index = values[0]
        value = values[1]
        term_id = value.get('term', {}).get('@id')
        errors = _filter_list_errors(
            flatten(map(lambda v: validate_properties(term_id, v), enumerate(value.get(properties_key, [])))), False
        )
        return [update_error_path(error, list_key, index) for error in errors]

    return _filter_list_errors(flatten(map(validate_nodes, enumerate(node.get(list_key, [])))))


def _validate_list_model(node: dict, list_key: str):
    def validate(values: tuple):
        index, blank_node = values
        try:
            value = blank_node.get('value', [])
            value = list_sum(value, value)

            expected = run_model_from_node(blank_node, node)
            expected_value = expected[0].get('value', []) if isinstance(expected, list) else expected.get('value', [])
            expected_value = list_sum(expected_value, expected_value)

            delta = value_difference(value, expected_value)
            return delta < 0.05 or {
                'level': 'error',
                'dataPath': f".{list_key}[{index}].value",
                'message': 'the value provided is not consistent with the model result',
                'params': {
                    'model': blank_node.get('methodModel', {}),
                    'term': blank_node.get('term', {}),
                    'current': value,
                    'expected': expected_value,
                    'delta': delta * 100
                }
            }
        except ModuleNotFoundError:
            return True
    return validate


def validate_list_model(node: dict, list_key: str):
    run = os.environ.get('VALIDATE_MODELS', 'true') == 'true'
    nodes = node.get(list_key, [])
    return _filter_list_errors(map(_validate_list_model(node, list_key), enumerate(nodes))) if run else []
