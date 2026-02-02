import datetime
import json
import os
import logging
import re
import traceback

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from fastapi_core.models_abstract import JsonApiMixin
from as_admin.models_abstract import AbstractDateTimeModel, AbstractShortDateTimeModel


logger = logging.getLogger()


"""
Должна быть сущность по которой будет беседа (например, заказ)
расширение моделей для чатов
"""


class Conversation(JsonApiMixin, AbstractDateTimeModel):
    """Беседа
    """
    conversation_choices = (
        (1, 'Чат по продукту'),
        (2, 'Чат по заказу'),
    )
    conversation_type = models.IntegerField(blank=True, null=True, db_index=True,
        choices=conversation_choices,
        verbose_name='Тип беседы')

    class Meta:
        abstract = True
        verbose_name = 'Беседа'
        verbose_name_plural = 'Беседы'

    def get_name(self):
        return '#%s, %s' % (self.id, self.get_conversation_type_display())

    def __str__(self):
        return self.get_name()

    @cached_property
    def get_conversation_type(self) -> dict:
        if not self.conversation_type:
            return {}
        return {
            'id': self.conversation_type,
            'name': self.get_conversation_type_display(),
        }

    @cached_property
    def get_conversation(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'conversation_type': self.get_conversation_type,
        }


class ConversationUser(JsonApiMixin):
    """Пользователи участвующие в беседе
    """
    conversation = models.ForeignKey(Conversation, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Беседа')

    class Meta:
        abstract = True
        verbose_name = 'Участник беседы'
        verbose_name_plural = 'Участники бесед'

    def get_name(self):
        return 'id=%s, conversation_id=%s' % (self.id, self.conversation_id)

    def __str__(self):
        return self.get_name()


class ConversationMessage(JsonApiMixin, AbstractDateTimeModel):
    """Сообщения в чат
    """
    conversation = models.ForeignKey(Conversation, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Беседа')
    text = models.TextField(blank=True, null=True, verbose_name='Сообщение')

    class Meta:
        abstract = True
        verbose_name = 'Сообщение беседы'
        verbose_name_plural = 'Сообщения по беседам'

    def get_name(self):
        return 'id=%s, %s' % (self.id, self.text)

    def __str__(self):
        return self.get_name()

    def delete(self, *args, **kwargs):
        """Удаление сообщения беседы
        """
        super(ConversationMessage, self).delete(*args, **kwargs)

    @staticmethod
    def only_fields():
        """Поля для маршрутов
           для функции object_fields
        """
        return (
            'id',
            'text',
            'created_at',
            'updated_at',
        )

    def get_conversation(self) -> dict:
        """Получение беседы по сообщению"""
        if not self.conversation_id:
            return {}
        return self.conversation.get_conversation


class ConversationMessageState(JsonApiMixin):
    """Состояние сообщения
    """
    state_choices = (
        (1, 'Не прочитано'),
        (2, 'Прочитано'),
    )
    conversation_message = models.ForeignKey(ConversationMessage, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Сообщение')
    state = models.IntegerField(blank=True, null=True, db_index=True,
        choices=state_choices,
        verbose_name='Состояние')

    class Meta:
        abstract = True
        verbose_name = 'Состояние сообщения'
        verbose_name_plural = 'Состояния сообщений'

    def get_name(self):
        return 'id=%s, %s' % (self.id, self.get_state_display())

    def __str__(self):
        return self.get_name()
