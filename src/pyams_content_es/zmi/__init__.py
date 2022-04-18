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

"""PyAMS_content_es.zmi module

This module defines a few components used to handle Elasticsearch content
indexer utility properties.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_content_es.interfaces import IContentIndexerUtility, INDEXER_LABEL
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces.form import IInnerSubForm
from pyams_form.subform import InnerDisplayForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_skin.schema.button import ActionButton
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.url import absolute_url
from pyams_zmi.form import AdminInnerDisplayForm, AdminModalDisplayForm, AdminModalEditForm
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.form import IModalEditFormButtons
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_label

from pyams_content_es import _


@adapter_config(required=(IContentIndexerUtility, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def content_indexer_label(context, request, view):
    """Content indexer label"""
    return request.localizer.translate(INDEXER_LABEL)


@adapter_config(required=(IContentIndexerUtility, IAdminLayer, Interface),
                provides=ITableElementEditor)
class ContentIndexerElementEditor(TableElementEditor):
    """Content index element editor"""

    def __new__(cls, context, request, view):
        if not request.has_permission(MANAGE_SYSTEM_PERMISSION, context=context):
            return None
        return TableElementEditor.__new__(cls)


class IContentIndexerPropertiesEditFormButtons(IModalEditFormButtons):
    """Content indexer properties edit form buttons"""

    test = ActionButton(name='test',
                        title=_("Test connection"))


@ajax_form_config(name='properties.html',
                  context=IContentIndexerUtility, layer=IPyAMSLayer,
                  permission=MANAGE_SYSTEM_PERMISSION)
class ContentIndexerPropertiesEditForm(AdminModalEditForm):
    """Content indexer properties edit form"""

    @property
    def title(self):
        return get_object_label(self.context, self.request, self)

    legend = _("Document indexer properties")
    fields = Fields(IContentIndexerUtility)
    buttons = Buttons(IContentIndexerPropertiesEditFormButtons).select('test', 'apply', 'close')

    def update_actions(self):
        super().update_actions()
        test = self.actions.get('test')
        if test is not None:
            test.add_class('btn-info mr-auto')
            test.href = absolute_url(self.context, self.request, 'test-indexer.html')
            test.modal_target = True

    @handler(IContentIndexerPropertiesEditFormButtons['apply'])
    def handle_apply(self, action):
        """Apply button handler"""
        super().handle_apply(self, action)


@ajax_form_config(name='test-indexer.html',
                  context=IContentIndexerUtility, layer=IPyAMSLayer,
                  permission=MANAGE_SYSTEM_PERMISSION)
class ContentIndexerTestForm(AdminModalDisplayForm):
    """Content indexer test form"""

    @property
    def title(self):
        return get_object_label(self.context, self.request, self)


@adapter_config(name='test',
                required=(IContentIndexerUtility, IAdminLayer, ContentIndexerTestForm),
                provides=IInnerSubForm)
@template_config(template='templates/test-indexer.pt', layer=IAdminLayer)
class ContentIndexerTestStatusForm(InnerDisplayForm):
    """Content indexer test status form"""

    legend = _("Content indexer test")

    def test(self):
        """Content indexer test"""
        return self.context.test_process()
