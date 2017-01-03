from django import forms

TYPE_CHOICES = (('1', 'Garsonka, 1-Izbovy'), ('2', '2-Izbovy'), ('3', '3-Izbovy'), ('4', '4+-Izbovy'), ('5', 'Dom'), ('6', 'Pozemok'))
CITY_LIST = (('0', 'Senica'), ('1', 'Skalica'))


class AdvertFilterForm(forms.Form):
    city = forms.ChoiceField(choices=CITY_LIST, required=False)
    estate_type = forms.MultipleChoiceField(choices=TYPE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
