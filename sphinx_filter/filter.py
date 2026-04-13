""" filter extension for sphinx with the goal to filter a document for different viewers. """

from __future__ import annotations

from docutils import nodes

from sphinx.application import Sphinx

from sphinx.util.docutils import SphinxDirective

from sphinx.util.typing import ExtensionMetadata

from sphinx.environment.collectors.toctree import TocTreeCollector

class FilterRole(): #pylint: disable=too-few-public-methods

    """ A role to filter sphinx documents for different viewers. """



class filterIncludeHeadingOnlyDirective(SphinxDirective): #pylint: disable=invalid-name

    """ A directive to include only the heading of a section in documentation. """

    required_arguments = 1
    optional_arguments = 100

    def run(self) -> list[nodes.Node]:

        filter_tags = self.env.app.builder.filter_builder.filter_tags

        if [i for i in self.arguments if i in filter_tags]:
            self.state_machine.node.remove_content = True
            self.state_machine.node.is_included = True
        return []

class filterIncludeDirective(SphinxDirective): #pylint: disable=invalid-name

    """ A directive to include chapters or sections in the documentation. """

    required_arguments = 1
    optional_arguments = 100

    def run(self) -> list[nodes.Node]:

        filter_tags = self.env.app.builder.filter_builder.filter_tags

        if [i for i in self.arguments if i in filter_tags]:
            self.state_machine.node.is_included = True
        return []

class filterExcludeDirectContentOnlyDirective(SphinxDirective): #pylint: disable=invalid-name

    """ A directive that excludes content that belongs directly
        to the section from the documentation. """

    required_arguments = 1
    optional_arguments = 100

    def run(self) -> list[nodes.Node]:

        filter_tags = self.env.app.builder.filter_builder.filter_tags

        if [i for i in self.arguments if i in filter_tags]:
            self.state_machine.node.remove_content = True
        return []

class filterExcludeDirective(SphinxDirective): #pylint: disable=invalid-name

    """ A directive to exclude chapters or sections from the documentation. """

    required_arguments = 1
    optional_arguments = 100

    def run(self) -> list[nodes.Node]:

        filter_tags = self.env.app.builder.filter_builder.filter_tags

        if [i for i in self.arguments if i in filter_tags]:
            self.state_machine.node.remove_section = True
        return []

class filterRenameHeadingDirective(SphinxDirective): #pylint: disable=invalid-name

    """ A directive to exclude chapters or sections from the documentation."""

    required_arguments = 1
    optional_arguments = 100
    has_content = True

    def run(self) -> list[nodes.Node]:

        filter_tags = self.env.app.builder.filter_builder.filter_tags

        if [i for i in self.arguments if i in filter_tags]:
            self.state_machine.node.children[0].clear()
            self.state_machine.node.children[0] += nodes.Text(self.block_text)
        return []

class filterValidTags(SphinxDirective): #pylint: disable=invalid-name

    """ A directive to check if a valid tag is used and prevent typos in the filter tags. """

    required_arguments = 1
    optional_arguments = 100

    def run(self) -> list[nodes.Node]:

        filter_tags = self.env.app.builder.filter_builder.filter_tags

        if not [i for i in self.arguments if i in filter_tags]:
            raise ValueError('sphinx_filter: tag used that is not in the valid tag list')
        return []

class FilterBuilder(): #pylint: disable=too-few-public-methods

    """ Builder class for the filter extension. """

    def __init__(self, builder):
        self.filter_tags = builder.config.filter_tags
        if builder.config.filter_mode in ['include', 'exclude']:
            self.filter_mode = builder.config.filter_mode
        else:
            raise ValueError('sphinx_filter: invalid filter_mode')

def _on_builder_inited(app):
    app.builder.filter_builder = FilterBuilder(app.builder)

