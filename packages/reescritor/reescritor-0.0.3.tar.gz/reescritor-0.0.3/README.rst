reescritor
=============

.. image:: https://reescritor.com/wp-content/uploads/2021/06/reescritor.png
   :alt: Reescritor.com API

A Python module for Article Rewriter (spanish) with `Reescritor.com
<https://reescritor.com>`_.

How to Install
==============

To install using pip run:

    pip install reescritor

How to use this module
======================

This module can be used to rewrite texts in Spanish.

See following example:

from reescritor import ReescritorRequest

provider = "reescritor.com"

apikey = "YOUR_API"


text_in = '''Texto en español de entrada
Puedes poner lo que quieras'''


protected = '''one word per line
other word'''

r = ReescritorRequest.spinner(apikey, text_in, protected, provider)

print(r[text])

print(r[text_nospintax])


Customer Support
----------------
Simply reach out to us via `Telegram Group
<https://t.me/joinchat/AwFbIhzfWQ9zVE8QZKYJow>`_

`Sign up 
<https://reescritor.com/>`_ to get a API key


Licence
=======

This software is licensed under the GNU General Public License (version 3) as published by the Free Software Foundation this licence http://www.gnu.org/licenses/ . If you would want a different licence please contact me, on twitter `@nicolasmarin
<https://twitter.com/@nicolasmarin>`_.
