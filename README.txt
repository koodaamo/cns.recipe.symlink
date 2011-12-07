================================
Introduction
================================

This recipe makes it easy to create symbolic links on Unix variants. Links can be
specified one by one, or in bulk. Various shortcuts are provided to avoid unnecessary
repetition of source & target paths, etc.

Warning: If you're going to be linking to directories, **make sure** to see the wiki
`page <https://github.com/koodaamo/cns.recipe.symlink/wiki/zc.buildout-bug-%23144228>`_
on how to work around zc.buildout bug #144228. Otherwise your buildout will fail.

Common options
===================

 - *symlink_base* option may contain a common (source) base directory for symlinking,
   when links are created for many items from the same directory.
 - *symlink_target* may contain common target directory, when links are created in the
   same directory.
 - *autocreate* causes a target directory to be created if it does not exist


Specifying individual links
=============================

 - *symlink* option contains one or more values in format source=target

Example 1::

 [symlinks]
 symlink = ~/work/MyProj = ${buildout:directory}/products
 autocreate = true


If a common *symlink_target* is specified, *symlink* can be in format: source= (omitting target directory)

Specifying links in bulk
==========================

Links can be created for all items in a directory given via *symlink_base*, all buildout
eggs, and all development eggs. When links are created in bulk, they are always created
in directory given by *symlink_target*.

There's also a special option to constrain bulk link creation:

 - *ignore* option contains one or more wildcard expressions for choosing items that will
   be ignored, ie. no links will be created for them


For files in directory
------------------------

If *symlink_base* & *symlink_target* are specified, but no *symlink* option is given,
links are created for all items found in the (source) base directory. Furthermore, even
if *symlink* option is used, links can still also be created for all items in
*symlink_base* by giving the *bulk* option that forces bulk link creation even if
individual *symlink* specification is used.

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

