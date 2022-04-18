#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS content ES.interfaces module

"""

import logging
from zope.interface import Interface
from zope.schema import Choice

from pyams_utils.interfaces import ZODB_CONNECTIONS_VOCABULARY_NAME
from pyams_zmq.interfaces import IZMQProcess

from pyams_content_es import _


#
# Content indexer utility
#

LOGGER = logging.getLogger('PyAMS (ES content)')


INDEXER_NAME = 'Elasticsearch indexer'
INDEXER_LABEL = _("Elasticsearch documents indexer")


INDEXER_PREFIX = 'pyams_content_es'
INDEXER_STARTER_KEY = f'{INDEXER_PREFIX}.start_handler'
INDEXER_HANDLER_KEY = f'{INDEXER_PREFIX}.tcp_handler'
INDEXER_AUTH_KEY = f'{INDEXER_PREFIX}.allow_auth'
INDEXER_CLIENTS_KEY = f'{INDEXER_PREFIX}.allow_clients'


class IContentIndexerProcess(IZMQProcess):
    """Content indexer process"""


class IContentIndexerHandler(Interface):
    """Content indexer handler interface"""


class IContentIndexerUtility(Interface):
    """Content indexer utility interface"""

    zodb_name = Choice(title=_("ZODB connection name"),
                       description=_("Name of ZODB defining document indexer connection"),
                       required=False,
                       default='',
                       vocabulary=ZODB_CONNECTIONS_VOCABULARY_NAME)

    def get_socket(self):
        """ØMQ socket getter"""

    def test_process(self):
        """Test document indexer process connection"""

    def index_document(self, document):
        """Add or update document to Elasticsearch index"""

    def unindex_document(self, document):
        """Remove document from Elasticsearch index"""


class IDocumentIndexInfo(Interface):
    """Document index info"""


class IDocumentIndexTarget(Interface):
    """Document index target marker interface"""
