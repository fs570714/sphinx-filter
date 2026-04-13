# Markdown Test File

```{filter-valid-tags} test-exclude-mode1 test-exclude-mode2 test-exclude-mode3 test-exclude-mode4 test-include-mode1 test-include-mode2 test-include-mode3 test-include-mode4 test-exclude-mode5-rename-heading
```

## in this section we test the exclude mode

```{filter-exclude} test-exclude-mode1 test-exclude-mode3 test-exclude-mode4
```

this description of the section should be excluded

### confidental subsection we want to exclude

```{filter-exclude-content-only} test-exclude-mode2
```

```{filter-rename-heading} test-exclude-mode5-rename-heading
confidental subsection we want to rename
```

we want to remove this subsection

#### this is a subsection we want still to include even if the parent section is excluded

```{filter-include} test-exclude-mode3
```

this is information should be included

### this subsection is to be removed by its parent

this is content that should be removed

### this section should only contain its heading and subsections

```{filter-include-heading-only} test-exclude-mode4
```

this content should be removed

### just a subsection to remove

just subsection content to be removed

## in this section we test the include mode

```{filter-include} test-include-mode1 test-include-mode3 test-include-mode4
```

this description of the section is should be included

### section where we just want to exclude the heading

```{filter-include-heading-only} test-include-mode2
```

we want to direct content of this section

#### this is a subsection we want still to exclude even if the parent section is included

```{filter-exclude} test-include-mode3
```

```{filter-include} test-include-mode2
```

this is information should be included

### this subsection is to be removed by its parent (include mode)

this is content that should be removed

### this section should only contain its heading and subsections (include mode)

```{filter-exclude-content-only} test-include-mode4
```

section content to be removed

### just a subsection to remove (include mode)

just subsection content to be removed
