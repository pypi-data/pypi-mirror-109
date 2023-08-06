import logging
import os
from typing import Dict

from pylsp import plugins
from pylsp.config.config import Config
from pylsp.workspace import Document, Workspace

log = logging.getLogger(__name__)


def completions(
    hub,
    config: Config,
    workspace: Workspace,
    document: Document,
    position: Dict[str, int],
):
    """Return the hub.* completions for the project."""
    tree_path = hub.pyls_pop.utils.tree_path_under_cursor(document, position)
    tree_values = hub.pyls_pop.utils.tree_values(tree_path, fuzzy=True)
    completions = [
        hub.pyls_pop.utils.tree_ref_to_lsp_completion(x) for x in tree_values
    ]

    return completions


def signature_help(
    hub,
    config: Config,
    workspace: Workspace,
    document: Document,
    position: Dict[str, int],
):
    """Return the hub.* signature help for when requesting signature help
    for a hub namespace.
    """
    tree_path = hub.pyls_pop.utils.tree_path_under_cursor(document, position)
    if tree_path:
        tree_values = hub.pyls_pop.utils.tree_values(tree_path)
        completions = [
            hub.pyls_pop.utils.tree_ref_to_lsp_completion(x) for x in tree_values
        ]

        if completions:
            return {"signatures": completions, "activeSignature": 0}


def document_highlight(
    hub,
    config: Config,
    workspace: Workspace,
    document: Document,
    position: Dict[str, int],
):
    """Return the hub.* highlights for pylsp for the current document."""
    tree_path = hub.pyls_pop.utils.tree_path_under_cursor(document, position)
    if tree_path:
        highlights = []

        for line_no, line in [
            (i, x)
            for i, x in enumerate(document.lines)
            if tree_path in x and i != position["line"]
        ]:
            location = hub.pyls_pop.utils.to_lsp_location(
                tree_path, document.uri, line_no, line
            )
            highlights.append(location)

        return highlights


def hover(
    hub,
    config: Config,
    workspace: Workspace,
    document: Document,
    position: Dict[str, int],
):
    """Return any hub.* docs when hovering over a hub namespace."""
    contents = plugins.hover.pylsp_hover(document, position)
    if "contents" in contents and contents["contents"]:
        contents = contents["contents"]
    else:
        contents = []

    tree_path = hub.pyls_pop.utils.tree_path_under_cursor(document, position)
    tree_values = hub.pyls_pop.utils.tree_values(tree_path)

    for tree_ref in tree_values:
        lsp_completion = hub.pyls_pop.utils.tree_ref_to_lsp_completion(tree_ref)
        lsp_hover = "{}\n{}".format(
            lsp_completion["label"], lsp_completion["documentation"]
        )

        contents.append({"language": "python", "value": lsp_hover})

    return {"contents": contents if contents else ""}


def references(
    hub,
    config: Config,
    workspace: Workspace,
    document: Document,
    position: Dict[str, int],
    exclude_declaration=False,
):
    """Return all hub.* references for the project when requesting a reference
    for a hub namespace.
    """
    tree_path = hub.pyls_pop.utils.tree_path_under_cursor(document, position)
    tree_values = hub.pyls_pop.utils.tree_values(tree_path)

    if not tree_values:
        tree_values = hub.pyls_pop.utils.tree_values_from_document_position(
            document, position
        )
        if tree_values:
            tree_path = tree_values[0]["ref"]
        else:
            return []

    references = []
    for root, dirs, files in os.walk(workspace.root_path):
        for file_name in [x for x in files if x.endswith(".py")]:
            path = os.path.join(root, file_name)
            with open(path, encoding="utf-8") as f:
                for line_no, line in [
                    (i, x)
                    for i, x in enumerate(f)
                    if tree_path in x
                    and not (path == document.path and i == position["line"])
                ]:
                    location = hub.pyls_pop.utils.to_lsp_location(
                        tree_path, hub.pyls_pop.utils.to_uri(path), line_no, line
                    )
                    references.append(location)

    definitions = [
        hub.pyls_pop.utils.tree_ref_to_lsp_location(x)
        for x in tree_values
        if x["file"] != document.path and x["start_line_number"] != position["line"]
    ]

    return references + definitions


def document_symbols(hub, config: Config, workspace: Workspace, document: Document):
    """Return all hub.* symbols for the project."""
    symbols = []
    for line_no, line in [(i, x) for i, x in enumerate(document.lines) if "hub." in x]:
        for tree_path in hub.pyls_pop.utils.RE_TREE_PATH.findall(line):
            tree_values = hub.pyls_pop.utils.tree_values(tree_path)
            location = hub.pyls_pop.utils.to_lsp_location(
                tree_path, document.uri, line_no, line
            )

            for tree_ref in tree_values:
                lsp_completion = hub.pyls_pop.utils.tree_ref_to_lsp_completion(
                    tree_ref, map_type="symbol"
                )

                symbols.append(
                    {
                        "name": lsp_completion["label"],
                        "kind": lsp_completion["kind"],
                        "container_name": None,
                        "location": location,
                    }
                )

    return symbols


def definitions(hub, config: Config, document: Document, position: Dict[str, int]):
    """Support "goto declaration" for hub.* namespaces."""
    tree_path = hub.pyls_pop.utils.tree_path_under_cursor(document, position)
    if tree_path:
        tree_values = hub.pyls_pop.utils.tree_values(tree_path)
        definitions = [
            hub.pyls_pop.utils.tree_ref_to_lsp_location(x) for x in tree_values
        ]

        return definitions
