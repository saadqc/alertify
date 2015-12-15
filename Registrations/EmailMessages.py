from AlertManagement import settings
from AlertManagement.settings import SITE_URL
from Registrations.methods import send_email

__author__ = 'Saad'


class EmailMsg:
    def __init__(self):
        pass

    def sendVerificationMsg(self, m):
        send_email('Verification - ' + settings.APP_NAME,
                    'Please click the link below to verify your email address.<br>'
                    '<a href="'+SITE_URL+'/verify?e='+str(m.id)+'&hash='+m.hash_pass+'">Link</a>. The link will expire in 1 day.',
                    [m.email])

    def sendForgotPassCode(self, m):
        send_email('Forgot Password - ' + settings.APP_NAME,
                    'Your passowrd is <div style="color:blue; font-size: 16px">' + m.password + '</div>',
                    [m.email])
