from models import UserSetting


class SettingGateWay(object):
    def __init__(self, user):
        self._user = user
    
    def __getattr__(self, k):
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                asObject = UserSetting.objects.get(
                    user = self._user,
                    label=k,
                )
                return asObject.value
            except UserSetting.DoesNotExist:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            if not k.startswith("_"):
                asObject, created = UserSetting.objects.get_or_create(
                    user = self._user,
                    label = k,
                )
                asObject.value = v
                asObject.save()
            else:
                object.__setattr__(self, k, v)
        else:
            object.__setattr__(self, k, v)




class UserSettingDescriptor(object):
    def __get__(self, instance, owner):
        return SettingGateWay(instance)


