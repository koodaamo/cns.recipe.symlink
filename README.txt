**Simple recipe for creating symbolic links.**

Supported options:

 - *symlink* contains one or more values in format source=target
 - *symlink_base* may contain a common (source) base directory for symlinking, to simplify *symlink* parameter when there are many items from the same directory.
 - *symlink_target* may contain common target directory, to simplify *symlink* parameter when targets (links) are to be created in the same directory. In this case *symlink* can be in format: source= (thus omitting the target part).

Note: If only *symlink_base* & *symlink_target* are specified, links are created for all items found in the (source) base directory.

Example 1::

 [symlinks]
 symlink = ~/work/MyProj = ${buildout:directory}/products

Example 2::

 [symlinks]
 symlink = MyProj
           MyOtherProj
           MyThirdProj
 symlink_base = ~/work/
 symlink_target = ${buildout:directory}/products

Example 3::

 [symlinks]
 symlink = MyProj
           MyOtherProj
           ${buildout:directory}/var/fss-files=${instance1:location}/var
 symlink_base = ~/work/
 symlink_target = ${buildout:directory}/products
