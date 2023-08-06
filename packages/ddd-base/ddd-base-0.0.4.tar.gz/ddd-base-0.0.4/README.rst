DDD Base Framework
==================

|Build Status| |Pypi Status| |Coveralls Status|

Installation
------------

From source code:

::

    python setup.py install

From pypi:

::

    pip install ddd-base

Usage
-----

::

    import envoy_webhook_auth_decorator

    @envoy_webhook_auth_decorator.authentication({"api_key": ..., "timestamp": ..., "token": ..., "signature": ...})
    def mytest():
        print("Testing...")

    if __name__ == '__main__':
        mytest()


License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/sunwei/ddd-base/blob/master/LICENSE>`_

.. |Build Status| image:: https://travis-ci.com/sunwei/ddd-base.svg?branch=master
   :target: https://travis-ci.com/sunwei/ddd-base
.. |Pypi Status| image:: https://badge.fury.io/py/ddd-base.svg
   :target: https://badge.fury.io/py/ddd-base
.. |Coveralls Status| image:: https://coveralls.io/repos/github/sunwei/ddd-base/badge.svg?branch=master
   :target: https://coveralls.io/github/sunwei/ddd-base?branch=master

