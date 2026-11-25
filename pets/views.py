from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from pets.forms import PetForm
from pets.models import Pet


class PetsListView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'pets/pets_list.html'
    context_object_name = 'pets'
    paginate_by = 12

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = Pet.objects.filter(owner=self.request.user).count()
        return context


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['measurements'] = self.object.measurements.all()
        return context


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    template_name = 'pets/pet_form.html'
    form_class = PetForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Питомец «{form.instance.name}» успешно добавлен.')
        return response

    def get_success_url(self):
        return reverse_lazy('pets:pets_list')


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    template_name = 'pets/pet_form.html'
    form_class = PetForm
    context_object_name = 'pet'

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Информация о питомце «{form.instance.name}» обновлена.')
        return response

    def get_success_url(self):
        return reverse_lazy('pets:pets_detail', kwargs={'pk': self.object.pk})


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet_confirm_delete.html'
    context_object_name = 'pet'
    success_url = reverse_lazy('pets:pets_list')

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        self.object.delete()
        messages.success(request, f'Питомец «{name}» удалён.')
        return HttpResponseRedirect(self.get_success_url())
