from django.apps import apps
from django.conf import settings

PAPERCLIP_ENABLE_VIDEO = getattr(settings, 'PAPERCLIP_ENABLE_VIDEO', False)
PAPERCLIP_ENABLE_LINK = getattr(settings, 'PAPERCLIP_ENABLE_LINK', False)
PAPERCLIP_ACTION_HISTORY_ENABLED = getattr(settings, 'PAPERCLIP_ACTION_HISTORY_ENABLED', True)
PAPERCLIP_FILETYPE_MODEL = settings.PAPERCLIP_FILETYPE_MODEL
PAPERCLIP_ATTACHMENT_MODEL = settings.PAPERCLIP_ATTACHMENT_MODEL


def get_filetype_model():
    return apps.get_model(*PAPERCLIP_FILETYPE_MODEL.split('.'))


def get_attachment_model():
    return apps.get_model(*PAPERCLIP_ATTACHMENT_MODEL.split('.'))


def get_attachment_permission(action):
    model = get_attachment_model()
    return '{app}.{action}'.format(app=model._meta.app_label, action=action)
