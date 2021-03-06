from rest_framework import serializers


from homework.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer


class HomeWorkSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = HomeWork
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class AttachedFIleSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = AttachedFIle
        fields = '__all__'


class SubmitSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Submit
        fields = '__all__'


class SubmitFileSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = SubmitFile
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'