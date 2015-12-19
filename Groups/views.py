from Registrations.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from Groups.models import Group
from django.template.context_processors import csrf
from django.views.generic.list import ListView
from AlertManagement.Common.utils import update_response_logged_in
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

__author__ = 'Hp'

from AlertManagement.Common import faker


class GroupView(ListView):
    model = Group
    template_name = 'groups.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(GroupView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        list_group = Group.objects.all()
        paginator = Paginator(list_group, self.paginate_by)
        if list_group.count() > 0:
            context.update({'is_paginated': True})
        page = self.request.GET.get('page')

        try:
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)

        context['list_groups'] = groups
        return context


class GroupEditView(TemplateView):
    template_name = 'edit_groups.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(GroupEditView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context


class GroupCreateView(FormView):
    template_name = 'create_groups.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        context.update(csrf(self.request))
        return context

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name,
                                  context=self.get_context_data())

    def post(self, request, *args, **kwargs):
        group_name = request.POST.get('name')
        members_id = request.POST.getlist('member_id')
        group = Group.objects.create(name=group_name,
                                     owner=request.user)
        for id in members_id:
            user = User.objects.get(id=int(id))
            group.users.add(user)
        group.save()
        return HttpResponseRedirect(reverse('Groups:group_view'))


class GroupGetView(ListView):
    paginate_by = 30
    template_name = 'group.html'
    model = User

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(GroupGetView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        group = get_object_or_404(Group, pk=int(self.kwargs['id']))
        list_users = group.users.all()
        paginator = Paginator(list_users, self.paginate_by)
        if list_users.count() > 0:
            context.update({'is_paginated': True})
        page = self.request.GET.get('page')
        context.update({'group': group})
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        context['list_users'] = users
        return context


class GroupDeleteView(FormView):

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(GroupDeleteView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=int(kwargs['id']))
        if group.owner.id != request.user.id:
            raise Http404()
        group.delete()
        return HttpResponseRedirect(reverse('Groups:group_view'))


class GroupUserAddView(FormView):
    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(GroupUserAddView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=int(self.request.POST['group_id']))
        if group.owner.id != request.user.id:
            raise Http404()
        user = get_object_or_404(User, pk=int(self.request.POST['member_add']))
        group.users.add(user)
        group.save()
        return HttpResponseRedirect(reverse('Groups:group_get_view', args=[group.id, ]))


class GroupUserRemoveView(FormView):
    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(GroupUserRemoveView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=int(self.request.POST['group_id']))
        if group.owner.id != request.user.id:
            raise Http404()
        user = get_object_or_404(User, pk=int(self.request.POST['member_ids']))
        group.users.remove(user)
        group.save()
        if group.users.count() == 0:
            group.delete()
        return HttpResponseRedirect(reverse('Groups:group_get_view', args=[group.id, ]))
