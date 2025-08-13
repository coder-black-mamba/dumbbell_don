def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        payments = Payment.objects.filter(status='PAID')

        if start_date and end_date:
            payments = payments.filter(paid_at__date__range=[start_date, end_date])

        report = payments.values(
            'member__id', 'member__email'
        ).annotate(
            total_paid_cents=Sum('amount_cents'),
            payment_count=Count('id')
        ).order_by('-total_paid_cents')
