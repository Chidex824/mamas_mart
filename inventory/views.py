from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory, Category
from django.urls import reverse
from django.contrib import messages

def inventory_list(request):
    inventories = Inventory.objects.select_related('category').all()
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})

def add_inventory(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        category_id = request.POST.get('category')
        quantity = request.POST.get('quantity')
        location = request.POST.get('location')

        category = get_object_or_404(Category, id=category_id)

        Inventory.objects.create(
            item_name=item_name,
            category=category,
            quantity=quantity,
            location=location
        )
        messages.success(request, 'Inventory item added successfully.')
        return redirect(reverse('inventory:inventory_list'))

    return render(request, 'inventory/add_inventory.html', {'categories': categories})

def edit_inventory(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        inventory.item_name = request.POST.get('item_name')
        category_id = request.POST.get('category')
        inventory.category = get_object_or_404(Category, id=category_id)
        inventory.quantity = request.POST.get('quantity')
        inventory.location = request.POST.get('location')
        inventory.save()
        messages.success(request, 'Inventory item updated successfully.')
        return redirect(reverse('inventory:inventory_list'))

    return render(request, 'inventory/edit_inventory.html', {'inventory': inventory, 'categories': categories})

def delete_inventory(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory.delete()
        messages.success(request, 'Inventory item deleted successfully.')
        return redirect(reverse('inventory:inventory_list'))
    return render(request, 'inventory/delete_inventory.html', {'inventory': inventory})

from collections import defaultdict
from main.models import Supplier
from products.models import Purchase

def warehouse(request):
    inventories = Inventory.objects.select_related('category').all()
    location_dict = defaultdict(list)
    for inventory in inventories:
        location_dict[inventory.location].append(inventory)
    # Convert defaultdict to regular dict for template context
    grouped_inventories = dict(location_dict)
    return render(request, 'inventory/warehouse.html', {'grouped_inventories': grouped_inventories})

def supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier.html', {'suppliers': suppliers})

def invoice(request):
    purchases = Purchase.objects.select_related('product', 'supplier').all()
    return render(request, 'inventory/invoice.html', {'purchases': purchases})

def transfer_product(request):
    return render(request, 'inventory/transfer_product.html')

def stock(request):
    return render(request, 'inventory/stock.html')
