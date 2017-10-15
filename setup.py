#!/usr/bin/env python

import setuptools


setuptools.setup(
    setup_requires=['pbr'],
    pbr=True,
    entry_points={
        'sphinx.builders': [
            'odt = sphinxcontrib.odfbuilder',
        ],
    }
)
