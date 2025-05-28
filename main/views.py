from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .api import get_dashboard_data

@login_required
def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON data for AJAX requests
        return JsonResponse(get_dashboard_data())
    
    # Initial page load - return basic template
    return render(request, 'main/index.html')

@login_required
def get_dashboard_updates(request):
    """API endpoint for getting dashboard updates"""
    return JsonResponse(get_dashboard_data())




