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
        self.buildout = buildout


    def install(self):
        "implement recipe API"

        if sys.platform.startswith('win'):
            raise RuntimeError('Symlinks are not supported on Windows.')


        #shortcuts
        buildout = self.buildout["buildout"]
        options = self.options

        # buildout options
        source = options.get('symlink')
        symlink_base= options.get('symlink_base')
        starget = options.get('symlink_target')
        ignored = options.get('ignore')
        autocreate = options.get('autocreate')
        bulk = options.get("bulk")
        eggs = options.get("eggs")
        develop = options.get("develop")

        # check source base and target
        if symlink_base:
            symlink_base = os.path.expanduser(symlink_base)
            if not os.path.isdir(symlink_base):
               raise RuntimeError("Source directory %s does not exist." % symlink_base)


        bulkitems = []
        if starget:
            starget = os.path.expanduser(starget)
            if not os.path.isdir(starget):
               self.logger.debug("Target dir %s does not exist." % starget)
               if autocreate:
                  os.makedirs(starget)
               else:
                  raise RuntimeError("Target directory %s does not exist." % starget)

            # target is specified, so there might be bulk items

            if eggs:
               eggdir = buildout["eggs-directory"]
               eggnames = os.listdir(eggdir)
               bulkitems += [eggdir + os.sep + n for n in eggnames if n]

            if develop:
               try:
                  srcdirs = buildout["develop"].split("\n")
                  bulkitems += [buildout["directory"] + os.sep + dir for dir in srcdirs if dir]
               except:
                  pass

            if symlink_base and starget and (not source or bulk):
                items = os.listdir(symlink_base)
                bulkitems += [symlink_base + os.sep + item for item in items]

            # remove those that are to be ignored
            lastpart = lambda bi: bi[bi.rfind(os.sep)+1:]

            if ignored:
                ignores = [i for i in ignored.split("\n") if i]
                # check whether an item should be ignored
                check = lambda fpath: True not in [fnmatch.fnmatch(lastpart(fpath), expr) for expr in ignores]
                bulkitems = itertools.ifilter(check, bulkitems)

            bulkitems = [(bi, starget + os.sep + lastpart(bi)) for bi in bulkitems]


        sourceitems = []
        if source:
            items = [item for item in source.split('\n') if item]
            for item in items:
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

                sourceitems.append((source, target))


        elif not starget and (symlink_base or eggs or develop):
            raise RuntimeError("Provide at least 'symlink', or 'symlink_target'" \
                               " with either 'symlink_base', 'eggs' or 'develop'")

        result = []
        # remove duplicates by turning the tuple list into a set
        for source, target in set(bulkitems + sourceitems):
            if os.path.exists(target):
                self.logger.debug('Symlink target %s already exists' % target)
                result.append(target)
            elif not os.path.exists(source):
                self.logger.warning('Symlink source not found! %s' % source)
            else:
                os.symlink(source, target)
                self.logger.debug("creating link for %s at %s" % (source, target))
                result.append(target)
        self.logger.debug(result)
        return result


#    def update(self):
#       "Implement recipe API. Just call install for lack of better job."
#       return self.install()
