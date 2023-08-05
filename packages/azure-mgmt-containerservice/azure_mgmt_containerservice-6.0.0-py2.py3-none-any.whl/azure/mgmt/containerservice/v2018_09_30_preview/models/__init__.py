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

try:
    from ._models_py3 import NetworkProfile
    from ._models_py3 import OpenShiftManagedCluster
    from ._models_py3 import OpenShiftManagedClusterAADIdentityProvider
    from ._models_py3 import OpenShiftManagedClusterAgentPoolProfile
    from ._models_py3 import OpenShiftManagedClusterAuthProfile
    from ._models_py3 import OpenShiftManagedClusterBaseIdentityProvider
    from ._models_py3 import OpenShiftManagedClusterIdentityProvider
    from ._models_py3 import OpenShiftManagedClusterMasterPoolProfile
    from ._models_py3 import OpenShiftRouterProfile
    from ._models_py3 import PurchasePlan
    from ._models_py3 import Resource
    from ._models_py3 import TagsObject
except (SyntaxError, ImportError):
    from ._models import NetworkProfile
    from ._models import OpenShiftManagedCluster
    from ._models import OpenShiftManagedClusterAADIdentityProvider
    from ._models import OpenShiftManagedClusterAgentPoolProfile
    from ._models import OpenShiftManagedClusterAuthProfile
    from ._models import OpenShiftManagedClusterBaseIdentityProvider
    from ._models import OpenShiftManagedClusterIdentityProvider
    from ._models import OpenShiftManagedClusterMasterPoolProfile
    from ._models import OpenShiftRouterProfile
    from ._models import PurchasePlan
    from ._models import Resource
    from ._models import TagsObject
from ._paged_models import OpenShiftManagedClusterPaged
from ._container_service_client_enums import (
    OSType,
    OpenShiftContainerServiceVMSize,
    OpenShiftAgentPoolProfileRole,
)

__all__ = [
    'NetworkProfile',
    'OpenShiftManagedCluster',
    'OpenShiftManagedClusterAADIdentityProvider',
    'OpenShiftManagedClusterAgentPoolProfile',
    'OpenShiftManagedClusterAuthProfile',
    'OpenShiftManagedClusterBaseIdentityProvider',
    'OpenShiftManagedClusterIdentityProvider',
    'OpenShiftManagedClusterMasterPoolProfile',
    'OpenShiftRouterProfile',
    'PurchasePlan',
    'Resource',
    'TagsObject',
    'OpenShiftManagedClusterPaged',
    'OSType',
    'OpenShiftContainerServiceVMSize',
    'OpenShiftAgentPoolProfileRole',
]
