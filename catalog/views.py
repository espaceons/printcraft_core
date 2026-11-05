# catalog/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import PaperType, PaperWeight, BindingType
from .forms import PaperTypeForm, PaperWeightForm, BindingTypeForm

# ==========================================
# 1. CRUD : TYPES DE PAPIER (PaperType)
# ==========================================

class PaperTypeListView(ListView):
    model = PaperType
    template_name = 'catalog/papertype_list.html'
    context_object_name = 'paper_types'

class PaperTypeCreateView(CreateView):
    model = PaperType
    form_class = PaperTypeForm
    template_name = 'catalog/form_generic.html'
    success_url = reverse_lazy('catalog:papertype_list')

    def form_valid(self, form):
        messages.success(self.request, "Type de papier ajouté avec succès.")
        return super().form_valid(form)

class PaperTypeUpdateView(UpdateView):
    model = PaperType
    form_class = PaperTypeForm
    template_name = 'catalog/form_generic.html'
    success_url = reverse_lazy('catalog:papertype_list')

    def form_valid(self, form):
        messages.success(self.request, "Type de papier mis à jour.")
        return super().form_valid(form)

class PaperTypeDeleteView(DeleteView):
    model = PaperType
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('catalog:papertype_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Type de papier supprimé.")
        return super().delete(request, *args, **kwargs)

# ==========================================
# 2. CRUD : GRAMMAGES (PaperWeight)
# ==========================================

class PaperWeightListView(ListView):
    model = PaperWeight
    template_name = 'catalog/paperweight_list.html'
    context_object_name = 'paper_weights'
    queryset = PaperWeight.objects.select_related('paper_type').all()

class PaperWeightCreateView(CreateView):
    model = PaperWeight
    form_class = PaperWeightForm
    template_name = 'catalog/form_generic.html'
    success_url = reverse_lazy('catalog:paperweight_list')

class PaperWeightUpdateView(UpdateView):
    model = PaperWeight
    form_class = PaperWeightForm
    template_name = 'catalog/form_generic.html'
    success_url = reverse_lazy('catalog:paperweight_list')

class PaperWeightDeleteView(DeleteView):
    model = PaperWeight
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('catalog:paperweight_list')

# ==========================================
# 3. CRUD : RELIURES (BindingType)
# ==========================================

class BindingTypeListView(ListView):
    model = BindingType
    template_name = 'catalog/bindingtype_list.html'
    context_object_name = 'bindings'

class BindingTypeCreateView(CreateView):
    model = BindingType
    form_class = BindingTypeForm
    template_name = 'catalog/form_generic.html'
    success_url = reverse_lazy('catalog:bindingtype_list')

class BindingTypeUpdateView(UpdateView):
    model = BindingType
    form_class = BindingTypeForm
    template_name = 'catalog/form_generic.html'
    success_url = reverse_lazy('catalog:bindingtype_list')

class BindingTypeDeleteView(DeleteView):
    model = BindingType
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('catalog:bindingtype_list')