# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2005-2019, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

'''
Mock package defining a global variable of the same name as a mock submodule of
this package.

This package is exercised by the `test_import_submodule_global_shadowed`
functional test.
'''


submodule = 'That is not dead which can eternal lie.'
'''
Global variable of the same name as a mock submodule of this package.

This variable's value is arbitrary. This variable's type, however, is asserted
to be `str` by this test.
'''
