"""
This package provides a SSOT for setup information for all subpackages.
"""

import setuptools
from pathlib import Path

VERSION = '0.8'


def setup_pkg(name, packages, description, install_requires, extras_require={}):

    setuptools.setup(
        name=name,
        packages=packages,
        description=description,
        install_requires=[
            (pkg + '==' + VERSION) if (pkg.startswith('bdsim.') and '=' not in pkg)
            else pkg for pkg in install_requires],
        extras_require=extras_require,

        version=VERSION,

        # This is a one-line description or tagline of what your project does. This
        # corresponds to the "Summary" metadata field:
        long_description_content_type='text/markdown',
        # each subpkg should have its own README.md that becomes the long_description
        long_description=(Path(__file__).parent.absolute() / \
                          'README.md').open().read(),

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
        python_requires='>=3.6',
    )
