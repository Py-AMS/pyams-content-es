# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_content_es.interfaces import IContentIndexerUtility
from pyams_elastic.include import client_from_config
from pyams_utils.factory import create_object
from pyams_utils.interfaces.monitor import IMonitorExtension, IMonitorExtensionStatus
from pyams_utils.registry import query_utility, utility_config

__docformat__ = 'restructuredtext'


@utility_config(name='pyams_content_es.monitor',
                provides=IMonitorExtension)
class ElasticsearchContentMonitor:
    """Elasticsearch indexer monitor utility"""

    def get_status(self, request):
        registry = request.registry
        es_client = client_from_config(registry.settings)
        if not es_client.es.ping():
            yield create_object(IMonitorExtensionStatus,
                                handler='pyams_content_es.monitor:client',
                                status='DOWN',
                                message='Elasticsearch server not available!')
        else:
            yield create_object(IMonitorExtensionStatus,
                                handler='pyams_content_es.monitor:client',
                                status='UP')
            indexer = query_utility(IContentIndexerUtility)
            if indexer is None:
                yield create_object(IMonitorExtensionStatus,
                                    handler='pyams_content_es.monitor:indexer',
                                    status='DOWN',
                                    message='Missing content indexer utility!')
            else:
                yield create_object(IMonitorExtensionStatus,
                                    handler='pyams_content_es.monitor:indexer',
                                    status='UP')
                status_code, message = indexer.test_process()
                if status_code == 200:
                    yield create_object(IMonitorExtensionStatus,
                                        handler='pyams_content_es.monitor:indexer:process',
                                        status='UP',
                                        message=message)
                else:
                    yield create_object(IMonitorExtensionStatus,
                                        handler='pyams_content_es.monitor:indexer:process',
                                        status='DOWN',
                                        message=f'Content indexer process not running: {message}')
