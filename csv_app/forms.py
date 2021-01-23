# import the standard Django Forms
# from built-in library
from django import forms


# creating a form
class InputForm(forms.Form):
    search_term = forms.CharField(max_length=200)

