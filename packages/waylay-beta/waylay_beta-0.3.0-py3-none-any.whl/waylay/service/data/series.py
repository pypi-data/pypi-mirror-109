"""REST definitions for the 'series' entity of the 'data' service."""

from waylay.service import WaylayResource
from waylay.service import decorators

DEFAULT_DECORATORS = [decorators.exception_decorator, decorators.return_body_decorator]


class SeriesResource(WaylayResource):
    """REST Resource for the 'series' entity of the 'data' service."""

    link_roots = {
        'doc': '${doc_url}/api/broker-and-storage/#',
        'iodoc': '${iodoc_url}/api/broker/?id='
    }

    actions = {
        'data': {
            'method': 'GET', 'url': '/resources/{}/series/{}',
            'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(['series']),
            ],
            'description': 'Retrieve the (optionally aggregated) data of a single series.',
            'links': {
                'doc': 'getting-time-series-data',
                'iodoc': 'getting-time-series-data'
            },
        },
        'list': {
            'method': 'GET', 'url': '/resources/{}/series',
            'decorators': [
                decorators.default_params_decorator({'metadata': 'true'}),
                decorators.exception_decorator,
                decorators.return_path_decorator([]),
            ],
            'description': 'Retrieve a list of series and their latest value for a given resource.',
            'links': {
                'doc': 'metadata',
                'iodoc': 'metadata'
            },
        },
        'latest': {
            'method': 'GET', 'url': '/resources/{}/series/{}/latest',
            'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator([])
            ],
            'description': 'Fetch the latest value for a series.',
            'links': {
                'doc': 'latest-value-for-a-series',
                'iodoc': 'latest-value-for-a-series'
            },
        },
        'query': {
            'method': 'POST', 'url': '/series/query',
            'description': 'Execute a broker query document to retrieve aggregated timeseries.',
            'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(['series'])
            ],
            'links': {
                'doc': 'post-timeseries-query',
                'iodoc': 'post-timeseries-query'
            },
        }
    }