def inherit_filter_flags(node: nodes.Node, filter_mode: str):

    """ function to inherit the filterflags from the parent node. """

    node.parentIsSet = False
    if getattr(node, 'parent', False):
        node.parentIsSet = getattr(node.parent, 'is_included', False) or \
                            getattr(node.parent, 'remove_section', False) or \
                            getattr(node.parent, 'parentIsSet', False)

    no_filter_flag = not getattr(node, 'is_included', False) and \
                      not getattr(node, 'remove_section', False) and \
                      not getattr(node, 'remove_content', False) and \
                      not node.parentIsSet

    if no_filter_flag:
        if filter_mode == 'include':
            node.remove_section = True
        if filter_mode == 'exclude':
            node.is_included = True

    if getattr(node, 'parent', False):
        if not getattr(node, 'is_included', False) and not getattr(node, 'remove_section', False):
            if filter_mode == 'include':

                section_is_included = getattr(node.parent, 'is_included', False) or \
                                      getattr(node.parent, 'remove_content', False)

                if section_is_included:
                    node.is_included = True
            elif filter_mode == 'exclude':
                if getattr(node.parent, 'remove_section', False):
                    node.remove_section = True


def remove_section(node: nodes.Node, filter_mode: str) -> bool:

    """ tells if a section is marked to be removed. """

    return getattr(node, 'remove_section', False) or filter_mode == 'include'

def get_filtered_tree(node: nodes.Node, filter_mode: str) -> list[nodes.Node]:

    """ function that filters the doctree. """

    inherit_filter_flags(node, filter_mode)

    nr_elements = len(node.children[:])
    idx = 0
    while idx < nr_elements:
        child = node.children[idx]

        child_removable = not isinstance(child, nodes.section) and \
                              not getattr(child, 'is_included', False)

        child_removable_content = getattr(node, 'remove_content', False) and \
                                  not isinstance(child, nodes.title)

        child_should_be_removed = getattr(node, 'remove_section', False) or \
                                  child_removable_content

        if child_removable and child_should_be_removed:
            del node.children[idx]
            idx -= 1

        if isinstance(child, nodes.section):
            returned_children = get_filtered_tree(child, filter_mode)
            if (returned_children is None) or (len(returned_children) == 0):
                del node.children[idx]
                idx -= 1
            else:
                old_len = len(node.children)
                node.children = node.children[:idx] + returned_children + node.children[idx+1:]
                idx += len(node.children) - old_len

        idx += 1
        nr_elements = len(node.children)

    nr_elements = len(node.children)
    idx = 0
    while idx < nr_elements:
        child = node.children[idx]

        parent_not_included = not getattr(node, 'is_included', False)

        child_removable = isinstance(child, nodes.section) or \
                          (not isinstance(child, nodes.section) and parent_not_included)

        child_should_be_removed = remove_section(child, filter_mode) and \
                                  not getattr(child, 'is_included', False)

        if child_removable and child_should_be_removed:
            del node.children[idx]
            idx -= 1
        idx += 1
        nr_elements = len(node.children)

    has_included_children = any(getattr(child, 'is_included', False) for child in node.children)
    included_children_removed_section = has_included_children and remove_section(node, filter_mode)

    if  included_children_removed_section and not getattr(node, 'is_included', False):
        return node.children

    if len(node.children) == 0:
        return None

    return [node]

def process_doctree(app, doctree):

    """ processes the doctree. """

    filter_mode     = app.builder.filter_builder.filter_mode
    get_filtered_tree(doctree, filter_mode)
    TocTreeCollector().process_doc(app, doctree)

def setup(app: Sphinx) -> ExtensionMetadata:

    """ setup function for the sphinx_filter extension. """

    app.add_role('filter', FilterRole())
    app.add_directive('filter-exclude', filterExcludeDirective)
    app.add_directive('filter-exclude-content-only', filterExcludeDirectContentOnlyDirective)
    app.add_directive('filter-include', filterIncludeDirective)
    app.add_directive('filter-include-heading-only', filterIncludeHeadingOnlyDirective)
    app.add_directive('filter-rename-heading', filterRenameHeadingDirective)
    app.add_directive('filter-valid-tags', filterValidTags)
    app.add_config_value('filter_tags', ['excluded'], 'env')
    app.add_config_value('filter_mode', 'exclude', 'env')
    app.connect('builder-inited', _on_builder_inited)
    app.connect('doctree-read', process_doctree)

    return {

        'version': '0.1',

        'parallel_read_safe': False,

        'parallel_write_safe': False,

    }
