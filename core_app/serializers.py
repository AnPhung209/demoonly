from rest_framework import serializers
from .models import Conversation, SystemPrompt, ExternalKnowledge, Agent, AgentTool

class ConversationSerializer(serializers.ModelSerializer):
    chat_history = serializers.ListField(child=serializers.DictField(), required=False, allow_empty=True)
    class Meta:
        model = Conversation
        fields = '__all__'

class SystemPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = '__all__'

class ExternalKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalKnowledge
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
        
class AgentToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentTool
        fields = '__all__'