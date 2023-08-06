==========================================================
polaroidme - converts an image into vintage polaroid style
==========================================================

polaroidme is a simple to use command-line-tool for placing an image into a
Polaroid-like frame and optionally put a title / description on the bottom.
The default font mimics scribbled handwriting but any (ttf-)font
which suits your taste is supported. The tool offers basic features
like auto-scaling up-/downwards and/or cropping, using any (ttf-)font,
supports high-res output and gets it's job done well.

polaroidme is actively maintained & developed (2019). To see if it fits
your needs take a look at the project's github-repo and check out the
[examples](https://github.com/s3h10r/polaroidme/blob/master/README.md)

Contributions are welcome, and they are greatly appreciated!

Example output:

<img src="/examples/example.ps-10.polaroid.png" width="48%"></img>
<img src="/examples/example2.ps-10.polaroid.jpg" width="48%"></img>
<img src="/examples/example.corkboard.jpg" width="48%"></img>
<img src="/examples/DSCF6061.polaroid.jpg" width="48%"></img>
<img src="/examples/DSCF2330.polaroid.nocrop.png" width="48%"></img>
<img src="./examples/DSCF2313.polaroid.nocrop.png" width="48%"></img>

```
Usage:

  polaroidme [options] source-image [size] [alignment] [title]

Where:

  source-image  name of the image file to transform. If no extension is
                specified .jpg is assumed.
  size          size of the picture part of the polaroid (default=800)
  alignment     This specifies the portion (crop) of the image to include in the final
                output. One of 'top', 'left', 'bottom', 'right' or 'center'.
                'top' and 'left' are synonomous as are 'bottom' and
                'right'. (default="center"). Omitted if --nocrop option is set
  title         If specified defines the caption to be displayed at the
                bottom of the image. (default=None)

Available options are:

  --nocrop        Rescale the image to fit fullframe in the final output
                  (default="--crop"). btw. alignment is ignored if option is set.
  --clockwise     Rotate the image clockwise before processing
  --anticlockwise Rotate the image anti-clockwise before processing
```

example usage:

```console
foo@bar:~$ polaroidme --crop ./example/example.png .jpg 800 center "--crop option center"
foo@bar:~$ feh ./example/example.polaroid.png
foo@bar:~$ polaroidme --nocrop ./example/example.png .jpg 800 "--nocrop option"
foo@bar:~$ feh ./example/example.polaroid.png
```

installation
------------

The latest stable release can be found on [pypi](https://pypi.org/project/polaroidme/)
and therefore installed via **`pip install polaroidme`**.

Instead of installing the software system-wide it's usally best practice to install
it in a python-virtualenv:

```console
foo@bar:~$ python3 -m venv vent_polaroidme
foo@bar:~$ source venv_polaroidme/bin/activate
(venv_polaroidme) foo@bar:~$ pip install polaroidme
[...]
Installing collected packages: polaroidme
  Running setup.py install for polaroidme ... done
Successfully installed polaroidme-0.8.6
(venv_polaroidme) foo@bar:~$ polaroidme
(venv_polaroidme) foo@bar:~$ ...
(venv_polaroidme) foo@bar:~$ deactivate
foo@bar:~$
```

TODO
----

 - implement a more convenient arparsing
   (add ``--use-font <pathtofont>``, shorten the --nocrop call (alignment is unused in this case, ...)
 - custom colors
 - option to put a description-text below title
 - automated testing
 - eye-candy like distortion filters
 - rewrite corkboard (lab-branch) and add to master


 changelog
 ---------

 **0.9.1**
 - argument alignment omitted if `--nocrop option` is set
 - updates packaging meta-data & docs
 - adds more free fonts. changes default font to [Jakes Handwriting](https://www.dafont.com/jakeshandwriting.font)

 **0.9.0**
 - packaging (pypi)

 **0.8.4**
 - updates usage-string
 - adds correct file encoding (`pydoc3 ./polaroidme`)

 **0.8.2**
 - adds free example fonts (source: https://www.dafont.com/ttf.d592)
 - support for different fonts via argument

 **0.8.0**
 - supports for high-res output (argument size, default=800)
 - adds `--nocrop` option
 - refactoring

 **0.1.0**

 - initial commit based on https://github.com/thegaragelab/pythonutils/tree/master/polaroid
 - converts to python3
