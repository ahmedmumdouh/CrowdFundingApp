from django import forms
from .models import ReportComment
from .models import ReportProject


class ReportProjectForm(forms.ModelForm):
    class Meta:
        model = ReportProject
        fields = ('title', 'body_project')


class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = ('title', 'body_comment')
