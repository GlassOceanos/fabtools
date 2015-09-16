"""
Update-conf.py files management
===============================

This module provides tools for generating configuration files from
'conf.d' like directories.

.. _update-conf.py: https://github.com/rarylson/update-conf.py

"""

import os

from fabric.api import abort, run

from fabtools import python, require
from fabtools.files import is_dir, is_file, move
from fabtools.utils import run_as_root


def is_installed():
    """
    Check if `update-conf.py`_ is installed.
    """
    return python.is_installed('update-conf.py')


def generate_file(config_file, snippets_dir=None, use_sudo=False, owner='', group='', mode=''):
    """
    Generate a configuration file from a 'conf.d' snippets directory.
    """
    require.python.package('update-conf.py')

    if snippets_dir is None:
        snippets_dir = '%s.d' % config_file

    if not is_dir(snippets_dir, use_sudo):
        abort('Snippets directory "%s" does not exist' % snippets_dir)

    command = 'update-conf.py -f %s -d %s' % (config_file, snippets_dir)

    if use_sudo:
        run_as_root(command, pty=False)
    else:
        run(command, pty=False)

    require.file(config_file, use_sudo=use_sudo, owner=owner, group=group, mode=mode)


def create_snippets_dir(config_file, snippets_dir=None, move_file=True, use_sudo=False,
                        owner='', group='', mode=''):
    """
    Create a 'conf.d' snippets directory suitable to be used with update-conf.py,
    optionally moving the original configuration file into the new snippets directory.
    """
    require.python.package('update-conf.py')

    if snippets_dir is None:
        snippets_dir = '%s.d' % config_file

    if not is_dir(snippets_dir):
        require.directory(snippets_dir, use_sudo, owner, group, mode)

        if is_file(config_file, use_sudo) and move_file:
            base_file = os.path.join(snippets_dir,
                                     '%s.orig' % os.path.basename(config_file))
            move(config_file, base_file, use_sudo=use_sudo)
