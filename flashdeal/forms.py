from django import forms


class AddLogNoteForm(forms.Form):

    note = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text='Add reason for your decision if you have one'
    )

