from pybuilder.core import use_plugin, init

use_plugin("python.core")
# the python unittest plugin allows running python's standard library unittests
use_plugin("python.unittest")
# this plugin allows installing project dependencies with pip
use_plugin("python.install_dependencies")
# a linter plugin that runs flake8 (pyflakes + pep8) on our project sources
use_plugin("python.flake8")
# a plugin that measures unit test statement coverage
use_plugin("python.coverage")
# for packaging purposes since we'll build a tarball
use_plugin("python.distutils")

name = "software_engineering"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("coverage_break_build", False)
    project.set_property("verbose", True)
    project.set_property("dir_source_main_python", "src/main/python")
    project.set_property("dir_source_unittest_python", "src/unittest/python")
    project.set_property("unittest_module_glob", "tests.py")
    project.build_depends_on("pytest")
    project.build_depends_on("mock")

@init(environments="unit_test")
def set_properties_for_unit_tests(project):
    project.set_property("verbose", True)