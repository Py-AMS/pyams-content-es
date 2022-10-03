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

"""PyAMS_content_es.component.gallery module

This module index content extensions for media galleries.
"""

__docformat__ = 'restructuredtext'

from pyams_content.component.gallery import IGallery, IGalleryFile, IGalleryTarget
from pyams_content_es.interfaces import IDocumentIndexInfo
from pyams_utils.adapter import adapter_config


@adapter_config(context=IGallery,
                provides=IDocumentIndexInfo)
def gallery_index_info(gallery):
    """Gallery index info"""
    info = {}
    if gallery.title:
        for lang, title in gallery.title.items():
            if title:
                info.setdefault(lang, title)
    if gallery.description:
        for lang, description in gallery.description.items():
            if description:
                new_info = f"{info.get(lang, '')}\n{description}"
                info[lang] = new_info
    for image in gallery.values():
        file = IGalleryFile(image, None)
        if (file is None) or not file.visible:
            continue
        for lang, title in (image.title or {}).items():
            if title:
                new_info = f"{info.get(lang, '')}\n{title}"
                info[lang] = new_info
        for lang, description in (image.description or {}).items():
            if description:
                new_info = f"{info.get(lang, '')}\n{description}"
                info[lang] = new_info
        for lang, comments in (image.author_comments or {}).items():
            if comments:
                new_info = f"{info.get(lang, '')}\n{comments}"
                info[lang] = new_info
    return info


@adapter_config(name='gallery',
                required=IGalleryTarget,
                provides=IDocumentIndexInfo)
def gallery_target_index_info(context):
    """Gallery target index info"""
    body = {}
    gallery = IGallery(context)
    info = IDocumentIndexInfo(gallery, None)
    if info is not None:
        for lang, info_body in info.items():
            body[lang] = f"{body.get(lang, '')}\n{info_body}"
    return {
        'gallery': body
    }
