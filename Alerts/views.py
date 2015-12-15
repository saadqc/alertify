from django.shortcuts import render_to_response
from AlertManagement.Common.utils import update_response, update_response_logged_in
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView
from Groups.models import Group

__author__ = 'Hp'


class AlertView(TemplateView):
    template_name = 'alerts.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(AlertView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context


class AlertAddView(FormView):
    template_name = 'add_alerts.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(AlertAddView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        groups = Group.objects.filter(owner=request.user)
        context = self.get_context_data()
        context.update({'groups': groups})
        return render_to_response(template_name=self.template_name,
                                  context=context)


class AlertEditView(TemplateView):
    template_name = 'edit_alerts.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(AlertEditView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context
