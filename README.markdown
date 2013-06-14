iTunesLoader
============

Easy upload your lossless and mp3 music to iTunes in Mac OS.

Installation
------------

First you need to upload command line version of X Lossless Decoder.
You can find it [here](http://tmkk.pv.land.to/xld/index_e.html).
Don't forget to add it to your PATH variable.


The following dependences are available at [homebrew](http://mxcl.github.com/homebrew/) or
[mac ports](http://guide.macports.org/):

  * `ffmpeg`
  * `cuetools`
  * `atomicparsley` — for attaching coverarts to the audiofiles (albums look more neat in iTunes!)


Python dependences
------------------

  * `mutagen` — library for reading audio file tags

Usage
-----

Upload [iTunesLoader]() and run loader.py. It has one required argument — the path to your music.


License
-------

Copyright (c) Ignatiy Kolesnichenko and Vladimir Moskva. Distribution is free.
