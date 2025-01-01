from django import forms

# Custom way to set css styling on a form field in python code
def field_style():
     styles_string = ' '

     # List of what you want to add to style the field
     styles_list = [
          'height: 160px;',
     ]

     # Converting the list to a string 
     styles_string = styles_string.join(styles_list)
     # or
     # styles_string = ' '.join(styles_list)
     return styles_string

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Your Name", 'name':'name', 'id':'name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Your Email", 'name':'email', 'id':'email'}))

    #name = forms.CharField(max_length=100, attrs={'class': 'form-control'})
    #email = forms.EmailField()
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Subject", 'name':'subject', 'id':'subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': "Message!", 'name':'message', 'id':'message', 'style': field_style()}))