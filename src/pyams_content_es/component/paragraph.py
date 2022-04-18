#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content_es.component.paragraph module

This module defines the adapters which are used to handle paragraphs indexation.
"""

__docformat__ = 'restructuredtext'

from pyams_content.component.paragraph.interfaces import IBaseParagraph, IParagraphContainer, \
    IParagraphContainerTarget
from pyams_content.component.paragraph.interfaces.html import IHTMLParagraph, IRawParagraph
from pyams_content_es.interfaces import IDocumentIndexInfo
from pyams_utils.adapter import adapter_config
from pyams_utils.html import html_to_text


@adapter_config(name='paragraphs',
                required=IParagraphContainerTarget,
                provides=IDocumentIndexInfo)
def paragraph_container_index_info(context):
    """Paragraph container index info"""
    body = {}
    for paragraph in IParagraphContainer(context).get_visible_paragraphs():
        info = IDocumentIndexInfo(paragraph, None)
        if info is not None:
            for lang, body_info in info.items():
                body[lang] = f"{body.get(lang, '')}\n{body_info}"
    return {
        'body': body
    }


@adapter_config(required=IBaseParagraph,
                provides=IDocumentIndexInfo)
def base_paragraph_index_info(context):
    """Base paragraph index info"""
    info = {}
    for lang, title in (getattr(context, 'title', {}) or {}).items():
        if title:
            info.setdefault(lang, title)
    return info


@adapter_config(required=IRawParagraph,
                provides=IDocumentIndexInfo)
@adapter_config(required=IHTMLParagraph,
                provides=IDocumentIndexInfo)
def html_paragraph_index_info(context):
    """HTML paragraph index info"""
    info = base_paragraph_index_info(context)
    for lang, body in (getattr(context, 'body', {}) or {}).items():
        if body:
            info[lang] = f"{info.get(lang, '')}\n" \
                         f"{html_to_text(body).replace(chr(13), '')}"
    return info
