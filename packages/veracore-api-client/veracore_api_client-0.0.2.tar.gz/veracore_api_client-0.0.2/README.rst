*******************
VeraCore API Client
*******************

.. image:: https://api.travis-ci.org/VeraCore-API/veracore-api-client-python.svg?branch=master
   :target: https://travis-ci.org/VeraCore-API/veracore-api-client-python

.. image:: https://readthedocs.org/projects/veracore-api-client-python/badge/?version=latest
   :target: https://veracore-api-client-python.readthedocs.io/en/latest/
   :alt: Documentation Status

The VeraCore API Client is a basic VeraCore.com REST API client built for Python.

Compatibility & Unit Testing are actively done against Python 3.8 and 3.9.

=============

You can find out more regarding the API in the `Official VeraCore.com REST API Documentation`_

.. _Official VeraCore.com REST API Documentation: https://support.veracore.com/support/s/apiobject

The Swagger documentation can be found here: `https://{domain}.veracore.com/VeraCore/Public.Api/swagger/ui/index`

* Replace `{domain}` with your VeraCore domain name

Examples
--------------------------
Retrieving orders that are in an unprocessed state:

.. code-block:: python

    from veracore_api_client import VeraCore
    from veracore_api_client.constants import ORDER_STATUS_UNPROCESSED


    veracore = VeraCore(username='APIUsername', password='APIPassword', system_id='APISystemID', domain='VCDomain.veracore.com')
    orders = veracore.get_orders(order_status=ORDER_STATUS_UNPROCESSED)

    for order in orders:
      print('ID: %s | Status: %s | Stream: %s | Ordered By: %s | Ship To: %s' % (
         order['ID'], order['CurrentOrderStatus'], order['OrderClassification']['OrderProcessingStream'],
         order['OrderedBy']['Name'], ','.join([shipment['ShipTo']['Name'] for shipment in order['Shipments']])
      ))

Authors & License
--------------------------

This package is released under an open source GNU General Public License v3 or later (GPLv3+) license. This package was originally created by Eli Keimig.

The latest build status can be found at `Travis CI`_

.. _Eli Keimig: https://github.com/cyclops26
.. _GitHub Repo: https://github.com/VeraCore-API/veracore-api-client-python
.. _Travis CI: https://travis-ci.com/VeraCore-API/veracore-api-client-python
