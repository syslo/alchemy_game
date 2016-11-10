from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from . import forms
from . import models
from . import logic


@login_required
def crafting(request):
    if request.method == 'POST':
        form = forms.CraftingForm(
            request.POST, prefix='crafting', user=request.user,
        )
        if form.is_valid():
            logic.perform_crafting(
                request.user,
                form.cleaned_data['item1'],
                form.cleaned_data['item2'],
            )
            form = forms.CraftingForm(
                prefix='crafting', user=request.user,
            )
    else:
        form = forms.CraftingForm(
            prefix='crafting', user=request.user,
        )

    context = {
        'form': form,
        'accounts': (
            models.Account.objects
            .filter(user=request.user)
            .select_related('item')
            .order_by('item__name')
        )
    }

    return render(request, 'alchemy/crafting.html', context)


@staff_member_required
def mining(request):
    users = get_user_model().objects.all()
    items = models.Item.objects.all()

    if request.method == 'POST':
        form = forms.MiningForm(
            request.POST, prefix='mining', users=users, items=items,
        )
        if form.is_valid():
            logic.perform_mining(
                form.cleaned_data['user'],
                form.cleaned_data['item'],
                form.cleaned_data['amount'],
            )
            form = forms.MiningForm(
                prefix='mining', users=users, items=items,
            )
    else:
        form = forms.MiningForm(
            prefix='mining', users=users, items=items,
        )

    context = {
        'form': form,
    }

    return render(request, 'alchemy/mining.html', context)
