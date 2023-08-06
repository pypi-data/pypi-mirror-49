========
Overview
========

To have a better understanding of Salut a Toi, this page gives a global view of what it is
and what are the important concepts linked to it. You don't need to read this to use it, but you
can if you wish to understand "who is doing what".

Salut à Toi (or SàT) is a XMPP client. `XMPP`_ is an open standard used
for communication (notably instant messaging but not only). XMPP is a solid standard,
which is decentralised and federated.

SàT is not only focusing on instant messaging, and aims to be a universal communication
tools. In other words, you can use SàT to chat, but also to blog publicly or privately, to
share file, photo albums, to create events, to have discussion forum, etc.

SàT is actually a whole ecosystem, and is made in a way that you can use it with many
different interfaces (or "frontends"). There is a common central part which is called the
"backend", it handles most of the work, while frontends are mostly about the interactions
with user(s).

To work, as SàT is a XMPP **client**, a XMPP **server** is needed. You can either run your
own, or use an existing one (either public, or run by an organisation you belong to, like
family server, run by a friend, your company, university, association, etc.). If you want
to run your own server, there are already plenty of them and happily most of which are
`libre <https://en.wikipedia.org/wiki/Free_software>`_, you can check an `up-to-date list
on the XSF website <https://xmpp.org/software/servers.html>`_ (the XSF or *XMPP Standards
Foundation* being the non-profit organisation taking care of the XMPP standard).

So to summarise, Salut à Toi, or SàT, is a communication ecosystem. Technically, it is a
**XMPP client** which connect to an **XMPP server**. SàT itself works with a **backend**
and one or many **frontends**.

.. _XMPP: https://xmpp.org


Backend
=======

The backend is a daemon, that means that it's a service running in the background.
It takes its main configuration from a file named ``sat.conf`` and can be in different
locations (see below). It uses data in a directory called ``local_dir``, and which
default, on suitable platforms, to the corresponding `XDG directory`_, which is most of
time ``~/.local/share/sat``. In this directory, you'll find the main database in the
``sat.db`` file, which is a `SQLite`_ database.

The backend is run and stopped with the ``sat`` binary. Running it without argument launch
the backend in the background, with ``sat fg`` you run it in the foreground (you'll see
log directly and can stop the backend with ``Ctrl + c``). The ``sat status`` commands help
you discover if the backend is running or stopped.

.. _XDG directory: https://www.freedesktop.org/wiki/Software/xdg-user-dirs/
.. _SQLite: https://sqlite.org

Frontends
=========

Frontends are used to make the interface between user and the backend. Frontends are
adapted to different use cases, and must be started after the backend (if the backend is
not started, you'll see a message telling you so). In most installations, the backend
should be started automatically when you want to use a frontend.

Bellow you'll see a list of the official frontends currently maintained:

Cagou
-----

Cagou is the desktop/mobile frontend. It's probably the main interface for most users. It
is based on the `Kivy`_ framework and should run of most platforms (for now it is
officially tested only on GNU/Linux and Android phones and tablets).

.. _Kivy: https://kivy.org

Libervia
--------

Libervia is the web frontend, and is the second main interface for most users. This
frontend has the particularity to be in 2 parts: a server which serves HTTP content, and a
client which runs in the browser. So you have Libervia server which connect to SàT backend
which itself connect to the XMPP server, and your browser will connect to Libervia server.

In the browser, you can access the server in two ways: either directly with what we call
**Libervia pages**, or with a JavaScript code in `single-page application`_ which is the
**Libervia client** (or **Libervia web app**) that we have mentioned above.

The **Libervia pages** are web pages managing a single feature. They can work without
JavaScript when it's possible (it's not the case for instant messaging or similar highly
dynamic contents). They aims to be simple and straightforward to use.

The **Libervia client** is a highly dynamic web application, used to access more features.
It's more complete and may be well adapted if you want to let SàT running in a browser tab
for an extended period.

Please note that the current web application (SàT 0.7) will be completely rewritten for next 0.8 release.

