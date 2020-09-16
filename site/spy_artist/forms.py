from django import forms

class InputForm(forms.Form):
       input1 = forms.CharField(label='Artist name')