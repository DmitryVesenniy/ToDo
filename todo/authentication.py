from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status

from .models import OrganizationModel


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, write_only=True)
    organization = serializers.MultipleChoiceField(required=True, choices=sorted([
                                                        (p.id, p.name) for p in OrganizationModel.objects.all()
                                                    ]))
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password1'])
        user.save()

        orgs = OrganizationModel.objects.filter(pk__in=self.organization)
        user.profilemodel.organizations.add(orgs)

        user.save()
        return user


class Registration(APIView):

    def get(self, request, format=None):
        serializer = RegisterSerializer()
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    organization = request.data.get("org")

    user = authenticate(email=email, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    try:
        org = OrganizationModel.objets.get(name=organization)

    except OrganizationModel.DoesNotExist:
        org = None

    if org and org not in user.profilemodel.organizations:
        return Response({"error": "permission danied"}, status=HTTP_401_UNAUTHORIZED)

    user.profilemodel.active_organization = org
    user.save()

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})
