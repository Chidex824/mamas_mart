from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Sale

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'

class SaleCreateView(CreateView):
    model = Sale
    template_name = 'sales/add_sales.html'
    fields = ['product', 'quantity', 'price']
    success_url = reverse_lazy('sales:index')

class SaleUpdateView(UpdateView):
    model = Sale
    template_name = 'sales/edit_sales.html'
    fields = ['product', 'quantity', 'price']
    success_url = reverse_lazy('sales:index')

class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'sales/remove_sales.html'
    success_url = reverse_lazy('sales:index')
