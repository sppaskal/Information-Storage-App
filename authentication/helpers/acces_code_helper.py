from ..models import AccessCode
from django.core.exceptions import ObjectDoesNotExist


class AccessCodeHelper():

    @staticmethod
    def get_access_code_instance_by_user_id(user_id):
        try:
            return AccessCode.objects.get(user=user_id)
        except AccessCode.DoesNotExist:
            return None

    @staticmethod
    def create_access_code_entry(access_code_data):
        return AccessCode.objects.create(
            user=access_code_data.get("user"),
            code=access_code_data.get("code")
        )
