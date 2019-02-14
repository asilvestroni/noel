# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

from django import forms

ERRORS = {
    'required': 'Campo obbligatorio',
    'invalid': 'Valore non valido',
}


class UploadPicsForm(forms.Form):
    """
    Form for picture uploading on the index page
    """
    # TODO: check for multiple pictures
    pics = forms.FileField(label="Immagini", required=True,
                           widget=forms.ClearableFileInput(attrs={'multiple': True, 'data-max-files': 30}),
                           error_messages=ERRORS)
