#  Copyright (c) 2019 Giacomo Lacava <giac@autoepm.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from django.urls import path

from .views import xero_auth_start, xero_auth_accept, xero_logout, \
    xero_interstitial

urlpatterns = [
    path('start', xero_auth_start, name='xero-auth-start'),
    path('accepted', xero_auth_accept, name='xero-auth-accept'),
    path('logout', xero_logout, name='xero-logout'),
    path('please', xero_interstitial, name='xero-interstitial')
]
