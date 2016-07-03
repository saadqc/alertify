from Groups.views import *
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

__author__ = 'Saad'

urlpatterns = [
    # Registration Section
    url(r'^$', login_required(GroupView.as_view(), login_url='/login/'), name='group_view'),
    url(r'^id/(?P<id>[0-9]+)/$', login_required(GroupGetView.as_view(), login_url='/login/'), name='group_get_view'),
    url(r'^create$', login_required(GroupCreateView.as_view(), login_url='/login/'), name='group_create_view'),
    url(r'^delete/(?P<id>[0-9]+)/$', login_required(GroupDeleteView.as_view(), login_url='/login/'), name='group_delete_view'),
    url(r'^add-user$', login_required(GroupUserAddView.as_view(), login_url='/login/'), name='group_user_add_view'),
    url(r'^remove-user$', login_required(GroupUserRemoveView.as_view(), login_url='/login/'), name='group_user_remove_view'),
    url(r'^edit$', login_required(GroupEditView.as_view(), login_url='/login/'), name='group_edit_view'),
]
