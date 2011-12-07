==========================================
Usage instructions
==========================================

This recipe makes it easy to create symbolic links on Unix variants. Links can be specified one by one, or in bulk. Various shortcuts are provided to avoid unnecessary repetition of source & target paths, etc.

.. warning:: until bug `#144228 <https://bugs.launchpad.net/zc.buildout/+bug/144228>`_ in zc.buildout is fixed, this recipe will fail when linking to directories. There are some `workarounds <workarounds.txt>`_ though, that you can use.

Common options
============================

 - *symlink_base* option may contain a common (source) base directory for symlinking, when links are created for many items from the same directory.
 - *symlink_target* may contain common target directory, when links are created in the same directory.
 - *autocreate* causes a target directory to be created if it does not exist

Specifying individual links
============================

 - *symlink* option contains one or more values in format source=target

Example 1::

 [symlinks]
 symlink = ~/work/MyProj = ${buildout:directory}/products

If a common *symlink_target* is specified, *symlink* can be in format: source= (omitting target directory)

Specifying links in bulk
=========================

Links can be created for all items in a directory given via *symlink_base*, all buildout eggs, and all development eggs. When links are created in bulk, they are always created in directory given by *symlink_target*.

There's also a special option to constrain bulk link creation:

 - *ignore* option contains one or more wildcard expressions for choosing items that will be ignored, ie. no links will be created for them

For files in directory
------------------------

If *symlink_base* & *symlink_target* are specified, but no *symlink* option is given, links are created for all items found in the (source) base directory. Furthermore, even if *symlink* option is used, links can still also be created for all items in *symlink_base* by giving the *bulk* option that forces bulk link creation even if individual *symlink* specification is used.

Example 2::

 [symlinks]
 symlink_base = ~/work/
 symlink_target = ${buildout:directory}/products
 ignore = *.tmp


For eggs in buildout
---------------------

There are two options to generate symlinks for eggs downloaded to a buildout.

 - *eggs*
 - *develop*

The *ignore option* can be used here as well.

Example 3::

 eggs = true
 develop = true
 ignore = *.tar.gz
          *.zip
 symlink_target = ${buildout:directory}/products


Working around bug #144228
============================

The zc.buildout package is (at the end of 2011) considered overcomplex and in need of
overhaul. It is not expected that fix for this bug will be released any time soon.

However, it is always possible to roll a custom version of zc.buildout that has this bug
fixed. Or, you can patch your existing zc.buildout. Here's the patch file::

   --- zc/buildout/buildout.py
   +++ zc/buildout/buildout.py
   @@ -753,9 +753,7 @@
                if not f:
                    continue
                f = self._buildout_path(f)
   -            if os.path.isdir(f):
   -                rmtree(f)
   -            elif os.path.isfile(f):
   +            if os.path.isfile(f) or os.path.islink(f):
                    try:
                        os.remove(f)
                    except OSError:
   @@ -770,6 +768,8 @@
                            # and, of course, it's in use. Leave it.
                            ):
                            raise
   +            elif os.path.isdir(f):
   +                rmtree(f)

        def _install(self, part):
            options = self[part]

There's also a recipe, collective.recipe.patch that could be used, except that it passes
the patched path or egg to buildout. This means the path/egg gets removed by buildout
upon next buildout run, which is not what we'd want here...
