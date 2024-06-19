import dataclasses

from fhirmodels.fhir_package import FhirPackage

import constants as c


@dataclasses.dataclass
class ProfileMapElement:
    is_primitive: bool
    full_path: str
    element: dict


class ProfileMap:
    def __init__(self, map: dict[str, ProfileMapElement]):
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


class ProfileMapBuilder:
    def __init__(self, package: "FhirPackage"):
        self.package = package

    def build_from_profile(self, profile: dict) -> ProfileMap:
        map = {}

        def process(element: dict, parent_path: str, rec_level: int):
            if self.is_invalid_element(element) or rec_level > 5:
                return

            # Handle multi-type strings
            if self.is_multi_type_string(element["id"]):
                element_types = element["type"]
                for element_type in element_types:
                    code = element_type["code"]
                    code = code[0].upper() + code[1:]
                    new_element = {
                        **element,
                        "id": element["id"].replace("[x]", code),
                        "type": [element_type],
                    }
                    process(new_element, parent_path, rec_level + 1)
                return  # Ensure we don't process the original multi-type element further

            full_path = self.get_full_path(element, parent_path)

            if self.is_primitive_element(element):
                map[full_path] = ProfileMapElement(
                    is_primitive=True, full_path=full_path, element=element
                )
            elif self.is_complex_element(element):
                map[full_path] = ProfileMapElement(
                    is_primitive=False, full_path=full_path, element=element
                )
                children_type_defs = [
                    sd
                    for types in element.get("type", [])
                    for sd in self.package.structure_definitions
                    if sd["id"] == types["code"]
                ]

                for child in children_type_defs:
                    if self.is_primitive_kind(child):
                        child_element = child["snapshot"]["element"][0]
                        child_full_path = self.get_full_path(child_element, full_path)
                        map[child_full_path] = ProfileMapElement(
                            is_primitive=True,
                            full_path=child_full_path,
                            element=child_element,
                        )
                    else:
                        process(
                            child["snapshot"]["element"][0], full_path, rec_level + 1
                        )
                        for child_element in child["snapshot"]["element"][1:]:
                            process(child_element, full_path, rec_level + 1)

        if "snapshot" in profile:
            for element in profile["snapshot"]["element"]:
                process(element, "", 0)

        return ProfileMap(map)

    def is_primitive_element(self, element: dict):
        if "type" in element:
            return element["type"][0].get("code") in c.PRIMITIVE_ELEMENT_TYPES

    def is_invalid_element(self, element: dict):
        # ignore extension for now
        if element.get("id", "").startswith("Extension"):
            return True
        if not "type" in element:
            return True
        if element.get("base", {}).get("path").startswith("Element"):
            return True

    def is_contained_element(self, element: dict):
        if "type" in element:
            return element["type"][0].get("code") in c.CONTAINED_ELEMENT_TYPES

    def is_complex_element(self, element: dict):
        if "type" in element:
            return element["type"][0].get("code") in c.COMPLEX_ELEMENT_TYPES

    def is_multi_type_string(self, input: str):
        return "[x]" in input

    def is_primitive_kind(self, structure_definition: dict):
        return structure_definition["kind"] == c.PRIMITIVE_KIND

    def is_complex_kind(self, structure_definition: dict):
        return structure_definition["kind"] == c.COMPLEX_KIND

    def get_full_path(self, element: dict, parent_path: str):
        id = element.get("id")
        suffix = id.split(".")[1:]
        suffix = ".".join(suffix)
        if self.element_is_array(element):
            suffix += "[i]"
        return f"{parent_path}.{suffix}" if parent_path else suffix

    def element_is_array(self, element: dict):
        if "max" in element:
            max_val = element["max"]
            return max_val == "*" or int(max_val) > 1
