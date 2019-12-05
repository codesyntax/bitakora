from django import forms
from bitakora.ikasbloga.models import School
from bitakora.ikasbloga.models import Room


class SchoolForm(forms.ModelForm):

    class Meta:
        model = School
        fields = [
            "desc",
        ]


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = [
            "name",
            "year",
            "level"
        ]