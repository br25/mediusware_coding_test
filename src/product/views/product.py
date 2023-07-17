from django.views import generic
from django.views.generic import ListView
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.utils import timezone
from django.core.paginator import Paginator


from product.models import Variant, Product, ProductVariant, ProductVariantPrice

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ListProductView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if variant:
            queryset = queryset.filter(productvariant__variant_title=variant)

        if price_from and price_to:
            queryset = queryset.filter(productvariantprice__price__range=(price_from, price_to))

        if date:
            try:
                date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date=date_obj)
            except ValueError:
                pass

        return queryset.distinct()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['variants'] = Variant.objects.all().distinct()

        variant_sub_options = {} 
        
        for variant in context['variants']:
            sub_options = ProductVariant.objects.filter(variant=variant).values_list('variant_title', flat=True).distinct()
            variant_sub_options[variant] = sub_options

        context['variant_sub_options'] = variant_sub_options

        product_variant_data = {}

        for product in context['products']:
            variant_data = ProductVariantPrice.objects.filter(product=product).annotate(
                variant_combination=Concat(
                    F('product_variant_one__variant_title'),
                    Value(' / '),
                    F('product_variant_two__variant_title'),
                    Value(' / '),
                    F('product_variant_three__variant_title')
                )
            )

            product_variant_data[product.id] = variant_data

        context['product_variant_data'] = product_variant_data
        return context
    