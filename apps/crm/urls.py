
from django.urls import path
from apps.crm.views.customer import download, customer_create_view, customer_list_view

urlpatterns = [
    #path('', CustomerListView.as_view(), name='customers'),
    path('', customer_list_view, name='customers'),
    #path('upload/', CustomerCreateView.as_view(), name='upload'),
    path('upload/', customer_create_view, name='upload'),

    path('download/<int:customer_id>/', download, name='download'),
]
