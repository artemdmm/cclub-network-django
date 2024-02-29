from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sent_by', 'body', 'created_at']
        read_only_fields = ['id', 'created_at']

