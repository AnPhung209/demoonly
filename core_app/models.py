import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField
from pgvector.django import VectorField
from django.utils import timezone
from import_export import resources
# Create your models here.

# create a array that have dimension of 1536
empty_vector = [0.0]*1536


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_index=True)

    class Meta:
        abstract = True


# expose
class SystemPrompt(CommonModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt_name = models.CharField(max_length=100, unique=True)
    prompt_content = models.TextField()

    def __str__(self):
        return self.prompt_name


class AgentTool(CommonModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool_name = models.CharField(max_length=100)
    args_schema = ArrayField(models.JSONField(default=dict, null=True, blank=True), default=list, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.tool_name}"

class Agent(CommonModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_name = models.CharField(max_length=100)
    llm = models.CharField(max_length=100)
    prompt = models.ForeignKey(SystemPrompt, on_delete=models.DO_NOTHING)
    tools = ArrayField(models.CharField(max_length=100), default=list, null=True, blank=True)

    def __str__(self):
        return self.agent_name
# expose
class Conversation(CommonModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    chat_history = ArrayField(models.JSONField(), default=list, null=True, blank=True)
    meta_data = models.JSONField(default=dict, null=True, blank=True) # tool id

    def __str__(self):
        return f"{self.id} - with agent: {self.agent.agent_name}"

class ExternalKnowledge(CommonModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField()
    title_embedding = VectorField(dimensions=1536, default=empty_vector)
    content_embedding = VectorField(dimensions=1536, default=empty_vector)

    def __str__(self):
        return f"{self.title}"

class Product(CommonModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.IntegerField()

