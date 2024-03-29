from rest_framework import serializers
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


from authentication.models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', "first_name", "last_name","groups")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )


class RegisterSerializer(serializers.ModelSerializer):
    '''
    Register user include data{
        username, password, email, first_name, last_name
    }
    '''
    username = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    birth_date = serializers.DateField(required=False)
    avatar = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender',
                  'password', 'avatar', 'birth_date']

    def validate(self, data):
        try:
            user = User.objects.filter(username=data.get('username'))
            if len(user) > 0:
                raise serializers.ValidationError(_("Username already exists"))
        except User.DoesNotExist:
            pass

        if not data.get('password'):
            raise serializers.ValidationError(_("Empty Password"))

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    # avatar = serializers.CharField(required=False)
    group_id = serializers.CharField(required=False)

    # def get_avatar(self, obj):
    #     request = self.context['request']
    #     if obj.avatar and not obj.avatar.name.startswith("/static"):

    #         path = '/static/%s' % obj.avatar.name

    #         return request.build_absolute_uri(path)

    def create(self, validated_data):
        data = validated_data.copy()
        groups_id = data.pop('group_id').split(',')
        print(groups_id)
        user = User(**data)
        user.set_password(user.password)
        user.save()
        for group_id in groups_id:
            print(group_id)
            group = Group.objects.get(id=group_id)
            user.groups.add(group)

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'group_id',
                  'avatar', 'gender', 'groups']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'groups': {
                'read_only': True
            }
        }
