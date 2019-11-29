from django import forms

class HostRegForm(forms.Form):
    host_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=10)
    meeting_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=500)
    email = forms.EmailField(max_length=100)


class GuestRegForm(forms.Form):
    guest_name = forms.CharField(max_length=100)
    guest_phone = forms.CharField(max_length=10)
    guest_mail = forms.EmailField(max_length=100)
    meeting_id = forms.IntegerField()

class CheckOutForm(forms.Form):
    guest_mail = forms.EmailField(max_length=100)
    token = forms.IntegerField()

class HostDetailsForm(forms.Form):
    host_mail = forms.EmailField(max_length=100)
    token = forms.IntegerField()