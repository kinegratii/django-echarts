from django import forms


class ParamsForm:
    name = forms.CharField(label='Name', required=True, max_length=200)
    params_dic = forms.JSONField(label='Params(JSON)', max_length=500)
