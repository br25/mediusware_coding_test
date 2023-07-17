from django.views import generic
from django.views.generic import ListView
from django.db.models import F, Value
from django.db.models.functions import Concat
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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