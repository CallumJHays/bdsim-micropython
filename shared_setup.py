"""
This package provides a SSOT for setup information for all subpackages.
It is shared with all subpackages as symlinks.
"""

import setuptools
from pathlib import Path


def setup_pkg(name, packages, description, long_description, install_requires):
    here = Path(__file__).parent.absolute()

    setuptools.setup(
        name=name,
        packages=packages,
        description=description,
        long_description=long_description,
        install_requires=install_requires,

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
