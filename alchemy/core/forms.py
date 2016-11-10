from django import forms
from .models import Item, Account


class CraftingForm(forms.Form):

    item1 = forms.ModelChoiceField(
        required=True, queryset=None,
    )

    item2 = forms.ModelChoiceField(
        required=True, queryset=None,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        qs = Item.objects.filter(
            pk__in=Account.objects.filter(user=user, credit__gte=1).values_list('item')
        )
        super(CraftingForm, self).__init__(*args, **kwargs)
        self.fields['item1'].queryset = qs
        self.fields['item2'].queryset = qs


class MiningForm(forms.Form):

    user = forms.ModelChoiceField(
        required=True, queryset=None,
    )

    item = forms.ModelChoiceField(
        required=True, queryset=None,
    )

    amount = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        items = kwargs.pop('items')
        users = kwargs.pop('users')
        super(MiningForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = items
        self.fields['user'].queryset = users


