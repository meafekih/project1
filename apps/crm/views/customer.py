from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from apps.crm.schemas.customer import Customer , CustomerForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/upload.html'
    success_url = reverse_lazy('home')

class CustomerListView(ListView):
    model = Customer
    template_name = 'crm/download.html'
    context_object_name = 'customers'

def download(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    response = HttpResponse(customer.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{customer.document.name}"'
    return response