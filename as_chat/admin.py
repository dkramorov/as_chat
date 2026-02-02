import os
import logging

from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.urls import path, reverse
from django import forms

from import_export.admin import ImportExportModelAdmin
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline, AjaxSelectAdminStackedInline
from ajax_select import make_ajax_form

from as_admin.admin_abstract import InputFilter

from as_chat.models import (
    Conversation,
    ConversationUser,
    ConversationMessage,
    ConversationMessageState,
)


logger = logging.getLogger()


class ConversationFilter(InputFilter):
    parameter_name = 'conversation_id'
    title = 'Беседа'

    def queryset(self, request, queryset):
        if self.value() is not None:
            conversation_id = self.value()
            return queryset.filter(conversation_id=conversation_id)


class ConversationMessageFilter(InputFilter):
    parameter_name = 'conversation_message_id'
    title = 'Сообщение'

    def queryset(self, request, queryset):
        if self.value() is not None:
            conversation_message_id = self.value()
            return queryset.filter(conversation_message_id=conversation_message_id)


#@admin.register(Conversation)
class ConversationAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in Conversation._meta.fields]
    search_fields = ('id', )
    list_filter = ('conversation_type', )


#@admin.register(ConversationUser)
class ConversationUserAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in ConversationUser._meta.fields]
    search_fields = ('id', )
    list_filter = (
        ConversationFilter,
    )


#@admin.register(ConversationMessage)
class ConversationMessageAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in ConversationMessage._meta.fields]
    search_fields = ('id', )
    list_filter = (
        ConversationFilter,
    )

    #form = make_ajax_form(ConversationMessage, {
    #    'conversation': 'conversation',
    #})


#@admin.register(ConversationMessageState)
class ConversationMessageStateAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in ConversationMessageState._meta.fields]
    search_fields = ('id', )
    list_filter = (
        'state',
        ConversationMessageFilter,
    )

    #form = make_ajax_form(ConversationMessageState, {
    #    'conversation_message': 'conversation_message',
    #})
