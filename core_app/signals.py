from django.db.models.signals import post_save
from django.dispatch import receiver
from core_app.models import ExternalKnowledge
from core_app.embedding.embedding_by_openai import get_vector_from_embedding

# Sử dụng một biến toàn cục để theo dõi 
updating_embedding = False

@receiver(post_save, sender=ExternalKnowledge)
def update_content_embedding(sender, instance, **kwargs):
    global updating_embedding

    if updating_embedding:
        return

    if isinstance(instance, ExternalKnowledge):
        if instance.content:
            text_content = instance.content
            embedding = get_vector_from_embedding(text_content)
            instance.content_embedding = embedding

    # Save the instance and avoid recursion
    try:
        updating_embedding = True
        instance.save()
    finally:
        updating_embedding = False
