from rest_framework import serializers

from .models import ProfileModel, OrganizationModel, ToDoModel


class TodoSerializer(serializers.ModelSerializer):

    create_user = serializers.ReadOnlyField(source='create_user.username')
    organization = serializers.ReadOnlyField(source='organization.name')

    class Meta:
        model = ToDoModel
        fields = (
            'id', 'title', 'content', 'date',
            'create_user', 'organization',
        )


class UserSerializer(serializers.ModelSerializer):

    organizations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=OrganizationModel.objects.all()
    )

    active_organization = serializers.ReadOnlyField(source='creator.name')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ProfileModel
        fields = ('id', 'username', 'active_organization')


class OrganizationSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = OrganizationModel
        fields = ('id', 'name', 'date')
