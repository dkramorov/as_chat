from ajax_select import register, LookupChannel
from fastapi_core.filtering import ServiceFiltering
from as_admin.lookup_abstract import format_item_display
from as_chat.models import Conversation, ConversationMessage


#@register('conversation')
class ConversationLookup(LookupChannel):

    model = Conversation

    def get_query(self, q, request):
        query = '[id__icontains={q}]'
        if q and q.isdigit():
            query += ' OR [id={q}]'
        return ServiceFiltering(query.format(q=q), True).apply(self.model.objects.all())

    def format_item_display(self, item):
        return format_item_display(self, item)


#@register('conversation_message')
class ConversationLookup(LookupChannel):

    model = ConversationMessage

    def get_query(self, q, request):
        query = '[id__icontains={q}]'
        if q and q.isdigit():
            query += ' OR [id={q}]'
        return ServiceFiltering(query.format(q=q), True).apply(self.model.objects.all())

    def format_item_display(self, item):
        return format_item_display(self, item)