Last but not least, Libervia is also the central part of the new **web framework** of
Salut à Toi. Indeed, in addition of being a frontend to SàT features (which is built with
this framework), you can create totally different websites which are integrated in SàT
(and so XMPP) ecosystem. This framework uses SàT template engine (based on `Jinja2`_) and
makes the creation of decentralised and federated websites simple. Thanks to this framework,
it's easy to experiment new ideas/features, or to change completely the look and feel of
the Libervia frontend.

The `official SàT website`_ is made with Libervia web framework.

.. _single-page application: https://en.wikipedia.org/wiki/Single-page_application
.. _Jinja2: http://jinja.pocoo.org/
.. _official SàT website: https://salut-a-toi.org

Primitivus
----------

Primitivus is the Terminal User Interface (TUI). In other words, it works in console and
is intended for people at ease with it. Its text only interface has several advantages:
you get rid of many distracting things (like images), it works without graphical
environment installed (which is often the case on servers) and it works on distant shell
(like `ssh`_) while staying gentle with your bandwidth.

Primitivus is shipped with the backend, so it should be always available once SàT is
installed (but some distributions may provide it separately).

You can check :doc:`Primitivus documentation <primitivus/index>` for more details.

.. _ssh: https://en.wikipedia.org/wiki/Secure_Shell

jp
--

Jp is the Command Line Interface (CLI). It's a powerful tool which allows to do nearly
everything you can do with other frontends. Particularly useful if you want to check
something quickly, or if you want to do some automation.

You can check :doc:`jp documentation <jp/index>` documentation for more details.


Glossary
========

While using SàT you may see some terms or concept. This section explain the most important
ones.

profile
-------

A profile is the name linked to an account data. Usually a profile correspond to an XMPP
account, but you can have several profiles using the same XMPP account (with different
parameters) even if this is not usual.

On a SàT installation used by a single user, the profiles are usually used for multiple
accounts. On a multi-users installations, there is usually one profile per user.

When you connect to a SàT frontend, you need to specify a profile and the associated password. The profile password is not the same as the password of the XMPP account. While this may sounds confusing, there are several reason why we use this notion of profile instead of directly the XMPP account/password:

- SàT needs to know the plain XMPP password to connect, and it is encrypted in database.
  The profile password is used to encrypt/decrypt it, this way only a `password hash`_ is
  stored and the XMPP password is encrypted `at rest`_.

- As a further benefit, several passwords could be associated to the same profile (this
  feature is currently not used in SàT).

- profile password can be empty, in which case no password is requested when a profile is
  used

  .. note::

   if you use an empty profile password, the XMPP password won't be encrypted in database
   (or more precisely, will be trivial to decrypt).

- a profile is a simple name associated with an account, it's easier to remember than a
  whole XMPP identifier (also named "JID" for *Jabber ID*)

You always have a *default* profile which is the profile used when you don't select any
(notably used in jp). This is the first profile that you have created except if you have
changed it using a frontend (you can change it with jp).

.. _password hash: https://en.wikipedia.org/wiki/Key_derivation_function
.. _at rest: https://en.wikipedia.org/wiki/Data_at_rest

profile key
-----------

A profile **key** is a special name used as a way to select automatically one profile. The
most important one is ``@DEFAULT@`` which, as you can guess, means the default profile.

bridge
------

The "bridge" is the name used to design Salut à Toi's `IPC`_, or in other words the way
the backend communicate with frontends. Several bridges can be used, the default one being
`D-Bus`_.

The other available bridges are:

pb
  `Perspective Broker`_ is a part of `Twisted`_ (the framework used by the backend and some
  frontends)

embedded
  this embeds the backend into the frontend. The frontend is then using the backend as a
  library.

.. _IPC: https://en.wikipedia.org/wiki/Inter-process_communication
.. _D-Bus: https://www.freedesktop.org/wiki/Software/dbus/
.. _Perspective Broker: https://twistedmatrix.com/documents/current/core/howto/pb-intro.html
.. _Twisted: https://twistedmatrix.com

