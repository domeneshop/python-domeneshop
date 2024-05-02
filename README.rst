domeneshop
==========

Python 3 library for working with the Domeneshop_ API.

**Note:** This library does *not* support Python 2.x.

.. _Domeneshop: https://domene.shop

Installation
------------

``pip3 install domeneshop``

Credentials
-----------

Use of this plugin requires Domeneshop API credentials.

See the `Domeneshop API <https://api.domeneshop.no/docs>`_ documentation for more information.

Examples
--------

Listing DNS records for the first domain in your account:

.. code:: python

    from domeneshop import Client


    if __name__ == "__main__":
        client = Client("<token>", "<secret>")

        domains = client.get_domains()
        domain = domains[0]

        print("DNS records for {0}:".format(domain["domain"]))
        for record in client.get_records(domain["id"]):
            print(record["id"], record["host"], record["type"], record["data"])

More examples can be found in the `examples <examples/>`_ folder.

Documentation
-------------

See the docstrings for `domeneshop.client.Client <src/domeneshop/client.py>`_.
