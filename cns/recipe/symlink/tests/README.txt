First, we create a simple filesystem structure to do linking with.
At first, we'll have a file called "my_file.txt" and a directory where
links will be created, giving us paths like this:

/sources/my_dir/my_file.txt
/sources/my_dir/my_file2.txt
/destinations/

Note that this is rooted at a temporary directory, not system root.

>>> sources = tmpdir("sources")
>>> mkdir(sources, "my_dir")
>>> write(sources, "my_dir", "my_file.txt", "This is empty file.")
>>> write(sources, "my_dir", "my_file2.txt", "This is empty file.")
>>> destinations = tmpdir("destinations")

Then, let's create our simple buildout.cfg file with a simple
link:

>>> write(sample_buildout, 'buildout.cfg', """
... [buildout]
... parts = symlink
... [symlink]
... recipe = cns.recipe.symlink
... symlink = %s/my_dir/my_file.txt = %s/my_file.txt""" % (sources, destinations))
>>>
>>> system(buildout + " -N")
'Installing symlink.\n'

>>> import os; os.path.islink(destinations + os.sep + "my_file.txt") 
True

Try symlink_base & symlink_target shortcuts:

>>> write(sample_buildout, 'buildout.cfg', """
... [buildout]
... parts = symlink
... [symlink]
... recipe = cns.recipe.symlink
... symlink_base = %s/my_dir/
... symlink_target = %s
... symlink = my_file.txt""" % (sources, destinations))
>>>
>>> system(buildout + " -N")
'Uninstalling symlink.\nInstalling symlink.\n'

>>> os.path.islink(destinations + os.sep + "my_file.txt")
True

Same, but in bulk:

>>> write(sample_buildout, 'buildout.cfg', """
... [buildout]
... parts = symlink
... [symlink]
... recipe = cns.recipe.symlink
... symlink_base = %s/my_dir/
... symlink_target = %s
... bulk = true""" % (sources, destinations))
>>>
>>> system(buildout + " -N")
'Uninstalling symlink.\nInstalling symlink.\n'

>>> os.path.islink(destinations + os.sep + "my_file.txt")
True
>>> os.path.islink(destinations + os.sep + "my_file2.txt")
True
