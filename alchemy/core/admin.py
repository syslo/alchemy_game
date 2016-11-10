from django.contrib import admin
from easy_select2 import select2_modelform

from . import models


ItemForm = select2_modelform(models.Item)


class ItemAdmin(admin.ModelAdmin):
    form = ItemForm

admin.site.register(models.Item, ItemAdmin)


RuleForm = select2_modelform(models.Rule)


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm

admin.site.register(models.Rule, RuleAdmin)


AccountForm = select2_modelform(models.Account)


class AccountAdmin(admin.ModelAdmin):
    form = AccountForm

admin.site.register(models.Account, AccountAdmin)


LogItemForm = select2_modelform(models.LogItem)


class LogItemAdmin(admin.ModelAdmin):
    form = LogItemForm

admin.site.register(models.LogItem, LogItemAdmin)

