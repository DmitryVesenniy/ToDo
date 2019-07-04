from django.contrib.auth.models import User

from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .serializers import UserSerializer, TodoSerializer, OrganizationSerializer
from .models import ToDoModel, OrganizationModel
from .permission import IsOrganizationUserOrReadOnly


class UserView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class OrganizationView(viewsets.ModelViewSet):

    queryset = OrganizationModel.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAdminUser,)


class TodoView(viewsets.ModelViewSet):

    queryset = ToDoModel.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsOrganizationUserOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return TodoSerializer
        return TodoSerializer

    def get_queryset(self):
        if hasattr(self.request.user, "profilemodel"):
            return ToDoModel.objects.filter(organization=self.request.user.profilemodel.active_organization)

        return ToDoModel.objects.filter(organization=None)

    def handle_exception(self, exc):
        data = {
            "error": str(exc)
        }
        return Response(data)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        org = user.profilemodel.active_organization if hasattr(user, "profilemodel") else None
        serializer.save(create_user=creator, organization=org)
