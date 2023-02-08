# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.hello import HelloWorld
# from resources.iapi import iapi_resources
from resources.template import templates_resources
from resources.authentication import auth_resources
from resources.user import users_resources

api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    # **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    **{f'/template{k}': val for k, val in templates_resources.items()},
    **{f'/auth{k}': val for k, val in auth_resources.items()},
    **{f'/user{k}': val for k, val in users_resources.items()},
}
