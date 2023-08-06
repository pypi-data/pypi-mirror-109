import pop.hub
import pylsp


@pylsp.hookimpl
def pylsp_settings(config):
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="pyls_pop")
    # Populate hub.OPT fconfig file
    hub.pop.config.load(["pyls_pop", "pop_tree"], cli="pyls_pop", parse_cli=False)
    return {"plugins": {"pyls_pop": {"hub": hub}}}


@pylsp.hookimpl
def pylsp_initialize(config):
    hub = config.plugin_settings("pyls_pop")["hub"]
    hub.pop.loop.start(hub.pyls_pop.cache.create())


@pylsp.hookimpl
def pylsp_completions(config, workspace, document, position):
    hub = config.plugin_settings("pyls_pop")["hub"]
    return hub.pyls_pop.plugin.completions(config, workspace, document, position)


@pylsp.hookimpl
def pylsp_signature_help(config, workspace, document, position):
    hub = config.plugin_settings("pyls_pop")["hub"]
    return hub.pyls_pop.plugin.signature_help(config, workspace, document, position)


@pylsp.hookimpl
def pylsp_document_highlight(config, workspace, document, position):
    hub = config.plugin_settings("pyls_pop")["hub"]
    return hub.pyls_pop.plugin.document_highlight(config, workspace, document, position)


@pylsp.hookimpl
def pylsp_hover(config, workspace, document, position):
    hub = config.plugin_settings("pyls_pop")["hub"]
    return hub.pyls_pop.plugin.hover(config, workspace, document, position)


@pylsp.hookimpl
def pylsp_references(
    config,
    workspace,
    document,
    position,
    exclude_declaration,
):
    hub = config.plugin_settings("pyls_pop")["hub"]
    return hub.pyls_pop.plugin.references(
        config, workspace, document, position, exclude_declaration
    )


@pylsp.hookimpl
def pylsp_document_symbols(config, workspace, document):
    hub = config.plugin_settings("pyls_pop")["hub"]
    return hub.pyls_pop.plugin.document_symbols(config, workspace, document)


@pylsp.hookimpl
def pylsp_definitions(config, document, position):
    hub = config.plugin_settings("pyls_pop")["hub"]
    return hub.pyls_pop.plugin.definitions(config, document, position)
