from django.contrib import admin
from core_app.models import Conversation, SystemPrompt, ExternalKnowledge, Agent, AgentTool, Product
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

    def before_import(self, dataset, using_transactions = True, dry_run = False):
        pass

# Register your models here.

admin.site.register(Conversation)
admin.site.register(SystemPrompt)
admin.site.register(ExternalKnowledge)
admin.site.register(Agent)
admin.site.register(AgentTool)
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource