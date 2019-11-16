from django.shortcuts import render, redirect, get_object_or_404
from .models import Report, ProblemReported
from .forms import ReportForm, ProblemReportedForm, ReportResultForm, ReportSelectLineForm
# from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from areas.models import ProductionLine
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import Http404


class HomeView(FormView):
    template_name = 'reports/home.html'
    form_class = ReportSelectLineForm
    # login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, *args, **kwargs):
        prod_line = self.request.POST.get("prod_line")
        return redirect('reports:rvp', production_line=prod_line)


class SelectView(LoginRequiredMixin, FormView):
    template_name = 'reports/select.html'
    form_class = ReportResultForm
    success_url = reverse_lazy('reports:summary')
    # login_url = '/login/'

    def form_valid(self, form):
        self.request.session['day'] = self.request.POST.get('day', None)
        self.request.session['line'] = self.request.POST.get('production_line', None)
        return super(SelectView, self).form_valid(form)


@login_required
def main_report_summary(request):
    try:
        day = request.session.get('day', None)
        line = request.session.get('line', None)

        queryset_plan = Report.objects.filter_by_day(
            day).aggregate_plan()['plan__sum']
        queryset_execution = Report.objects.filter_by_day(
            day).aggregate_execution()['execution__sum']
        queryset_pr = ProblemReported.objects.problem_reported_by_day(day, line)

        context = {
            "plan": queryset_plan,
            "execution": queryset_execution,
            "problems_reported": queryset_pr,
            "day": day,
        }
    except:
        pass

    return render(request, 'reports/main.html', context)


@login_required
def report_view(request, production_line):
    form = ReportForm(request.POST or None, production_line=production_line)
    pform = ProblemReportedForm(request.POST or None)
    queryset = Report.objects.filter(production_line__name=production_line)
    # line = ProductionLine.objects.get(name=production_line)
    line = get_object_or_404(ProductionLine, name=production_line)

    if 'submitbtn1' in request.POST:
        if form.is_valid():
            print('tu')
            obj = form.save(commit=False)
            obj.user = request.user
            obj.production_line = line
            obj.save()
            print(request.POST)
            # pform = ProblemReportedForm()
            # form = ReportForm()
            return redirect(request.META.get('HTTP_REFERER'))
    elif 'submitbtn2' in request.POST:
        r_id = request.POST.get("report_id")
        report = Report.objects.get(id=r_id)
        print(report)
        print(pform.is_valid())
        if pform.is_valid():
            obj = pform.save(commit=False)
            obj.user = request.user
            obj.report = report
            obj.save()
            print(r_id)
            print(request.POST)
            # form = ReportForm()
            return redirect(request.META.get('HTTP_REFERER'))
    

    context = {
        'form': form,
        'pform': pform,
        'object_list': queryset,

    }

    return render(request, 'reports/report.html', context)


@login_required
def delete_view(request, *args, **kwargs):
    r_id = kwargs.get('pk')
    obj = Report.objects.get(id=r_id)
    obj.delete()
    return redirect(request.META.get('HTTP_REFERER'))


class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update.html'

    def get_success_url(self):
        return self.request.path


def generate_problems_in_pdf(request):

    problems = ProblemReported.objects.problems_from_today()

    html_string = render_to_string(
        'reports/problems.html', {'problems': problems})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=todays_problem_list.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response
