import json
from AlertManagement import settings

__author__ = 'Hp'


def update_response(response):
    """
    Update the title in the response
    :param response: the response which is being sent to user
    :return: updated title response to user
    """
    response['title'] = settings.APP_NAME
    return response


def update_response_logged_in(request, response):
    """
        Update the title in the response
        :param response: the response which is being sent to user
        :return: updated title response to user
        """
    response['title'] = settings.APP_NAME
    response['user'] = request.user
    return response