SàT Media
---------

Most of the frontends use images or other media. To avoid duplication and to make the code
repositories lighter, those media are grouped in a separate repository. The SàT media
repository is available at https://repos.goffi.org/sat_media. You can also download media
at https://ftp.goffi.org/sat_media/sat_media.tar.bz2. The path where SàT media are
installed must be specified in ``sat.conf`` in ``media_dir`` option of the ``[DEFAULT``
section.

SàT Templates
-------------

SàT embeds a `Jinja2`_ template engine (see `Libervia`_ above). "SàT templates" refers to
the default templates (i.e. the official templates, the ones used in default Libervia pages). Those template may also be used by other frontends than Libervia (jp can use them with the :ref:`jp-output` arguments).

SàT templates repository is available at https://repos.goffi.org/sat_templates, they can
also be downloaded at `PyPI <https://pypi.org/project/sat-templates/>`_ and will be
installed automatically if you install Libervia.

Related projects
================

Some project are closely related to Salut à Toi, here is a list of official related
project.

SàT PubSub
----------

Numerous features of Salut à Toi are taking profit of `PubSub`_ functionalities of XMPP.
Because PubSub implementations in the wild are not all on the same level, and some
experimental features are sometimes explored, a PubSub service as been written
specifically for the needs of SàT (but it's not depending on SàT and any XMPP software can
use it).

SàT PubSub aims to be a feature complete, server-independent PubSub implementation, and
try to be up-to-date with latest XMPP PubSub extensions. It is the privileged service to
use with SàT because it supports everything needed (but SàT can work with any XMPP PubSub
service, it will adapt itself to available features).

SàT PubSub can also be used as a `PEP`_ service, if some XMPP extensions are supported by
your server (see below).

.. _PubSub: https://xmpp.org/about/technology-overview.html#pubsub
.. _PEP: https://xmpp.org/extensions/xep-0163.html

XMPP Extension Protocols
------------------------

For the needs of SàT or SàT PubSub, some `XMPP Extension Protocols`_ (or XEP) have been
proposed and got an official number. The current list of extensions is:

`XEP-0355`_: Namespace Delegation
  This has been proposed for the needs of SàT PubSub, and allows the XMPP server to
  "delegate" some features management to a third party service. It is needed to use SàT
  Pubsub as a PEP service.

`XEP-0356`_: Privileged Entity
  In the same spirit as previous one, this has been done so SàT PubSub could be used as a
  PEP service. This extensions allows a "component" (which is more or less a server
  generic plugin) to gain some privileged access to data such as presence information,
  roster or to send a message like if it was sent by the server.

`XEP-0413`_: Order-By
  This extension is used to specify the sorting order in which a client wishes to retrieve
  some results. It is notably used by SàT and SàT PubSub to retrieve items like blog posts
  or tickets in creation order or order of last modification.

.. _XEP-0355: https://xmpp.org/extensions/xep-0355.html
.. _XEP-0356: https://xmpp.org/extensions/xep-0356.html
.. _XEP-0413: https://xmpp.org/extensions/xep-0413.html

.. _XMPP Extension Protocols: https://xmpp.org/about/standards-process.html

Prosody's `mod_delegation`_ and `mod_privilege`_
-------------------------------------------------

Prosody modules have been created to implement the *Namespace Delegation* and *Privileged
Entity* extensions mentioned above. If you use Prosody, you'll have to activate those 2
modules to use SàT PubSub as a PEP service.

.. _mod_privilege: https://modules.prosody.im/mod_privilege.html
.. _mod_delegation: https://modules.prosody.im/mod_delegation.html

SàT official website
--------------------

The official website is made with Libervia web framework. You'll find it at https://repos.goffi.org/sat_web_site

Salut
-----
Probably the smaller side project used by SàT, it is a simple users directory (registration must be done explicitly by users) using `XEP-0055`_ (Jabber Search).

You'll find it at https://repos.goffi.org/salut/

.. _XEP-0055: https://xmpp.org/extensions/xep-0055.html
