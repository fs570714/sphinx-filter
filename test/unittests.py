""" Module providing the unittest for sphinx_filter. """

import os

import unittest
import subprocess

test_source_path = os.path.dirname(__file__) + "/" + "test_source/"
test_build_path  = os.path.dirname(__file__) + "/" + "test_build/"
test_passed_path = os.path.dirname(__file__) + "/" + "test_passed/"
TEST_OUTPUT_FILE = "index.md"

class SphinxFilterUnittest(unittest.TestCase):

    """ class providing the unittest for sphinx_filter. """

    def run_build(self, test_name, test_output_folder, mode):

        """ function build the unittest output and to check the build process """

        cmd = [
            "sphinx-build", "-M", "markdown", test_source_path, test_output_folder,
            "-E", f"-Dfilter_tags={test_name}", f"-Dfilter_mode={mode}"
        ]

        result = subprocess.run(cmd, check=False, capture_output=True)
        self.assertEqual(result.returncode, 0)

    def run_compare(self, test_name, test_output_folder, mode):

        """ function that compares the build output with the passed file """

        test_markdown_folder = f"{test_output_folder}/markdown/"

        with open(test_markdown_folder + TEST_OUTPUT_FILE, "r", encoding="utf-8") as test_output:

            test_output_lines = test_output.readlines()

            test_passed_folder = f"test-{mode}-mode/"
            test_passed_file = f"{test_name}.md"
            test_passed_output = test_passed_path + test_passed_folder + test_passed_file

            with open(test_passed_output, "r", encoding="utf-8") as test_passed:

                test_passed_lines = test_passed.readlines()
                self.assertEqual(len(test_passed_lines), len(test_output_lines))

                for test_output_line, test_passed_line in zip(test_output_lines, test_passed_lines):
                    self.assertEqual(test_output_line, test_passed_line)

    def run_sphinx_test(self, mode, nr, extra_name=""):

        """ function to generate the unittest for the in- and exclude directives """

        test_name = f"test-{mode}-mode{nr}{extra_name}"
        test_output_folder = test_build_path + test_name

        self.run_build(test_name, test_output_folder, mode)
        self.run_compare(test_name, test_output_folder, mode)

    def test_exclude_mode1(self):

        """ unittest that tests the filter-exclude directive in filter-mode exclude. """

        self.run_sphinx_test("exclude", 1)


    def test_exclude_mode2(self):

        """ unittest that tests the filter-exclude-content-only directive in
            filter-mode exclude. """

        self.run_sphinx_test("exclude", 2)

    def test_exclude_mode3(self):

        """ unittest that tests the filter-exclude directive in filter-mode
            exclude with a filter-include directive in a subsection. """

        self.run_sphinx_test("exclude", 3)

    def test_exclude_mode4(self):

        """ unittest that tests the filter-exclude directive in filter-mode
            exclude with a filter-include-heading-only directive in a subsection. """

        self.run_sphinx_test("exclude", 4)

    def test_include_mode1(self):

        """ unittest that tests the filter-include directive in filter-mode
            include. """

        self.run_sphinx_test("include", 1)

    def test_include_mode2(self):

        """ unittest that tests the filter-include-heading-only directive in filter-mode
            include. """

        self.run_sphinx_test("include", 2)

    def test_include_mode3(self):

        """ unittest that tests the filter-include directive in filter-mode
            include with a filter-exclude directive in a subsection. """

        self.run_sphinx_test("include", 3)

    def test_include_mode4(self):

        """ unittest that tests the filter-include directive in filter-mode
            include with a filter-exclude-content-only directive in a subsection. """

        self.run_sphinx_test("include", 4)

    def test_rename_heading(self):

        """ test if the filter-rename-heading directive works as expected. """

        self.run_sphinx_test("exclude", 5, "-rename-heading")

    def test_invalid_filter_mode(self):

        """ test if the correct exception is raised if an invalid filter-mode is choosen. """

        test_mode = "invalid"
        test_nr     = 5
        test_name = "test-" + test_mode + "-mode" + str(test_nr)
        test_output_folder = test_build_path + test_name

        cmd = ["sphinx-build", "-M", "markdown", test_source_path, test_output_folder,\
               "-E", "-Dfilter_tags=" + test_name, "-Dfilter_mode=" + test_mode]

        result = subprocess.run(cmd, check=False, capture_output=True)

        self.assertNotEqual(result.returncode, 0)

        assert_str = 'sphinx_filter: invalid filter_mode'
        self.assertIn(assert_str, str(result.stderr))

    def test_invalid_tags(self):

        """ test if the correct exception is raised if an invalid tag is choosen. """

        test_mode = "exclude"
        test_nr     = 6
        test_name = "test-exclude-tags" + str(test_nr) + "-invalid"
        test_output_folder = test_build_path + test_name

        cmd = ["sphinx-build", "-M", "markdown", test_source_path, test_output_folder,\
               "-E", "-Dfilter_tags=" + test_name, "-Dfilter_mode=" + test_mode]

        result = subprocess.run(cmd, check=False, capture_output=True)

        self.assertNotEqual(result.returncode, 0)

        assert_str = 'sphinx_filter: tag used that is not in the valid tag list'
        self.assertIn(assert_str, str(result.stderr))
