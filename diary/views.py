from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from diary.forms import DiaryEntryForm
from diary.models import DiaryEntry, VetVisit
from pets.models import Pet


class DiaryListView(LoginRequiredMixin, ListView):
    """Список записей дневника текущего пользователя."""
    model = DiaryEntry
    template_name = 'diary/diary_list.html'
    context_object_name = 'entries'
    paginate_by = 20

    def get_queryset(self):
        return DiaryEntry.objects.filter(pet__owner=self.request.user).order_by('-date')


class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = DiaryEntry
    template_name = 'diary/diary_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return DiaryEntry.objects.filter(pet__owner=self.request.user)


class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = DiaryEntry
    template_name = 'diary/diary_form.html'
    form_class = DiaryEntryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.instance.pet.owner_id != self.request.user.id:
            form.add_error('pet', 'Выберите своего питомца.')
            return self.form_invalid(form)
        response = super().form_valid(form)
        messages.success(self.request, f'Запись «{form.instance.title}» успешно добавлена.')
        return response

    def get_success_url(self):
        return reverse_lazy('diary:diary_list')


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    model = DiaryEntry
    template_name = 'diary/diary_form.html'
    form_class = DiaryEntryForm
    context_object_name = 'entry'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return DiaryEntry.objects.filter(pet__owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Запись «{form.instance.title}» успешно обновлена.')
        return response

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.object.pk})


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    model = DiaryEntry
    template_name = 'diary/diary_confirm_delete.html'
    context_object_name = 'entry'
    success_url = reverse_lazy('diary:diary_list')

    def get_queryset(self):
        return DiaryEntry.objects.filter(pet__owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.title
        self.object.delete()
        messages.success(request, f'Запись «{title}» удалена.')
        return HttpResponseRedirect(self.get_success_url())
