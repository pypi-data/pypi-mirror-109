import logging
import re
from typing import Any, Dict, List, Optional

from pylsp.lsp import CompletionItemKind, SymbolKind
from pylsp.plugins.jedi_completion import _TYPE_MAP
from pylsp.plugins.symbols import _SYMBOL_KIND_MAP
from pylsp.workspace import Document

RE_START_TREE_PATH = re.compile(r"[\w|\.]*$")
RE_END_TREE_PATH = re.compile(r"^[\w]*")
RE_TREE_PATH = re.compile(r"hub\.([\w|\.]*)")
log = logging.getLogger(__name__)


def tree_path_under_cursor(
    hub, document: Document, position: Dict[str, int]
) -> Optional[str]:
    """
    Return the pop-tree path under the cursor.

    :param document: pylsp.workspace.Document
    :param position: {"line": int, "character": int}
    :returns: the pop_tree path or None
    :examples: (the <pipe> character represents the cursor position)
        hub.pyls_pop.utils.tree_pa|th_under_cursor -> hub.pyls_pop.utils.tree_path_under_cursor
        hub.pyls_pop.uti|ls.tree_path_under_cursor -> hub.pyls_pop.utils
        hub.pyls_pop.utils.|tree_pa|th_under_cursor -> *
        hu|b.pyls_pop.utils.tree_path_under_cursor -> None
    """
    lines = document.lines
    if position["line"] >= len(lines):
        return ""

    line = lines[position["line"]]
    i = position["character"]

    start = line[:i]
    end = line[i:]

    m_start = RE_START_TREE_PATH.findall(start)
    m_end = RE_END_TREE_PATH.findall(end)

    path = m_start[0] + m_end[-1]
    if "hub" not in path:
        return None

    tree = hub.pyls_pop.cache.get()
    tree_path = path.replace("hub.", "")
    tree_path_parts = tree_path.split(".")
    if tree_path in tree or hub.pyls_pop.utils.tree_property_value(
        tree, tree_path_parts[-1]
    ):
        return tree_path

    word = document.word_at_position(position)
    parent_path_parts = tree_path_parts[:-1] + [word] if tree_path_parts else [word]
    parent_path = ".".join(parent_path_parts)

    if not parent_path or parent_path in tree:
        return "*"

    return None


def tree_values(
    hub,
    tree_path: str,
    fuzzy: bool = False,
) -> List[Dict[str, Any]]:
    """
    Return the pop-tree value from the pyls_pop cache.

    :param tree_path: the pop-tree cache key
    :param fuzzy: fuzzily match pop-tree cache keys (default False)
    :returns: the pop-tree cache value
    :examples:
        >>> tree_values(tree_path='pylsp_pop.utils')
        [{"ref": "pyls_pop.utils", "functions": {"tree_values": ...}}]

        >>> tree_values(tree_path=None)
        []

        >>> tree_values(tree_path='*', fuzzy=False)
        []

        >>> tree_values(tree_path='*', fuzzy=True)
        [{...}, {...}, {...}, ...]
    """
    if not tree_path or not fuzzy and tree_path == "*":
        return []

    tree = hub.pyls_pop.cache.get()

    if fuzzy:
        return [
            tree[x] for x in tree if tree_path == "*" or tree_path.lower() in x.lower()
        ]

    return [tree[x] for x in tree if tree_path == x]


def tree_values_from_document_position(
    hub, document: Document, position: Dict[str, int]
) -> List[Dict[str, Any]]:
    """
    Return the pop-tree value given a pylsp document and position.

    :param document: the pop-tree cache key
    :param position: {"line": int, "character": int}
    :returns: the pop-tree cache value
    """
    tree = hub.pyls_pop.cache.get()
    word = document.word_at_position(position)
    tree_values = []

    for tree_ref in [tree[x] for x in tree]:
        if "attributes" in tree_ref and "file" in tree_ref:
            tree_value = hub.pyls_pop.utils.tree_property_value(tree_ref, word)
            if tree_value:
                tree_values.append({**tree_value})

    return tree_values


