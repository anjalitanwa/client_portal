import requests
import json
import uuid
from django.conf import settings


class ShopifyMCPService:
    """
    Service class to communicate with the Shopify MCP server
    """
    def __init__(self):
        self.server_url = getattr(settings, 'MCP_SERVER_URL', 'http://localhost:3001')
        self.tools_endpoint = f"{self.server_url}/message/" 

    def _send_json_rpc_request(self, method_name, params=None):
        """
        Send a JSON-RPC request to the MCP server
        """
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method_name,
            "params": params or {}
        }
        
        print(f"Django is asking the MCP Specialist: {method_name} with params: {params}")

        try:
            response = requests.post(self.tools_endpoint, json=payload, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            print(f"MCP Specialist responded successfully!")
            return result

        except requests.exceptions.ConnectionError:
            print("ERROR: Django could not find the MCP Specialist. Is it running?")
            return {"error": {"message": "Connection failed. Is the MCP server running?"}}
        except Exception as e:
            print(f"ERROR: Something went wrong: {e}")
            return {"error": {"message": str(e)}}

    def list_products(self, first=10):
        """Get a list of products"""
        return self._send_json_rpc_request("get-products", {"limit": first})

    def get_product_count(self):
        """Get the total number of products"""
        response = self._send_json_rpc_request("get-products", {"limit": 250})
        if "error" in response:
            return response
        
        try:
            response_text = response.get("result", {}).get("content", [{}])[0].get("text", "{}")
            products_data = json.loads(response_text)
            products = products_data.get("products", [])
            return {"result": {"count": len(products)}}
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"Error parsing product count response: {e}")
            return {"error": {"message": "Failed to parse product count response."}}

    def get_product_by_id(self, product_id):
        """Get a specific product by ID"""
        return self._send_json_rpc_request("get-product-by-id", {"productId": product_id})

    def create_product(self, title, description_html="", status="DRAFT"):
        """Create a new product"""
        return self._send_json_rpc_request("create-product", {
            "title": title,
            "descriptionHtml": description_html,
            "status": status
        })
    
    def create_product_with_variants(self, title, description_html="", status="DRAFT", 
                                    options=None, variants=None, tags=None, 
                                    product_type=None, vendor=None):
        """
        Create a new product with variants (patterns, sizes, colors, etc.)
        
        Args:
            title: Product title
            description_html: Product description in HTML
            status: Product status (ACTIVE, DRAFT, ARCHIVED)
            options: List of product options (e.g., ["Size", "Color"])
            variants: List of variant dictionaries with details
            tags: Product tags
            product_type: Product type
            vendor: Product vendor
        """
        product_data = {
            "title": title,
            "descriptionHtml": description_html,
            "status": status
        }
        
        if options:
            product_data["options"] = options
            
        if variants:
            product_data["variants"] = variants
            
        if tags:
            product_data["tags"] = tags
            
        if product_type:
            product_data["productType"] = product_type
            
        if vendor:
            product_data["vendor"] = vendor
            
        return self._send_json_rpc_request("create-product-with-variants", product_data)
    
    def update_product(self, product_id, **kwargs):
        """Update an existing product"""
        params = {"productId": product_id}
        params.update(kwargs)
        return self._send_json_rpc_request("update-product", params)
    
    def delete_product(self, product_id):
        """Delete a product"""
        return self._send_json_rpc_request("delete-product", {"productId": product_id})
    
    def create_product_image(self, product_id, image_src, alt_text=None):
        """Add an image to a product"""
        params = {
            "productId": product_id,
            "src": image_src
        }
        if alt_text:
            params["altText"] = alt_text
        return self._send_json_rpc_request("create-product-image", params)
    
    # New methods for order handling
    def list_orders(self, first=10):
        """Get a list of recent orders"""
        return self._send_json_rpc_request("get-orders", {"limit": first})
    
    def get_order_by_id(self, order_id):
        """Get a specific order by ID"""
        return self._send_json_rpc_request("get-order-by-id", {"orderId": order_id})

    
    
    
# import requests
# import json
# import uuid
# from django.conf import settings



# class ShopifyMCPService:
#     """
#     Service class to communicate with the Shopify MCP server
#     """
#     def __init__(self):
#         self.server_url = getattr(settings, 'MCP_SERVER_URL', 'http://localhost:3001')
#         self.tools_endpoint = f"{self.server_url}/message/" 

#     def _send_json_rpc_request(self, method_name, params=None):
#         """
#         Send a JSON-RPC request to the MCP server
#         """
#         payload = {
#             "jsonrpc": "2.0",
#             "id": str(uuid.uuid4()),
#             "method": method_name,
#             "params": params or {}
#         }
        
#         print(f"Django is asking the MCP Specialist: {method_name} with params: {params}")

#         try:
#             response = requests.post(self.tools_endpoint, json=payload, timeout=15)
#             response.raise_for_status()
            
#             result = response.json()
#             print(f"MCP Specialist responded successfully!")
#             return result

#         except requests.exceptions.ConnectionError:
#             print("ERROR: Django could not find the MCP Specialist. Is it running?")
#             return {"error": {"message": "Connection failed. Is the MCP server running?"}}
#         except Exception as e:
#             print(f"ERROR: Something went wrong: {e}")
#             return {"error": {"message": str(e)}}

#     def list_products(self, first=10):
#         """Get a list of products"""
#         return self._send_json_rpc_request("get-products", {"limit": first})

