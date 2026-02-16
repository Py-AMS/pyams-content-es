# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from elasticsearch_dsl import A, AttrDict, Search

from pyams_catalog.query import CatalogResultSet
from pyams_content.shared.view.interfaces import RELEVANCE_ORDER
from pyams_content.shared.view.interfaces.query import IViewQuery
from pyams_elastic.include import get_client
from pyams_utils.list import unique_iter
from pyams_utils.request import query_request

__docformat__ = 'restructuredtext'


def get_merged_results(views, context, request=None, get_user_params=False, aggregates=None,
                       sort_index=None, reverse=False, limit=None, **kwargs):
    """Get results from merged views"""
    if request is None:
        request = query_request()
    client = get_client(request)
    search_params = []
    for view in views:
        query = IViewQuery(view, None)
        if query is not None:
            params = query.get_params(context, request, get_user_params=get_user_params, **kwargs)
            if params is None:
                continue
            search_params.append(Search().query(params).to_dict()['query'])
    if not search_params:
        return (), 0, {}
    combined_params = {'bool': {'should': search_params}}
    search = Search(using=client.es, index=client.index) \
        .params(request_timeout=30) \
        .query(combined_params) \
        .source(['internal_id'])
    if aggregates:
        for agg in aggregates:
            search.aggs.bucket(agg['name'],
                               A(agg['type'], **agg['params']))
    # Define sort order
    sort_values = []
    if (not sort_index) or (sort_index == RELEVANCE_ORDER):
        sort_values.append({
            '_score': {
                'order': 'desc'
            }
        })
    else:
        sort_values.append({
            'workflow.{0}'.format(sort_index): {
                'order': 'desc' if reverse else 'asc',
                'unmapped_type': 'date'
            }
        })
    if sort_values:
        search = search.sort(*sort_values)
    if limit:
        search = search[:limit]
    else:
        search = search[:999]
    results = search.execute()
    items = CatalogResultSet([result.internal_id for result in results.hits])
    aggregations = results.aggregations
    total_count = results.hits.total
    if isinstance(total_count, (dict, AttrDict)):
        total_count = results.hits.total['value']
    return unique_iter(items), total_count, aggregations
