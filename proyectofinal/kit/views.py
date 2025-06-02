from django.shortcuts import get_object_or_404, redirect
from django.views.generic import list, edit, detail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Kit, SolarPanel, ChargeController
from .forms import KitForm, PanelForm, ControllerForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class KitListView(list.ListView):
    model = Kit
    template_name = 'kit/kit_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kits'] = self.request.user.equipos_solares.all()
        return context
    
@method_decorator(login_required, name='dispatch')
class KitDetailView(detail.DetailView):
    model = Kit
    model2 = SolarPanel
    model3 = ChargeController
    template_name = 'kit/kit_detail.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Kit, id=self.kwargs['kit_id'], user=self.request.user)
    
@method_decorator(login_required, name='dispatch')
class KitCreateView(edit.CreateView):
    form_class= KitForm
    success_url = '/kit'
    template_name = 'kit/kit_create.html'

    def form_valid(self, form):
        kit = form.save(commit=False)
        kit.user = self.request.user
        kit.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class PanelCreateView(edit.CreateView):
    form_class= PanelForm
    template_name = 'kit/panel_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        self.success_url = f'/kit/{self.kit_id}/'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kit'] = get_object_or_404(Kit, id=self.kwargs.get('kit_id'), user=self.request.user)
        return context

    def form_valid(self, form):
        kit_id = self.kwargs.get('kit_id')
        kit = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        panel = form.save(commit=False)
        panel.kit = kit
        panel.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class ControllerCreateView(edit.CreateView):
    form_class= ControllerForm
    template_name = 'kit/controller_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        self.success_url = f'/kit/{self.kit_id}/'
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kit'] = get_object_or_404(Kit, id=self.kwargs.get('kit_id'), user=self.request.user)
        return context

    def form_valid(self, form):
        kit_id = self.kwargs.get('kit_id')
        kit = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        controller = form.save(commit=False)
        controller.kit = kit
        controller.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class KitUpdateView(edit.UpdateView):
    form_class= KitForm
    template_name = 'kit/kit_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Kit, id=self.kwargs['kit_id'], user=self.request.user)
    
    def get_success_url(self):
        return f'/kit/{self.kwargs["kit_id"]}/'
    
@method_decorator(login_required, name='dispatch')
class PanelUpdateView(edit.UpdateView):
    form_class= PanelForm
    template_name = 'kit/panel_update.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        self.success_url = f'/kit/{self.kit_id}/'
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kit'] = get_object_or_404(Kit, id=self.kwargs.get('kit_id'), user=self.request.user)
        context['panel'] = get_object_or_404(SolarPanel, id=self.kwargs.get('panel_id'), kit__user=self.request.user)
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(SolarPanel, id=self.kwargs['panel_id'], kit__user=self.request.user)
    
@method_decorator(login_required, name='dispatch')
class ControllerUpdateView(edit.UpdateView):
    form_class= ControllerForm
    template_name = 'kit/controller_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        self.success_url = f'/kit/{self.kit_id}/'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kit'] = get_object_or_404(Kit, id=self.kwargs.get('kit_id'), user=self.request.user)
        context['controller'] = get_object_or_404(ChargeController, id=self.kwargs.get('controller_id'), kit__user=self.request.user)
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(ChargeController, id=self.kwargs['controller_id'], kit__user=self.request.user)
    
@method_decorator(login_required, name='dispatch')
class KitDeleteView(edit.DeleteView):
    model = Kit
    template_name = 'kit/kit_delete.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Kit, id=self.kwargs['kit_id'], user=self.request.user)
    
    def get_success_url(self):
        return '/kit/'
    
@method_decorator(login_required, name='dispatch')
class PanelDeleteView(edit.DeleteView):
    model = SolarPanel
    template_name = 'kit/panel_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        self.panel_id = self.kwargs.get('panel_id')
        self.success_url = f'/kit/{self.kit_id}/'
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return get_object_or_404(SolarPanel, id=self.kwargs['panel_id'], kit__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kit'] = get_object_or_404(Kit, id=self.kwargs.get('kit_id'), user=self.request.user)
        context['panel'] = get_object_or_404(SolarPanel, id=self.kwargs.get('panel_id'), kit__user=self.request.user)
        return context
    
@method_decorator(login_required, name='dispatch')
class ControllerDeleteView(edit.DeleteView):
    model = ChargeController
    template_name = 'kit/controller_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        self.controller_id = self.kwargs.get('controller_id')
        self.success_url = f'/kit/{self.kit_id}/'
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return get_object_or_404(ChargeController, id=self.kwargs['controller_id'], kit__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kit'] = get_object_or_404(Kit, id=self.kwargs.get('kit_id'), user=self.request.user)
        context['controller'] = get_object_or_404(ChargeController, id=self.kwargs.get('controller_id'), kit__user=self.request.user)
        return context