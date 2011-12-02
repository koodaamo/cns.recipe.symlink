# -*- coding: utf-8 -*-
"""Recipe symlink"""

import logging
import os
import sys
import fnmatch
import itertools

class Recipe:
    def __init__(self, buildout, name, options):
        self.options = options
        self.logger = logging.getLogger(name)


    def install(self):
        "implement recipe API"
        if sys.platform.startswith('win'):
            raise RuntimeError('Symlinks are not supported on Windows.')
        source = self.options.get('symlink')
        symlink_base= self.options.get('symlink_base')
        starget = self.options.get('symlink_target')
        ignored = self.options.get('ignore')

        if symlink_base is not None:
            symlink_base = os.path.expanduser(symlink_base)
        if starget is not None:
            starget = os.path.expanduser(starget)

        # just base and target are given
        if source is None and (symlink_base and starget):
            items = os.listdir(symlink_base)

        elif source is not None:
            items = source.split('\n')
        else:
            err = "Please provide a symlink or both symlink_base & symlink_target"
            raise RuntimeError(err)

        check = lambda fname: True
        if ignored:
            ignores = ignored.split("\n")
            # check whether an item should be ignored
            check = lambda fname: True not in [fnmatch.fnmatch(fname, expr) for expr in ignores]
       
        result = []

        for item in itertools.ifilter(check, items):
            if item:
                # item is : source=target
                parts = item.split('=')
                if len(parts) == 1:
                    source = parts[0].strip()
                    target = starget # global target
                else:
                    source = parts[0].strip()
                    target = parts[1].strip()
                    if not target:
                        # for example: SRCPROJ=
                        target = starget
                # expand ~ variable
                source = os.path.expanduser(source)
                # check if apply symlink base to this entry
                if symlink_base and (os.path.abspath(source) != source):
                    source = os.path.join(symlink_base, source)
                    if os.path.isdir(target):
                        # take last part of source and append it to target
                        target = os.path.join(target, os.path.split(source)[-1])
                if os.path.isfile(target) or os.path.islink(target) :
                    self.logger.debug('Symlink target %s already exists' % target)
                    result.append(target)
                elif not os.path.exists(source):
                    self.logger.warning('Symlink source not found! %s' % source)
                else:
                    os.symlink(source, target)
                    result.append(target)

        return result


    def update(self):
       "Implement recipe API. Just call install for lack of better job."
       return self.install()
