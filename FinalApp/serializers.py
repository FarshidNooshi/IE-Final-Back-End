from rest_framework import serializers

from FinalApp.models import User, Webpage, Alarm, ExpiredToken, Result


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'


class ExpiredTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiredToken
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['webpage', 'status_code', 'date', 'error']


class WebpageSerializer(serializers.ModelSerializer):
    alarms = AlarmSerializer(many=True, read_only=True)
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = Webpage
        fields = ['url', 'active', 'max_error', 'alarms', 'results']
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    webpages = WebpageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username', 'webpages']
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True},
            'Webpages': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.password = password
        instance.save()
        return instance
