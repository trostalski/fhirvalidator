import json
import dataclasses

import fhirmodels.R5 as FHIR

import constants as c


@dataclasses.dataclass
class FlatResourceElement:
    path: str
    value: str


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def flatten_resource(resource):
    def flatten_element(element, path):
        if isinstance(element, dict):
            for key, value in element.items():
                if path:
                    new_path = f"{path}.{key}"
                else:
                    new_path = key
                yield from flatten_element(value, f"{new_path}")
        elif isinstance(element, list):
            for i, value in enumerate(element):
                yield from flatten_element(value, f"{path}[{i}]")
        else:
            yield FlatResourceElement(path, element)

    return list(flatten_element(resource, ""))


def is_primitive_element(element: dict):
    if "type" in element:
        return element["type"][0].get("code") in c.PRIMITIVE_ELEMENT_TYPES


def is_invalid_element(element: dict):
    if not "type" in element:
        return True


def is_contained_element(element: dict):
    if "type" in element:
        return element["type"][0].get("code") in c.CONTAINED_ELEMENT_TYPES


def is_complex_element(element: dict):
    if "type" in element:
        return element["type"][0].get("code") in c.COMPLEX_ELEMENT_TYPES


def is_multi_type_string(input: str):
    return "[x]" in input


def is_primitive_kind(structure_definition: dict):
    return structure_definition["kind"] == c.PRIMITIVE_KIND


def is_complex_kind(structure_definition: dict):
    return structure_definition["kind"] == c.COMPLEX_KIND


def get_full_path(element: dict, parent_path: str):
    id = element.get("id")
    suffix = id.split(".")[1:]
    suffix = ".".join(suffix)
    return f"{parent_path}.{suffix}" if parent_path else suffix
