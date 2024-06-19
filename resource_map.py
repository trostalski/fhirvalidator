from typing import Any
from pprint import pprint

from fhirmodels.fhir_package import FhirPackage
import constants as c
import dataclasses


@dataclasses.dataclass
class ResourceMapElement:
    path: str
    profile_path: str
    cardinality: int
    is_primitive: bool
    value: str | int | None = None
    value_domain: str | None = None
    coding_bindings: str | None = None
    invariants: str | None = None
    value: Any = None


class ResourceMap:
    def __init__(self, map: dict[str, ResourceMapElement]):
        self._map = map

    def __iter__(self):
        return iter(self._map)

    def __getitem__(self, key):
        return self._map[key]

    def __contains__(self, key):
        return key in self._map

    @property
    def map(self):
        return self._map


class ResourceMapBuilder:

    def __init__(self):
        pass

    def build_from_dict(cls, resource: dict):
        _map = {}

        def process(
            element: list | dict,
            parent_path: str,
            parent_profile_path: str,
            cardinality: int = 1,
        ):
            if parent_path == "resourceType":
                return
            if isinstance(element, dict):
                el = ResourceMapElement(
                    path=parent_path,
                    profile_path=parent_profile_path,
                    value=None,
                    cardinality=cardinality,
                    is_primitive=False,
                )
                _map[parent_path] = el
                for key, value in element.items():
                    new_path = f"{parent_path}.{key}" if parent_path else key
                    process(value, f"{new_path}", f"{parent_profile_path}.{key}")
            elif isinstance(element, list):
                for i, value in enumerate(element):
                    new_path = f"{parent_path}[{i}]"
                    process(
                        value,
                        f"{new_path}",
                        f"{parent_profile_path}[x]",
                        cardinality=len(element),
                    )
            else:
                el = ResourceMapElement(
                    path=parent_path,
                    profile_path=parent_profile_path,
                    value=element,
                    is_primitive=True,
                    cardinality=1,
                )
                _map[parent_path] = el

        for key, value in resource.items():
            process(value, key, key)

        return ResourceMap(map=_map)
