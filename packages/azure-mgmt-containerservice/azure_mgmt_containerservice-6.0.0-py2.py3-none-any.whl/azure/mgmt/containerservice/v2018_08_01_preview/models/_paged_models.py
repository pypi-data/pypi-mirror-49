# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.paging import Paged


class OperationValuePaged(Paged):
    """
    A paging container for iterating over a list of :class:`OperationValue <azure.mgmt.containerservice.v2018_08_01_preview.models.OperationValue>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[OperationValue]'}
    }

    def __init__(self, *args, **kwargs):

        super(OperationValuePaged, self).__init__(*args, **kwargs)
class ManagedClusterPaged(Paged):
    """
    A paging container for iterating over a list of :class:`ManagedCluster <azure.mgmt.containerservice.v2018_08_01_preview.models.ManagedCluster>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[ManagedCluster]'}
    }

    def __init__(self, *args, **kwargs):

        super(ManagedClusterPaged, self).__init__(*args, **kwargs)
