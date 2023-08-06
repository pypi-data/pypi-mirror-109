"""Core class for VeraCore"""

DEFAULT_API_VERSION = '2.0'

import datetime
import logging

import requests

from .constants import \
        ORDER_STATUSES, \
        SHIPPING_LABEL_STATUSES

from .exceptions import \
        VeraCoreRequestForbidden, \
        VeraCoreNoSession, \
        VeraCoreRequestError


# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class VeraCore:
    """ VeraCore API Client Class """

    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    def __init__(
            self,
            username,
            password,
            system_id,
            domain,
            session=None,
            authentication_token=None,
            version=DEFAULT_API_VERSION,
        ):
        """ Initialize the instance with the given parameters. """

        self.username = username
        self.password = password
        self.system_id = system_id
        self.domain = domain
        self.session = session or requests.Session()
        self.authentication_token = authentication_token
        self.authentication_token_expiration = None
        self.api_version = version

        self.login()

    def login(self):
        """ authenticate the instance for future requests """
        url = 'https://%s/VeraCore/Public.Api/api/login' % self.domain
        request = self.session.post(
            url, json={
                "userName": self.username,
                "password": self.password,
                "systemId": self.system_id
            })

        data = request.json()

        if request.status_code == 403:
            raise VeraCoreRequestForbidden(
                url, request.status_code, 'Login',
                data.get('Error', 'Unknown') if data else 'Unknown')
        elif request.status_code != 200:
            raise VeraCoreRequestError(
                url, request.status_code, 'Login',
                data.get('Error', 'Unknown') if data else 'Unknown')
        else:
            self.authentication_token = data.get('Token', None)
            self.authentication_token_expiration = datetime.datetime.strptime(
                data.get('UtcExpirationDate').split('.')[0],
                '%Y-%m-%dT%H:%M:%S') \
                    if data.get('UtcExpirationDate', None) else None

    def check_authentication_token(self):
        """Verify that a authentication token exists and has not expired"""
        return bool(
            self.authentication_token and \
                self.authentication_token_expiration > datetime.datetime.now())

    def get_orders(
            self,
            order_status=None,
            shipping_label_status=None,
            single_piece=None,
            carrier_code=None,
            stream=None,
            stream_start=None,
            stream_end=None,
            ):
        """ get orders matching the specified criteria """

        url = 'https://%s/VeraCore/Public.Api/api/orders?api=True' % self.domain

        if order_status and order_status in ORDER_STATUSES:
            url = '%s&request.status=%s' % (url, order_status)

        if shipping_label_status and \
                shipping_label_status in SHIPPING_LABEL_STATUSES:
            url = '%s&request.shippingLabelStatus=%s' % (
                url, shipping_label_status)

        if single_piece and isinstance(single_piece, bool):
            url = '%s&request.singlePiece=%s' % (url, single_piece)

        if carrier_code and isinstance(carrier_code, str):
            url = '%s&request.carrierCode=%s' % (url, carrier_code)

        if stream and isinstance(stream, str):
            url = '%s&request.carrierCode=%s' % (url, stream)

        if stream_start and isinstance(stream_start, datetime.datetime):
            url = '%s&request.streamAssignedUTCStartDate=%s' % (
                url,
                datetime.datetime.strftime(stream_start, '%Y-%m-%dT%H:%M:%S'))

        if stream_end and isinstance(stream_end, datetime.datetime):
            url = '%s&request.streamAssignedUTCEndDate=%s' % (
                url,
                datetime.datetime.strftime(
                    stream_end, '%Y-%m-%dT%H:%M:%S'))

        if not self.authentication_token or \
                not self.authentication_token_expiration or \
                datetime.datetime.now() > self.authentication_token_expiration:
            raise VeraCoreNoSession(url, None, 'Orders', '')

        request = self.session.get(
            url,
            headers={
                'Authorization': 'Bearer %s' % \
                    self.authentication_token
            })

        data = request.json()

        if request.status_code == 403:
            raise VeraCoreRequestForbidden(
                url, request.status_code, 'Orders',
                data.get('Error', 'Unknown') if data else 'Unknown')
        elif request.status_code != 200:
            raise VeraCoreRequestError(
                url, request.status_code, 'Orders',
                data.get('Error', 'Unknown') if data else 'Unknown')
        else:
            return data.get('Orders', [])
