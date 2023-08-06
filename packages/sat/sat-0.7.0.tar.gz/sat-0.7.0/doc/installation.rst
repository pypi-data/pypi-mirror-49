.. _installation:

============
Installation
============

This are the instructions to install SàT using Python.
Note that if you are using GNU/Linux, Salut à Toi may already be present on your distribution.

Salut à Toi is made of one backend, and several frontends. To use it, the first thing to do is to install the backend.

We recommand to use development version for now, until the release of
0.7 version which will be "general public" version.

Also note that SàT is still using Python 2 (this will change for 0.8 version which will be Python 3 only), so all instructions below have to be made using python 2.

Development version
-------------------

*Note for Arch users: a pkgbuild is available for your distribution on
AUR, check sat-xmpp-hg (as well as other sat-\* packages).*

You can install the latest development version using pip. You need to
have the following dependencies installed first:

-  Python 2 with development headers
-  Mercurial
-  VirtualEnv
-  libcairo 2 with development headers
-  libjpeg with development headers
-  libgirepository 1.0 with development headers
-  libdbus-1 with development headers
-  libdbus-glib-1 with development headers
-  libxml2 with development headers
-  libxlt2 with development headers
-  D-Bus x11 tools (this doesn't needs X11, it is just needed for dbus-launch)
-  cmake

On Debian and derivatives, you can get all this with following command::

  $ sudo apt-get install python-dev mercurial virtualenv libxml2-dev libxslt-dev libcairo2-dev libjpeg-dev libgirepository1.0-dev libdbus-1-dev libdbus-glib-1-dev dbus-x11 cmake

Now go in a location where you can install Salut à Toi, for
instance your home directory::

  $ cd

And enter the following commands (note that *virtualenv2* may be named
*virtualenv* on some distributions, just be sure it's Python **2** version)::

  $ virtualenv2 env
  $ source env/bin/activate
  $ pip install hg+https://repos.goffi.org/sat

Don't worry if you see the following message, SàT should work anyway::

  Failed building wheel for pygobject

After installing SàT, you need to install the media::

  $ cd
  $ hg clone https://repos.goffi.org/sat_media

then, create the file ~/.config/sat/sat.conf containing:

.. sourcecode:: cfg

  [DEFAULT]
  media_dir = ~/sat_media

Of course, replace ``~/sat_media`` with the actual path you have used.

.. following part is currently hidden until v0.7 is released

  Last release
  ------------

  This release is really old and code has changed a lot since it.
  Furthermore, stable version is currently not maintained. We recommend to use current dev version until version 0.7 is released.

  If you are willing to install last release anyway, here are the instructions.

  You can automatically install SàT and its dependencies using
  easy_install or pip. You will however need to install Python's headers
  (needed to build some packages),
  `PyGObject <http://ftp.gnome.org/pub/GNOME/sources/pygobject/>`__ and
  developments version of libxml2 and libxslt (to compile lxml python
  library). On some ARM systems like Raspberry Pi or OLinuXino, it is also
  required to install libjpeg-dev and libffi-dev beforehand.

  The environment variable SAT_INSTALL customises the installation, it
  contains flags separated by spaces:

  -  "nopreinstall" skip all preinstallation checks
  -  "autodeb" automatically install missing packages on Debian based
     distributions

  PyGobject is automatically installed on Debian based distributions if
  "autodeb" option is set. Indeed, on Debian based distribution, you can
  type:

  | ``sudo apt-get install python-pip python-virtualenv python-dev libxml2-dev libxslt-dev libjpeg-dev libffi-dev zlib1g-dev``
  | ``virtualenv --system-site-packages sat``
  | ``source sat/bin/activate``
  | ``pip2 install -U setuptools``
  | ``SAT_INSTALL="autodeb" pip2 install sat``

  After installing SàT, you need to install the media:

  | ``mkdir -p /path/to/sat_media``
  | ``cd /path/to/sat_media``
  | ``wget ``\ ```ftp://ftp.goffi.org/sat_media/sat_media.tar.bz2`` <ftp://ftp.goffi.org/sat_media/sat_media.tar.bz2>`__
  | ``tar -jxvf sat_media.tar.bz2``

  then, create a ~/.sat.conf file which contains:

  | ``[DEFAULT]``
  | ``media_dir=/path/to/sat_media``

  Of course, replace /path/to/sat_media with the actual path you want to
  use.

Usage
=====

To launch the sat backend, enter::

  $ sat

…or, if you want to launch it in foreground::

  $ sat fg

You can stop it with::

  $ sat stop

To know if backend is launched or not::

  $ sat status

**NOTE**: since SàT v0.5.0, the backend is automatically launched when a frontend needs it.

You can check that SàT is installed correctly by trying jp (the backend need to be launched first, check below)::

  $ jp --version
  jp 0.7.0D « La Commune » (rev 2dd53ffa4781 (default 2019-02-22 18:58 +0100) +110) Copyright (C) 2009-2019 Jérôme Poisson, Adrien Cossa
  This program comes with ABSOLUTELY NO WARRANTY;
  This is free software, and you are welcome to redistribute it under certain conditions.

If you have a similar output, SàT is working.

Frontends
=========

So far, the following frontends exist and are actively maintained:

Cagou
  desktop/mobile (Android) frontend

Libervia
  the web frontend

Primitivus
  Text User Interface

jp
  Command Line Interface

To launch Primitivus, just type::

  $ primitivus

then create a profile (XMPP account must already exist).

To use jp, follow its help::

  $ jp --help


There are some other frontends:

Bellaciao
  based on Qt, a rich desktop frontend (currently on hold)

Wix
  former desktop frontend based on WxWidgets (deprecated with version 0.6.0)

Sententia
  Emacs frontend developed by a third party (development is currently stalled)
