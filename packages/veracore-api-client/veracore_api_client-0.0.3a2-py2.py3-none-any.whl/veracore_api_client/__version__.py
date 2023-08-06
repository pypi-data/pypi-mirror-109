"""
Version details for VeraCore API Client
"""

__title__ = 'veracore_api_client'
__description__ = 'A simple class-based Python client for getting data \
                  from the VeraCore REST API'
__url__ = 'https://github.com/veracore-api/veracore-api-client-python'
__version__ = '0.0.3.alpha2'
__author__ = 'Eli Keimig'
__author_email__ = 'ewkeimig@cyclops26.com'
__license__ = 'GNU General Public License v3 or later (GPLv3+)'
__maintainer__ = 'Eli Keimig'
__maintainer_email__ = 'ewkeimig@cyclops26.com'
__keywords__ = 'python veracore oms wms veracore.com'


def get_version_information(display=True, debug=False):
    """ prints the package version information """
    # pylint: disable=line-too-long
    version = 'VeraCore API Python Client: Version {version}. Released under a {license} license. Author: {author}.'.format(
                  version=__version__, license=__license__, author=__author__
              )
    if display:
        print(version)
    return version if not display or debug else None
