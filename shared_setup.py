"""
This package provides a SSOT for setup information for all subpackages.
It is shared with all subpackages as symlinks.
"""

import setuptools
from platform import python_version
import os
from subprocess import call, check_call, check_output
from pathlib import Path
from shutil import rmtree


class Py34CompatabilityTranspiler:

    def __init__(self):
        # mypy stubgen still requires py >3.5 to run, so lets scan for any available versions on
        # PATH, ensure mypy is installed for that dist, and run it:
        self.python3x = os.getenv("BDSIM_SETUP_PY")
        if self.python3x is None:
            for minor_version in range(5, 12):
                self.python3x = "python3." + str(minor_version)

                try:
                    if call((self.python3x + ' --version').split()) == 0:
                        break
                except FileNotFoundError:  # the version of python doesn't exist
                    pass

            else:
                raise Exception(
                    "A python version >= 3.5 was not found on PATH. "
                    "This is required for bdsim package generation. "
                    "To supply a python version not on PATH, set envar BDSIM_SETUP_PY=[path/to/python3.>5]")

        # ensure mypy and strip-hints are installed
        check_call((self.python3x + ' -m pip install mypy strip-hints').split())

    def transpile(self, input, output):
        """
        input: the input file or module directory path
        output: the output file or output package path (parent of output module directory)
        """

        print('called transpile', input, output)
        print(Path(input), Path(output))

        # produce pyi files for each file in the module
        # call stubgen with the specific python version (a little hacky but it works)
        check_call([self.python3x, '-c', """import sys
from mypy.stubgen import main
sys.argv = ["stubgen", "%s", "-o", "%s"]
main()""" % (str(input), str(output))])

        # produce type-stripped files for each file in the module
        print(check_output([self.python3x, '-c', """from pathlib import Path;
from strip_hints import strip_file_to_string
src, out = Path("%s"), Path("%s")
print('SRC, OUT', src, out)
if src.is_dir():
    for infile in src.glob("**/*.py"):
        outfile = out / str(infile.parent) / (infile.stem + '.py')
        outfile.open('w').write(strip_file_to_string(str(infile)))
else:
    out.open('w').write(strip_file_to_string(str(src)))""" % (str(input), str(output))]).decode())


def setup_pkg(name, packages, description, long_description, here: Path, install_requires):

    src_relpath = 'bdsim'
    pkg_relpath = '.'  # might change in next 'if'

    if python_version() < '3.5':  # wow - this version no string comparison works perfectly!

        pkg_relpath = '.py3.4-pkg'

        # if we're below 3.5 we need to separate type hints from the code - into .pyi and .py
        # files respectively. We should also remove any imports from `typing` or `typing_extensions`.
        # all uses of any imports from these libraries should be stripped out anyway.
        pkg_dir = here / pkg_relpath
        if pkg_dir.exists():
            rmtree(str(pkg_dir))
        pkg_dir.mkdir()

        # transpile to <py35-compatible code and store in pkg_dir
        Py34CompatabilityTranspiler().transpile(src_relpath, pkg_dir)

    setuptools.setup(
        name=name,
        packages=packages,
        description=description,
        long_description=long_description,
        install_requires=install_requires,
        package_dir={"": pkg_relpath},

        version='0.8',

        # This is a one-line description or tagline of what your project does. This
        # corresponds to the "Summary" metadata field:
        long_description_content_type='text/markdown',

        classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support _here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3 :: Only'],

        project_urls={
            # 'Documentation': 'https://petercorke.github.io/bdsim',
            'Source': 'https://github.com/petercorke/bdsim',
            'Tracker': 'https://github.com/petercorke/bdsim/issues',
            # 'Coverage': 'https://codecov.io/gh/petercorke/spatialmath-python',
        },

        url='https://github.com/petercorke/bdsim',
        author='Peter Corke',
        author_email='rvc@petercorke.com',  # TODO
        keywords='python micropython block-diagram dynamic simulation realtime control-theory robot remote',
        license='MIT',  # TODO
        python_requires='>=3.4',
    )
