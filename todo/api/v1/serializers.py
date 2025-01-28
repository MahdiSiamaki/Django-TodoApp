from django.template.context_processors import request
from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    user= serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'description', 'due_date', 'done', 'created_at', 'updated_at']

    def to_representation(self, instance):
        request= self.context.get('request')
        data= super().to_representation(instance)
        if not request.parser_context['kwargs'].get('pk'):
            data.pop('description')
            data.pop('created_at')
            data.pop('updated_at')
        data['done']= 'Yes' if data['done'] else 'No'

        return data