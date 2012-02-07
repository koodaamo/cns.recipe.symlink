# -*- coding: utf-8 -*-
"""
Doctest runner for 'cns.recipe.symlink'.
"""
__docformat__ = 'restructuredtext'

import os, unittest, doctest
import zc.buildout.tests
import zc.buildout.testing
import interlude

from zope.testing import renormalizing

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('cns.recipe.symlink', test)
    # Install any other recipes that should be available in the tests

def test_suite():
    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                'README.txt',
                setUp=setUp,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                globs = dict(interact=interlude.interact),
                checker=renormalizing.RENormalizing([
                        zc.buildout.testing.normalize_path,
                        zc.buildout.testing.normalize_endings,
                        zc.buildout.tests.hide_distribute_additions,
                        zc.buildout.tests.hide_zip_safe_message,
                ]),
            ),
        ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
