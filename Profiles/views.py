import json
from django.http.response import JsonResponse
from AlertManagement.settings import BASE_DIR, STATIC_URL
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from AlertManagement.Common.utils import update_response_logged_in
from Registrations.models import User
from django.template.context_processors import csrf
from django.views.generic import TemplateView, View, FormView
import os

__author__ = 'Hp'


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        return context

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=int(kwargs.get('id', -1)))
        context = self.get_context_data()
        context.update({'profile_user': user})
        context.update(csrf(self.request))
        return render_to_response(self.template_name,
                                  context=context
                                  )


class ChangePasswordView(FormView):
    template_name = 'change_password.html'

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        new_pass_again = request.POST.get('new_password_again')
        if old_pass != user.password:
            context = self.get_context_data()
            context.update({'error': 'Invalid current password entered'})
            return render_to_response(self.template_name,
                                      context=context)
        elif new_pass != new_pass_again:
            context = self.get_context_data()
            context.update({'error': "Password doesn't match"})
            return render_to_response(self.template_name,
                                      context=context)

        user.set_password(new_pass)
        user.save()

        return HttpResponseRedirect(reverse('Profiles:profile_view', args=(user.id,)))

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context = update_response_logged_in(self.request, context)
        context.update(csrf(self.request))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render_to_response(self.template_name,
                                  context=context)


class ProfileGetView(View):

    def post(self, request, *args, **kwargs):
        search_field = request.POST.get('q')
        ids = request.POST.get('ids')
        ids = ids.split(',')
        if ids is None:
            ids = []
        users = User.objects.filter(Q(first_name__startswith=search_field) | Q(last_name__startswith=search_field))
        list_users = []
        for user in users:
            if str(user.id) not in ids and user.id != request.user.id:
                list_users.append(dict(label=user.get_full_name(),
                                       value=user.id))
        return JsonResponse(dict(results=list_users))


class ImageChangeView(FormView):

    def post(self, request, *args, **kwargs):
        file_image = request.FILES.get('image')
        file_dir = os.path.join(STATIC_URL, 'media/img/' + str(request.user.id))
        if not os.path.exists(BASE_DIR + "/" + file_dir):
            os.makedirs(BASE_DIR + "/" + file_dir)
        file_path = os.path.join(file_dir, file_image.name)
        if os.path.exists(BASE_DIR + "/" + file_path):
            try:
                os.remove(BASE_DIR + "/" + file_path)
            except Exception:
                print Exception.message
        with open(os.path.join(BASE_DIR + "/" + file_dir, file_image.name), 'wb') as destination:
            for chunk in file_image.chunks():
                destination.write(chunk)
        request.user.profile_img_path = file_path
        request.user.save()
        return HttpResponseRedirect(reverse('Profiles:profile_view', args=(request.user.id,)))
