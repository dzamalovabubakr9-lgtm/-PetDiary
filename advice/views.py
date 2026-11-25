from django.views.generic import DetailView, ListView

from advice.models import Advice, AdviceCategory


class AdviceListView(ListView):
    model = Advice
    template_name = 'advice/advice_list.html'
    context_object_name = 'advice_items'
    paginate_by = 20

    def get_queryset(self):
        return Advice.objects.filter(is_published=True).select_related('category').order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = AdviceCategory.objects.all()
        context['count'] = Advice.objects.filter(is_published=True).count()
        return context


class AdviceDetailView(DetailView):
    model = Advice
    template_name = 'advice/advice_detail.html'
    context_object_name = 'advice_item'

    def get_queryset(self):
        return Advice.objects.filter(is_published=True)
