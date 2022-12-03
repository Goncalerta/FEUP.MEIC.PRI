"""booksearch views Configuration"""

from rest_framework import viewsets

class UserViewSet(viewsets.GenericViewSet):
    """User View Set"""
    pass
    #queryset = User.objects.all()
    #serializer_class = UserSerializer

class WorkstationViewSet(viewsets.ModelViewSet):
    """Define Workstation views"""
    pass
    #serializer_class = WorkstationSerializer
    #permission_classes = (ServiceManagerPermission,)
    #throttle_classes = [UserRateThrottle]

    #def get_queryset(self):
    #    """
    #    Optionally restricts the returned workstations to a given service.
    #    """
    #    queryset = Workstation.objects.all()
    #    queryset = queryset.filter(service_manager_id=self.request.user.id)
    #    return queryset
