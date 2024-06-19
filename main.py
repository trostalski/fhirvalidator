# Validating a resource means, checking that the following aspects of the resource are valid:

# Structure: Check that all the content in the resource is described by the specification, and nothing extra is present
# Cardinality: Check that the cardinality of all properties is correct (min & max)
# Value Domains: Check that the values of all properties conform to the rules for the specified types (including checking that enumerated codes are valid)
# Coding/CodeableConcept bindings: Check that codes/displays provided in the Coding/CodeableConcept types are valid
# Invariants: Check that the invariants (co-occurrence rules, etc.) have been followed correctly
# Profiles: Check that any rules in profiles have been followed (including those listed in the Resource.meta.profile, or in CapabilityStatement, or in an ImplementationGuide, or otherwise required by context)
# Questionnaires: Check that a QuestionnaireResponse is valid against its matching Questionnaire
# Business Rules: Business rules are made outside the specification, such as checking for duplicates, checking that references resolve, checking that a user is authorized to do what they want to do, etc.

import re
import json

from fhirmodels.fhir_package import FhirPackage, FhirPackageLoader

import resource_map
import profile_map


def replace_index(path: str) -> str:
    return re.sub(r"\[\d+\]", "[i]", path)


def check_valid_json(input):
    if isinstance(input, str):
        try:
            json.loads(input)
        except ValueError as e:
            raise Exception("Invalid JSON")
    elif isinstance(input, dict):
        try:
            json.dumps(input)
        except ValueError as e:
            raise Exception("Invalid JSON")
    else:
        raise Exception("Invalid JSON")


def check_structure(rm: resource_map.ResourceMap, pm: profile_map.ProfileMap):
    # iterate over all elements in the resource and check if the full_path is in the ProfileTree
    for r_path in rm:
        r_path = replace_index(r_path)
        if r_path not in pm:
            print(f"Element {r_path} not in ProfileTree")
            raise Exception("Invalid Structure")


def check_cardinality(rm: resource_map.ResourceMap, pm: profile_map.ProfileMap):
    # iterate over elements in the resource and check if the cardinality is correct
    for r_path, r_element in rm.map.items():
        r_path = replace_index(r_path)
        r_card = r_element.cardinality

        p_max = pm[r_path].element.get("max")
        p_max = int(p_max) if p_max != "*" else "*"
        p_min = int(pm[r_path].element.get("min"))

        if r_card < p_min:
            print(
                f"Cardinality error: expected {p_min} but found {r_card} for element {r_path}"
            )
            raise Exception("Invalid Cardinality")
        elif p_max == "*":
            pass
        elif r_card > p_max:
            print(
                f"Cardinality error: expected {p_min} but found {r_card} for element {r_path}"
            )
            raise Exception("Invalid Cardinality")


def check_value_domains(rm: resource_map.ResourceMap, pm: profile_map.ProfileMap):
    # iterate over elements in the resource and check if the value domain is correct
    for r_path, r_element in rm.map.items():
        r_path = replace_index(r_path)
        p_el = pm[r_path]
        print(r_path, r_element.value, p_el.element.get("type"))


def check_coding_bindings():
    # iterate over elements in the resource and check if the coding bindings are correct
    pass


def check_invariants():
    # check rules of profile
    pass


def check_profiles():
    pass


def try_get_profile(resource: dict, package: FhirPackage) -> dict | None:
    profile = None
    if resource.get("meta") and resource["meta"].get("profile"):
        pass
    else:
        package_struc_defs = package.base_resource_structure_definitions
        for profile in package_struc_defs:
            if profile["type"] == resource["resourceType"]:
                return profile
    return profile


def validate(
    resource: dict,
    version: str | None = "R4",
    profile: dict | None = None,
):
    check_valid_json(resource)
    loader = FhirPackageLoader()
    base_package = loader.load_from_version(fhir_version=version)

    if not profile:
        profile = try_get_profile(resource=resource, package=base_package)
        if not profile:
            raise Exception("No profile found for resource")

    rm = resource_map.ResourceMapBuilder().build_from_dict(resource)
    pm = profile_map.ProfileMapBuilder(package=base_package).build_from_profile(profile)

    check_structure(rm, pm)
    check_cardinality(rm, pm)
    check_value_domains(rm, pm)
    return rm, pm


if __name__ == "__main__":
    pass