def tree_property_value(hub, tree_ref, property: str) -> Optional[Any]:
    """
    Return the pop-tree class, function, parameter or variable value
    given a tree ref and a property string in that tree ref.

    :param tree_ref: the pop-tree value
    :param property: the property name
    :returns: the nested pop-tree value
    :examples: (using the tree_ref {"a": {"classes": {"b": "c"}}})
        >>> tree_property_value(tree_ref, "b")
        "c"

        >>> tree_property_value(tree_ref, "d")
        None
    """
    if "classes" in tree_ref and property in tree_ref["classes"]:
        return tree_ref["classes"][property]
    elif "functions" in tree_ref and property in tree_ref["functions"]:
        return tree_ref["functions"][property]
    elif "variables" in tree_ref and property in tree_ref["variables"]:
        return tree_ref["parameters"][property]
    elif "parameters" in tree_ref and property in tree_ref["parameters"]:
        return tree_ref["variables"][property]

    return None


def tree_ref_to_lsp_completion(
    hub,
    tree_ref,
    map_type: str = "completion",
) -> Dict[str, Any]:
    """
    Return the pylsp completion object given a pop-tree value.
    The pop-tree value will be parsed for "documentation",
    "label", and "kind" values. The "label" will include the function
    signature when applicable.

    :param tree_ref: the pop-tree value
    :param map_type: the map type used for mapping the tree_ref (default "completion")
        allowed values: "completion" or "symbol"
    :returns: a dictionary representing the pylsp completion object
        {"label": str, "documentation": str, "kind": int}
    """
    kind = None
    if "type" in tree_ref:
        tree_type = tree_ref["type"]
        tree_type_map = {"bool": "boolean"}
        kind = tree_type_map[tree_type] if tree_type in tree_type_map else tree_type
    elif (
        "return_annotation" in tree_ref
        or "parameters" in tree_ref
        and tree_ref["parameters"]
    ):
        kind = "function"
    elif "file" in tree_ref:
        kind = "file"

    Kind = CompletionItemKind
    _KIND_MAP = _TYPE_MAP

    if map_type == "symbol":
        Kind = SymbolKind
        _KIND_MAP = _SYMBOL_KIND_MAP

    if kind in _KIND_MAP:
        kind = _KIND_MAP[kind]

    sig = tree_ref["ref"]
    if kind is Kind.Function:
        first = False
        for param in tree_ref["parameters"].keys():
            if not first:
                sig = f"{sig}({param}"
                first = True
            else:
                sig = f"{sig}, {param}"

            if "default" in tree_ref["parameters"][param]:
                default_value = tree_ref["parameters"][param]["default"]
                sig = f"{sig}={default_value}"

        sig = f"{sig})"

    return {
        "label": sig,
        "documentation": tree_ref["doc"] if "doc" in tree_ref else "",
        "kind": kind,
    }


def tree_ref_to_lsp_location(hub, tree_ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return the pylsp location object given a pop-tree value.

    :param tree_ref: the pop-tree value
    :returns: a dictionary representing the pylsp location object
        {
            "uri": str,
            "range": {
                "start": {"line": int, "character": int}
                "end": {"line": int, "character": int}
            }
        }
    """
    start_line_no = (
        tree_ref["start_line_number"] - 1 if "start_line_number" in tree_ref else 0
    )
    start = {"line": start_line_no, "character": 0}
    end_line_no = (
        tree_ref["end_line_number"] - 1 if "end_line_number" in tree_ref else 0
    )
    end = {"line": end_line_no, "character": 0}
    uri = hub.pyls_pop.utils.to_uri(tree_ref["file"])
    location = {"uri": uri, "range": {"start": start, "end": end}}

    return location


def to_lsp_location(
    hub, tree_path: str, uri: str, line_no: int, line: str
) -> Dict[str, Any]:
    """
    Return the pylsp location object.

    :param tree_path: the pop-tree value
    :param uri: the pop-tree value
    :param line_no: the line number for a line in its source code
    :param line: the raw text for the line
    :returns: a dictionary representing the pylsp location object
        {
            "uri": str,
            "range": {
                "start": {"line": int, "character": int}
                "end": {"line": int, "character": int}
            }
        }
    """
    word = tree_path.split(".")[-1]
    character = line.index(word)
    start = {"line": line_no, "character": character}
    end = {"line": line_no, "character": character + len(word)}
    location = {"uri": uri, "range": {"start": start, "end": end}}

    return location


def to_uri(hub, path) -> str:
    """
    Return the uri for a file path.

    :param path: the absolute file path
    :returns: the file uri
    :examples:
        >>> to_uri('/Users/salt/project/file.py')
        "file:///Users/salt/project/file.py"
    """
    return f"file://{path}"
