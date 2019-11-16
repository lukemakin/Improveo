from django import forms
from django.shortcuts import get_object_or_404
from .models import Report, ProblemReported
from products.models import Product
from areas.models import ProductionLine
import datetime


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        exclude = ('user', 'production_line',)

    def __init__(self, *args, **kwargs):
        production_line = kwargs.pop('production_line', None)
        super().__init__(*args, **kwargs)
        if production_line is not None:
            line = get_object_or_404(ProductionLine, name=production_line)
            self.fields['product'].queryset = line.products.all()


class ProblemReportedForm(forms.ModelForm):

    class Meta:
        model = ProblemReported
        # fields = "__all__"
        exclude = ('solved', 'user', 'report', 'problem_id')


class ReportResultForm(forms.Form):

    production_line = forms.ModelChoiceField(
        queryset=ProductionLine.objects.all())
    day = forms.CharField(widget=forms.DateTimeInput(
        attrs={'class': 'datepicker'}))


class ReportSelectLineForm(forms.Form):

    production_line = forms.ModelChoiceField(
        queryset=ProductionLine.objects.none())
    # widget=forms.Select(attrs={'id': 'prod_line'})

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['production_line'].queryset = ProductionLine.objects.filter(
            team_leader__user__username=user)
