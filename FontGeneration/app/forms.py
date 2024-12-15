from django import forms


class FontGenerationForm(forms.Form):
    image_file = forms.ImageField(label="Upload Image File")
    threshold_value = forms.IntegerField(initial=200)
    ascent = forms.IntegerField(initial=800)
    descent = forms.IntegerField(initial=200)
    em = forms.IntegerField(initial=1000)
    encoding = forms.CharField(initial="UnicodeFull")
    lang = forms.CharField(initial="English (US)")
    filename = forms.CharField(initial="MyFont")
    style = forms.CharField(initial="Regular")
    copyright = forms.CharField(initial="Nobody")
