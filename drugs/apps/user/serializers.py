from rest_framework import serializers

from apps.user.models import User


# # 保存用户基本信息
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # 指定字段
        # fields = ['id', 'username', 'mobile', 'email', 'password']
        # username 增加1长度限制，passwordz增加只写
        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 1
            },
            'password': {
                'max_length': 20,
                'min_length': 2,
                'write_only': True,
                'required': False
            },
            'mobile': {
                'required': False,
            }

        }
