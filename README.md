# Sphinx Filter Extension

This is an extension to filter the content of a Sphinx documentation to generate documentation for different audiences from the same source files. The directives work on the section in which they are placed. For example, you can exclude a section while including a subsection. Please see **test/test_source** and **test/test_passed** for examples.

## The modes are

- **exclude**
  Default: everything is included in the document; you have to exclude content that you don't want to publish with directives.

- **include**
  Default: nothing in your document will be included in the output document unless you include it.

## The directives are

- **filter-exclude**
  Exclude the section in which the directive is placed.

- **filter-exclude-content-only**
  Exclude only the paragraphs, etc., that belong to this section; keep the heading of the section and keep its subsections.

- **filter-include**
  Include the section in which the directive is placed.

- **filter-include-heading-only**
  Only include the heading of the section and include its subsections, but don't include content that directly belongs to the section.

- **filter-valid-tags**
  If you place this directive in the document (it makes sense to do that at the beginning to make other editors aware of it), tags that are not in the argument list of this directive will throw an exception.
