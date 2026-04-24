from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password1 = serializers.CharField()
    class Meta:
        fields = ['username', 'email', 'password', 'password1']


    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError("Passwords do not match")
        return data