"""
Model class for MyTardis API v1's FacilityResource.
"""

import logging
import requests

from ..conf import config
from .model import Model
from .group import Group

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Facility(Model):
    """
    Model class for MyTardis API v1's FacilityResource.
    """
    def __init__(self, response_dict):
        self.id = response_dict['id']  # pylint: disable=invalid-name
        self.name = response_dict['name']
        self.response_dict = response_dict
        self.manager_group = \
            Group(group_json=response_dict['manager_group'])

    def __str__(self):
        """
        Return a string representation of a facility
        """
        return "<%s: %s>" % (type(self).__name__, self.name)

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of facilities.

        :param filters: Filters, e.g. "id=123" or "name=Test Facility"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Facility` records, encapsulated in a
            `ResultSet` object`.
        """
        from ..utils import add_filters, extend_url
        from .resultset import ResultSet

        url = "%s/api/v1/facility/?format=json" % config.url
        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(Facility, url, response.json())

    @staticmethod
    def get(**kwargs):
        r"""
        Get facility by ID

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the Facility to retrieve

        :return: A :class:`Facility` record.

        :raises requests.exceptions.HTTPError:
        """
        facility_id = kwargs.get("id")
        if not facility_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for Facility get "
                "at this stage.")
        url = "%s/api/v1/facility/%s/?format=json" % (config.url,
                                                      facility_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return Facility(response.json())
