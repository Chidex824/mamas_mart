from django.db.models import Sum, Count
from django.db.models.functions import ExtractWeek, ExtractMonth, TruncDate
from django.utils import timezone
from datetime import timedelta
from .models import DailySalesReport
from products.models import Product, Purchase, Sale

def get_dashboard_data():
    """Get all dashboard data in a single API call"""
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    # Weekly earnings data
    weekly_sales = DailySalesReport.objects.filter(
        date__gte=week_ago
    ).annotate(
        day=TruncDate('date')
    ).values('day').annotate(
        total=Sum('total_sales'),
        transactions=Count('id')
    ).order_by('day')

    # Monthly revenue breakup
    revenue_breakup = Sale.objects.filter(
        date__gte=month_ago
    ).values('product__category').annotate(
        total=Sum('total_amount')
    ).order_by('-total')

    # Sales vs Expenses overview
    sales_expenses = {
        'sales': [],
        'expenses': [],
        'dates': []
    }
    
    for i in range(8):  # Last 8 months
        date = now - timedelta(days=30 * i)
        month_sales = Sale.objects.filter(
            date__year=date.year,
            date__month=date.month
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        month_expenses = Purchase.objects.filter(
            date__year=date.year,
            date__month=date.month
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        sales_expenses['sales'].insert(0, float(month_sales))
        sales_expenses['expenses'].insert(0, float(month_expenses))
        sales_expenses['dates'].insert(0, date.strftime('%b'))

    # Get current stats
    current_stats = {
        'total_products': Product.objects.count(),
        'low_stock_products': Product.objects.filter(stock__lte=10).count(),
        'todays_sales': DailySalesReport.objects.filter(
            date=timezone.now().date()
        ).aggregate(
            total_sales=Sum('total_sales'),
            total_transactions=Count('id')
        )
    }

    return {
        'weekly_earnings': list(weekly_sales),
        'revenue_breakup': list(revenue_breakup),
        'sales_expenses': sales_expenses,
        'current_stats': current_stats
    }
