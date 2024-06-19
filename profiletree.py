import dataclasses
import typing as t

from fhirmodels.fhir_package import FhirPackage

import constants as c
import utils


class ResourceTreeBuilder:
    def __init__(self):
        pass

    def build_from_json(self, resource: dict):
        nodes: list[ResourceTreeNode] = []

        def build_node(element, path):
            if isinstance(element, dict):
                children = []
                for key, value in element.items():
                    if path:
                        new_path = f"{path}.{key}"
                    else:
                        new_path = key
                    children.append(build_node(value, f"{new_path}"))
                return ResourceTreeNode(path, False, children=children)
            elif isinstance(element, list):
                children = []
                for i, value in enumerate(element):
                    children.append(build_node(value, f"{path}[{i}]"))
                return ResourceTreeNode(path, False, children=children)
            else:
                return ResourceTreeNode(path, True, element)

        for key, value in resource.items():
            nodes.append(build_node(value, key))

        return ResourceTree(nodes)


class ResourceTreeNode:
    def __init__(
        self,
        path: str,
        is_primitive: bool,
        value: str | int | None = None,
        children: list["ResourceTreeNode"] = None,
    ):
        self.children = children
        self.path = path
        self.is_primitive = is_primitive
        self.value = value

    def __repr__(self) -> str:
        return f"ResourceTreeNode(path={self.path}, is_primitive={self.is_primitive}, value={self.value})"


class ResourceTree:
    def __init__(self, nodes: list[ResourceTreeNode]):
        self.nodes = nodes

    @property
    def flattened(self):
        def flatten(node: ResourceTreeNode):
            if node.is_primitive:
                return [node]
            else:
                return [node] + [
                    child for child in node.children for child in flatten(child)
                ]

        return [node for node in self.nodes for node in flatten(node)]

    def bfs(self):
        queue: list[ResourceTreeNode] = []
        for node in self.nodes:
            queue.append(node)
        while queue:
            node = queue.pop(0)
            if node.children:
                for child in node.children:
                    queue.append(child)
            yield node

    @property
    def size(self):
        return len(self.nodes)


class ProfileTreeBuilder:
    def __init__(self, package: "FhirPackage"):
        self.package = package

    def build_from_snapshot(self, snapshot: list[dict]) -> "ProfileTree":
        nodes: list[ProfileTreeNode] = []

        def build_node(
            element: dict,
            path: str,
            parent_path: str,
            rec_depth: int = c.MAX_RECURSION_DEPTH,
        ):
            print("BUILDING", path)
            full_path = ".".join([parent_path, path]).strip(".")
            if utils.is_invalid_element(element) or rec_depth == 0:
                return None
            elif utils.is_primitive_element(element):
                nodes.append(
                    ProfileTreeNode(
                        full_path=full_path,
                        element=element,
                        is_primitive=True,
                        children=None,
                    )
                )
            elif utils.is_contained_element(element):
                return
            elif utils.is_complex_element(element):
                children_type_defs = [
                    sd
                    for types in element["type"]
                    for sd in self.package.structure_definitions
                    if sd["id"] == types["code"]
                ]

                for child in children_type_defs:
                    if utils.is_primitive_kind(child):
                        nodes.append(
                            ProfileTreeNode(
                                full_path=full_path,
                                element=element,
                                is_primitive=True,
                                children=None,
                            )
                        )
                    else:
                        for child_element in child["snapshot"]["element"]:
                            build_node(
                                child_element,
                                child_element["id"],
                                full_path,
                                rec_depth - 1,
                            )

        for element in snapshot:
            build_node(element, element["id"], "")

        return ProfileTree(nodes)


@dataclasses.dataclass
class ProfileTreeNode:
    full_path: str
    element: dict
    is_primitive: bool
    children: list["ProfileTreeNode"] | None = None


class ProfileTree:
    def __init__(self, nodes: list[ProfileTreeNode]):
        self.nodes = nodes
