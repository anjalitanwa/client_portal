from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,logging


logger = logging.getLogger(__name__)

@csrf_exempt
def shopify_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("Shopify ORDER CREATED:",data)
        logger.info(f"Shopify Webhook: {data}")
        return JsonResponse({"status": "received"}, status=200)
    return JsonResponse({"error": "invalid method"}, status=405)


def shopify_home(request):
    
    return redirect("https://admin.shopify.com/store/8s88kc-cm")


def debug_view(request):

    return JsonResponse({"status": "ok", "message": "Django is working and redirect is set!"})


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        print("\n===== NEW ORDER RECEIVED =====")
        print(data) 

        return JsonResponse({"status": "success"})

    return JsonResponse({"error": "Invalid request"}, status=400)













# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from django.urls import reverse
# from .shopify_service import ShopifyMCPService
# import json 

# shopify_service = ShopifyMCPService()

# def shopify_home(request):
#     return redirect("https://admin.shopify.com/store/8s88kc-cm/products")
# def product_list_view(request):
#     """Displays a list of products from the Shopify store."""
#     try:
#         api_response = shopify_service.list_products()
        
#         if "error" in api_response:
#             return render(request, "product_list.html", {"error_message": api_response["error"]["message"]})
        
#         response_text = api_response.get("result", {}).get("content", [{}])[0].get("text", "{}")
#         products_data = json.loads(response_text)
#         products = products_data.get("products", [])
        
#         return render(request, "product_list.html", {"products": products})
#     except Exception as e:
#         return render(request, "product_list.html", {"error_message": str(e)})

# def product_detail_view(request, product_id):
#     try:
#         api_response = shopify_service.get_product_by_id(product_id)
        
#         context = {}
#         if "error" in api_response:
#             context['error_message'] = api_response['error']['message']
#             context['product'] = None
#         else:
#             response_text = api_response.get("result", {}).get("content", [{}])[0].get("text", "{}")
#             product_data = json.loads(response_text)
#             context['product'] = product_data
#             context['error_message'] = None

#         return render(request, 'product_detail.html', context)
#     except Exception as e:
#         return render(request, 'product_detail.html', {"error_message": str(e)})

# def create_sample_product_view(request):
#     """A helper view to create a sample product for testing purposes."""
#     print("--- Creating a sample product ---")
#     api_response = shopify_service.create_product(
#         title="My Test T-Shirt",
#         description_html="<p>A comfortable t-shirt for testing purposes.</p>",
#         status="ACTIVE" 
#     )
#     print("--- Finished creating product ---")
#     return JsonResponse(api_response)

# def create_product_with_variants_view(request):
#     """Create a product with variants (patterns, sizes, colors, etc.)"""
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description', '')
#         status = request.POST.get('status', 'DRAFT')
#         product_type = request.POST.get('product_type', '')
#         vendor = request.POST.get('vendor', '')
#         tags = request.POST.get('tags', '')
        
#         # Get options (like Size, Color, Pattern)
#         options = []
#         option_names = request.POST.getlist('option_name')
#         for name in option_names:
#             if name.strip():
#                 options.append({"name": name.strip()})
        
#         # Get variants
#         variants = []
#         variant_count = int(request.POST.get('variant_count', 0))
        
#         for i in range(variant_count):
#             variant = {
#                 "title": request.POST.get(f'variant_title_{i}', ''),
#                 "price": request.POST.get(f'variant_price_{i}', '0.00'),
#                 "sku": request.POST.get(f'variant_sku_{i}', ''),
#                 "inventory_quantity": int(request.POST.get(f'variant_inventory_{i}', 0)),
#                 "weight": float(request.POST.get(f'variant_weight_{i}', 0.0)),
#                 "weight_unit": request.POST.get(f'variant_weight_unit_{i}', 'kg'),
#                 "requires_shipping": request.POST.get(f'variant_requires_shipping_{i}', 'off') == 'on',
#                 "taxable": request.POST.get(f'variant_taxable_{i}', 'off') == 'on',
#                 "option1": request.POST.get(f'variant_option1_{i}', ''),
#                 "option2": request.POST.get(f'variant_option2_{i}', ''),
#                 "option3": request.POST.get(f'variant_option3_{i}', ''),
#             }
#             variants.append(variant)
        
#         api_response = shopify_service.create_product_with_variants(
#             title=title,
#             description_html=description,
#             status=status,
#             options=options,
#             variants=variants,
#             tags=tags,
#             product_type=product_type,
#             vendor=vendor
#         )
        
#         if "error" in api_response:
#             return render(request, "create_product.html", {
#                 "error_message": api_response["error"]["message"],
#                 "form_data": request.POST
#             })
        
#         return redirect('product_list')
    
#     return render(request, "create_product.html")

# def test_connection_view(request):
#     """Tests the connection to the MCP server and returns the product count."""
#     print("--- Testing Connection to Shopify MCP Server ---")
#     api_response = shopify_service.get_product_count()
#     print("--- Finished Test ---")
#     return JsonResponse(api_response)

# def debug_view(request):
#     """A simple debug view to test if Django is working."""
#     return JsonResponse({"status": "debug", "message": "Django is working correctly!"})

# # from django.shortcuts import render
# # from django.http import JsonResponse
# # from .shopify_service import ShopifyMCPService
# # import json 


# # shopify_service = ShopifyMCPService()

# # def product_list_view(request):
# #     """Displays a list of products from the Shopify store."""
# #     try:
# #         api_response = shopify_service.list_products()
        
# #         if "error" in api_response:
# #             return render(request, "product_list.html", {"error_message": api_response["error"]["message"]})
        
# #         response_text = api_response.get("result", {}).get("content", [{}])[0].get("text", "{}")
# #         products_data = json.loads(response_text)
# #         products = products_data.get("products", [])
        
# #         return render(request, "product_list.html", {"products": products})
# #     except Exception as e:
# #         return render(request, "product_list.html", {"error_message": str(e)})

# # def product_detail_view(request, product_id):
   
# #     try:
# #         api_response = shopify_service.get_product_by_id(product_id)
        
# #         context = {}
# #         if "error" in api_response:
# #             context['error_message'] = api_response['error']['message']
# #             context['product'] = None
# #         else:
# #             response_text = api_response.get("result", {}).get("content", [{}])[0].get("text", "{}")
# #             product_data = json.loads(response_text)
# #             context['product'] = product_data
# #             context['error_message'] = None

# #         return render(request, 'product_detail.html', context)
# #     except Exception as e:
# #         return render(request, 'product_detail.html', {"error_message": str(e)})


# # def create_sample_product_view(request):
# #     """A helper view to create a sample product for testing purposes."""
# #     print("--- Creating a sample product ---")
# #     api_response = shopify_service.create_product(
# #         title="My Test T-Shirt",
# #         description_html="<p>A comfortable t-shirt for testing purposes.</p>",
# #         status="ACTIVE" 
# #     )
# #     print("--- Finished creating product ---")
# #     return JsonResponse(api_response)


# # def test_connection_view(request):
# #     """Tests the connection to the MCP server and returns the product count."""
# #     print("--- Testing Connection to Shopify MCP Server ---")
# #     api_response = shopify_service.get_product_count()
# #     print("--- Finished Test ---")
# #     return JsonResponse(api_response)


# # def debug_view(request):
# #     """A simple debug view to test if Django is working."""
# #     return JsonResponse({"status": "debug", "message": "Django is working correctly!"})