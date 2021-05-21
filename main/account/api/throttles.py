from rest_framework.throttling import SimpleRateThrottle

class RegisterThrottle(SimpleRateThrottle):
    scope = 'registerthrottle'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated or request.method == 'GET':
            return None
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }



# Handle both get and post method till reach certain times which set in settings.py
# from rest_framework.throttling import AnonRateThrottle

# class RegisterThrottle(AnonRateThrottle):
#     scope = 'registerthrottle'


#Regardless user is_authenticated or anonymous, it throttles calls depend on settings.py
# from rest_framework.throttling import UserRateThrottle

# class RegisterThrottle(UserRateThrottle):
#     scope = 'registerthrottle'



