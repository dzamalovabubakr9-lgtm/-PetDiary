from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from care.forms import ProcedureForm
from care.models import Procedure, ProcedureLog


class ProceduresListView(LoginRequiredMixin, ListView):
    model = Procedure
    template_name = 'care/procedures.html'
    context_object_name = 'procedures'
    paginate_by = 20

    def get_queryset(self):
        return Procedure.objects.filter(pet__owner=self.request.user).order_by('scheduled_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming'] = (
            Procedure.objects.filter(pet__owner=self.request.user, done=False).order_by('scheduled_date')[:5]
        )
        return context


class ProcedureDetailView(LoginRequiredMixin, DetailView):
    model = Procedure
    template_name = 'care/procedure_detail.html'
    context_object_name = 'procedure'

    def get_queryset(self):
        return Procedure.objects.filter(pet__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = ProcedureLog.objects.filter(procedure=self.object).order_by('-done_date')
        return context


class ProcedureCreateView(LoginRequiredMixin, CreateView):
    model = Procedure
    template_name = 'care/procedure_form.html'
    form_class = ProcedureForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.instance.pet.owner_id != self.request.user.id:
            form.add_error('pet', 'Выберите своего питомца.')
            return self.form_invalid(form)
        response = super().form_valid(form)
        messages.success(self.request, f'Процедура «{form.instance.get_name_display()}» успешно добавлена.')
        return response

    def get_success_url(self):
        return reverse_lazy('care:procedures')


class ProcedureUpdateView(LoginRequiredMixin, UpdateView):
    model = Procedure
    template_name = 'care/procedure_form.html'
    form_class = ProcedureForm
    context_object_name = 'procedure'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Procedure.objects.filter(pet__owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Процедура «{form.instance.get_name_display()}» успешно обновлена.')
        return response

    def get_success_url(self):
        return reverse_lazy('care:procedures')


class ProcedureDeleteView(LoginRequiredMixin, DeleteView):
    model = Procedure
    template_name = 'care/procedure_confirm_delete.html'
    context_object_name = 'procedure'
    success_url = reverse_lazy('care:procedures')

    def get_queryset(self):
        return Procedure.objects.filter(pet__owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.get_name_display()
        self.object.delete()
        messages.success(request, f'Процедура «{name}» удалена.')
        return HttpResponseRedirect(self.get_success_url())
