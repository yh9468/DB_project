from app.models import MyUser
from django.conf import settings
import logging

class MyAuthBackend(object):
    def authenticate(self,request, username = None, password=None):
        try:
            user = MyUser.objects.get(phonenum=username)
            print("user {}".format(type(user)))
            """
            if user.check_password(password):
                return user
            else:
                return None
            """
            return user
        except MyUser.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists ")
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)  # 유저가 활성화 되었는지
        return is_active or is_active is None  # 유저가 없는 경우 is_active는 None이므로 True

    def get_user(self, user_id):
        try:
            user = MyUser.objects.get(pk=user_id)           #아마도 DB에 접근한거같아서 pk로했다 만약 여기서 뻑나면 phonenum으로 바꾸자.
            if user.is_active:
                return user
            return None
        except MyUser.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None