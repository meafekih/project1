from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from apps.crm.schemas.customer import Customer , CustomerForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from apps.base.decorators import Rest_auth_required
from django.http import JsonResponse

""" 
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/upload.html'
    success_url = reverse_lazy('home')
 """

@Rest_auth_required
def customer_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        created_by = request.user
        document = request.FILES.get('document')
        description = request.POST.get('description')
        
        customer = Customer(name=name,email=email,phone=phone,address=address,
        created_by=created_by,document=document,description=description)
        
        customer.save()
        return JsonResponse({"success": True, "message": 'Customer created'}, status=200)
    else:
        form = CustomerForm()

    return render(request, 'crm/upload.html', {'form': form})


""" 
class CustomerListView(ListView):
model = Customer
template_name = 'crm/download.html'
    context_object_name = 'customers'
 """

def customer_list_view(request):
    customers = Customer.objects.all() 
    context = {'customers': customers}
    return render(request, 'crm/download.html', context)

def download(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    response = HttpResponse(customer.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{customer.document.name}"'
    return response


    """ 
i canot create form and modify field created_by

        """