#     def get_product_count(self):
#         """Get the total number of products"""
#         response = self._send_json_rpc_request("get-products", {"limit": 250})
#         if "error" in response:
#             return response
        
#         try:
#             response_text = response.get("result", {}).get("content", [{}])[0].get("text", "{}")
#             products_data = json.loads(response_text)
#             products = products_data.get("products", [])
#             return {"result": {"count": len(products)}}
#         except (json.JSONDecodeError, IndexError, KeyError) as e:
#             print(f"Error parsing product count response: {e}")
#             return {"error": {"message": "Failed to parse product count response."}}

#     def get_product_by_id(self, product_id):
#         """Get a specific product by ID"""
#         return self._send_json_rpc_request("get-product-by-id", {"productId": product_id})

#     def create_product(self, title, description_html="", status="DRAFT"):
#         """Create a new product"""
#         return self._send_json_rpc_request("create-product", {
#             "title": title,
#             "descriptionHtml": description_html,
#             "status": status
#         })
    
#     def create_product_with_variants(self, title, description_html="", status="DRAFT", 
#                                     options=None, variants=None, tags=None, 
#                                     product_type=None, vendor=None):
#         """
#         Create a new product with variants (patterns, sizes, colors, etc.)
        
#         Args:
#             title: Product title
#             description_html: Product description in HTML
#             status: Product status (ACTIVE, DRAFT, ARCHIVED)
#             options: List of product options (e.g., ["Size", "Color"])
#             variants: List of variant dictionaries with details
#             tags: Product tags
#             product_type: Product type
#             vendor: Product vendor
#         """
#         product_data = {
#             "title": title,
#             "descriptionHtml": description_html,
#             "status": status
#         }
        
#         if options:
#             product_data["options"] = options
            
#         if variants:
#             product_data["variants"] = variants
            
#         if tags:
#             product_data["tags"] = tags
            
#         if product_type:
#             product_data["productType"] = product_type
            
#         if vendor:
#             product_data["vendor"] = vendor
            
#         return self._send_json_rpc_request("create-product-with-variants", product_data)
    
#     def update_product(self, product_id, **kwargs):
#         """Update an existing product"""
#         params = {"productId": product_id}
#         params.update(kwargs)
#         return self._send_json_rpc_request("update-product", params)
    
#     def delete_product(self, product_id):
#         """Delete a product"""
#         return self._send_json_rpc_request("delete-product", {"productId": product_id})
    
#     def create_product_image(self, product_id, image_src, alt_text=None):
#         """Add an image to a product"""
#         params = {
#             "productId": product_id,
#             "src": image_src
#         }
#         if alt_text:
#             params["altText"] = alt_text
#         return self._send_json_rpc_request("create-product-image", params)


# # import requests
# # import json
# # import uuid
# # from django.conf import settings

# # class ShopifyMCPService:
# #     """
# #     Service class to communicate with the Shopify MCP server
# #     """
# #     def __init__(self):
# #         self.server_url = getattr(settings, 'MCP_SERVER_URL', 'http://localhost:3001')
# #         self.tools_endpoint = f"{self.server_url}/message/" 

# #     def _send_json_rpc_request(self, method_name, params=None):
# #         """
# #         Send a JSON-RPC request to the MCP server
# #         """
# #         payload = {
# #             "jsonrpc": "2.0",
# #             "id": str(uuid.uuid4()),
# #             "method": method_name,
# #             "params": params or {}
# #         }
        
# #         print(f"Django is asking the MCP Specialist: {method_name} with params: {params}")

# #         try:
# #             response = requests.post(self.tools_endpoint, json=payload, timeout=15)
# #             response.raise_for_status()
            
# #             result = response.json()
# #             print(f"MCP Specialist responded successfully!")
# #             return result

# #         except requests.exceptions.ConnectionError:
# #             print("ERROR: Django could not find the MCP Specialist. Is it running?")
# #             return {"error": {"message": "Connection failed. Is the MCP server running?"}}
# #         except Exception as e:
# #             print(f"ERROR: Something went wrong: {e}")
# #             return {"error": {"message": str(e)}}

# #     def list_products(self, first=10):
# #         """Get a list of products"""
# #         # The MCP server expects 'limit', not 'first'
# #         return self._send_json_rpc_request("get-products", {"limit": first})

# #     def get_product_count(self):
# #         """Get the total number of products"""
# #         # Call the correct method 'get-products' with a high limit
# #         response = self._send_json_rpc_request("get-products", {"limit": 250})
# #         if "error" in response:
# #             return response
        
# #         # Parse the nested response to count the products
# #         try:
# #             response_text = response.get("result", {}).get("content", [{}])[0].get("text", "{}")
# #             products_data = json.loads(response_text)
# #             products = products_data.get("products", [])
# #             return {"result": {"count": len(products)}}
# #         except (json.JSONDecodeError, IndexError, KeyError) as e:
# #             print(f"Error parsing product count response: {e}")
# #             return {"error": {"message": "Failed to parse product count response."}}

# #     def get_product_by_id(self, product_id):
# #         """Get a specific product by ID"""
# #         return self._send_json_rpc_request("get-product-by-id", {"productId": product_id})

# #     def create_product(self, title, description_html="", status="DRAFT"):
# #         """Create a new product"""
# #         return self._send_json_rpc_request("create-product", {
# #             "title": title,
# #             "descriptionHtml": description_html,
# #             "status": status
# #         })