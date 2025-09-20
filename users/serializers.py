from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'address','profile_picture']
        read_only_fields = ['role','join_date','last_active','updated_at','created_at','profile_picture_url','id']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'first_name',
                  'last_name', 'address', 'phone_number', 'role','profile_picture','profile_picture_url','join_date','last_active','updated_at','created_at']
        read_only_fields = ['id','role','profile_picture_url','join_date','last_active','updated_at','created_at']



class UserSimpleSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'first_name',
                  'last_name','profile_picture','profile_picture_url' ]
        read_only_fields = ['id', 'email', 'first_name',
                  'last_name','profile_picture','profile_picture_url']