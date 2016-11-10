from django.db import transaction
from django.db.models import F

from . import models


def perform_crafting(user, item1, item2):
    # Debit input resources
    if(item1 == item2):
        success = _update_account(user, item1, -2)
        if not success:
            return False
    else:
        with transaction.atomic():
            qs = models.Account.objects.filter(
                item__in=(item1, item2), user=user, credit__gte=1
            )
            if qs.count() < 2:
                _insufficient_resources(user)
                return False
            updated = qs.update(
                credit=F('credit')-1
            )
            if updated != 2:
                transaction.rollback()
                return False

    # Check for rule
    rules = models.Rule.objects.filter(input1=item1, input2=item2)
    if rules.count() == 0:
        rules = models.Rule.objects.filter(input1=item2, input2=item1)
    if rules.count() == 0:
        models.LogItem.objects.create(
            user=user,
            type='crafting',
            text=(
                'Používateľ %s sa neúspešne pokúsil o kombináciu %s a %s.'
                % (user, item1, item2)
            )
        )
        return False
    rule = rules[0]

    # Kredit output resources
    _update_account(user, rule.result, 1)
    models.LogItem.objects.create(
        user=user,
        type='crafting',
        text=(
            'Používateľ %s úspešne skombinoval %s a %s, pričom dostal %s.'
            % (user, item1, item2, rule.result)
        )
    )
    return True


def perform_mining(user, item, diff):
    success = _update_account(user, item, diff)
    if success:
        models.LogItem.objects.create(
            user=user,
            type='crafting',
            text=(
                'Používateľ %s úspešne vyťažil %s v množstve %d.'
                % (user, item, diff)
            )
        )
    return success


def _update_account(user, item, diff):
    models.Account.objects.get_or_create(
        user=user, item=item, defaults={'credit': 0}
    )
    updated = models.Account.objects.filter(
        item=item, user=user, credit__gte=-diff
    ).update(
        credit=F('credit') + diff
    )
    if updated == 0:
        _insufficient_resources(user)
        return False
    return True


def _insufficient_resources(user):
    models.LogItem.objects.create(
        user=user,
        type='error',
        text=(
            'Používateľ %s nemá dostatok surovín na vykonanie operácie.'
            % (user)
        )
    )
