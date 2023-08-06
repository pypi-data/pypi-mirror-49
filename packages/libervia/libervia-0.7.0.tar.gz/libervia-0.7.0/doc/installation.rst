============
Installation
============

This are the instructions to install Libervia (SàT) using Python.
Note that if you are using GNU/Linux, Libervia may already be present on your distribution.

Libervia is a Salut à Toi frontend, the SàT backend must be installed first (if you
haven't installed it yet, it will be downloaded automatically as it is a dependency of
Libervia). Libervia and SàT backend must always have the same version (Libervia won't
start if the version backend has not the same version).

We recommend to use development version for now, until the release of
0.7 version which will be "general public" version.

Also note that Libervia as all SàT ecosystem is still using Python 2 (this will change for
0.8 version which will be Python 3 only), so all instructions below have to be made using
python 2.

Development Version
-------------------

*Note for Arch users: a pkgbuild is available for your distribution on
AUR, check sat-libervia-hg (as well as other sat-\* packages).*

You can install the latest development version using pip. Please check backend documentation
to see the system dependencies needed.

You can use the same virtual environment as the one used for installing the backend. If
you haven't installed it yet, just select a location when you want to install it, for
instance your home directory::

  $ cd

And enter the following commands (note that *virtualenv2* may be named
*virtualenv* on some distributions, just be sure it's Python **2** version)::

  $ virtualenv2 env
  $ source env/bin/activate
  $ pip install hg+https://repos.goffi.org/libervia

If you haven't done it for the backend, you need to install the media::

  $ cd
  $ hg clone https://repos.goffi.org/sat_media

Post Installation
-----------------

Libervia uses its own XMPP account to fetch public data. You need to create a profile
named `libervia` linked to this account to launch Libervia. First create an account
dedicated to this on your XMPP server. For instance with `Prosody`_ you would enter
something like::

  $ prosodyctl adduser libervia@example.net

Where you'll obviously change ``libervia@example.net`` for the JID you want to use, with
your domain name. You'll then be prompted for a password. You can now create the
associated SàT profile::

  $ jp profile create libervia -j libervia@example.net -p <libervia_password>

.. note::

   jp doesn't prompt for password yet, this means that the password is visible to anybody
   looking at your screen and will stay in your shell history, and the password will be
   visible for a few seconds in process list. If this is a concern for you (e.g. you use a
   shared machine), use an other frontend to create the profile, or do the necessary to
   remove the password from history.

Finally, you need to specify to specify the password of this ``libervia`` profile in your
configuration. To do so, edit your ``sat.conf`` and edit ``[libervia]`` and set the
``passphrase`` option to the profile password you have used in the command above:

.. sourcecode:: cfg

    [libervia]
    passphrase = <libervia_password>

You should now be good to run the Libervia server.

.. _Prosody: https://prosody.im


Usage
=====

To launch the Libervia server, enter::

  $ libervia

…or, if you want to launch it in foreground::

  $ libervia fg

You can stop it with::

  $ libervia stop

To know if backend is launched or not::

  $ libervia status


SàT Pubsub
==========

Some functionalities use advanced or experimental features of XMPP PubSub. We recommend to
use the SàT PubSub service that is a side project developed for the needs of Salut à Toi,
and consequently implements everything needed. Please refer to SàT PubSub documentation to
know how to install and use it.
