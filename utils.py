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


def remove_after_pipe(s: str) -> str:
    return s.split("|")[0]
