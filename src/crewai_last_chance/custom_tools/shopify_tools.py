import os
import shopify
import requests
from crewai.tools import BaseTool
from pydantic import Field
from typing import Dict, List, Optional, Any

class ShopifyBaseTool(BaseTool):
    def __init__(self):
        super().__init__()
        self._setup_shopify_session()

    def _setup_shopify_session(self):
        """Set up the Shopify API session."""
        shop_url = os.getenv("SHOPIFY_STORE_URL")
        api_version = '2023-10'  # Use the current API version
        token = os.getenv("SHOPIFY_API_TKN")
        
        session = shopify.Session(shop_url, api_version, token)
        shopify.ShopifyResource.activate_session(session)


class ShopifyInventoryTool(ShopifyBaseTool):
    name: str = "ShopifyInventoryTool"
    description: str = "Get information about inventory levels and manage inventory"

    def _run(self, action: str = "get_all", product_id: Optional[int] = None, location_id: Optional[int] = None, quantity: Optional[int] = None) -> Dict:
        """
        Manage inventory in Shopify.
        
        Args:
            action: The action to perform (get_all, get_by_product, update)
            product_id: The ID of the product
            location_id: The ID of the location
            quantity: The quantity to set (for update action)
            
        Returns:
            Dict containing inventory information
        """
        try:
            if action == "get_all":
                inventory_levels = shopify.InventoryLevel.find()
                return [level.attributes for level in inventory_levels]
            
            elif action == "get_by_product" and product_id:
                inventory_items = shopify.InventoryItem.find(product_id=product_id)
                return [item.attributes for item in inventory_items]
            
            elif action == "update" and product_id and location_id and quantity is not None:
                inventory_item_id = self._get_inventory_item_id(product_id)
                inventory_level = shopify.InventoryLevel.set(inventory_item_id, location_id, quantity)
                return inventory_level.attributes
            
            return {"error": "Invalid parameters for inventory action"}
            
        except Exception as e:
            return {"error": str(e)}
            
    def _get_inventory_item_id(self, product_id):
        """Helper method to get inventory_item_id from product_id"""
        variant = shopify.Variant.find_first(product_id=product_id)
        return variant.inventory_item_id if variant else None


class ShopifyProductTool(ShopifyBaseTool):
    name: str = "ShopifyProductTool"
    description: str = "Get information about products and manage products"

    def _run(self, action: str = "get_all", product_id: Optional[int] = None, **kwargs) -> Dict:
        """
        Manage products in Shopify.
        
        Args:
            action: The action to perform (get_all, get_by_id, create, update, delete)
            product_id: The ID of the product (for get_by_id, update, delete)
            **kwargs: Additional parameters for create/update actions
            
        Returns:
            Dict containing product information
        """
        try:
            if action == "get_all":
                products = shopify.Product.find()
                return [product.attributes for product in products]
            
            elif action == "get_by_id" and product_id:
                product = shopify.Product.find(product_id)
                return product.attributes
            
            elif action == "create" and "title" in kwargs:
                product = shopify.Product()
                for key, value in kwargs.items():
                    setattr(product, key, value)
                product.save()
                return product.attributes
            
            elif action == "update" and product_id:
                product = shopify.Product.find(product_id)
                for key, value in kwargs.items():
                    setattr(product, key, value)
                product.save()
                return product.attributes
            
            elif action == "delete" and product_id:
                product = shopify.Product.find(product_id)
                result = product.destroy()
                return {"success": result}
            
            return {"error": "Invalid parameters for product action"}
            
        except Exception as e:
            return {"error": str(e)}


class ShopifyOrderTool(ShopifyBaseTool):
    name: str = "ShopifyOrderTool"
    description: str = "Get information about orders and manage orders"

    def _run(self, action: str = "get_all", order_id: Optional[int] = None, status: Optional[str] = None) -> Dict:
        """
        Manage orders in Shopify.
        
        Args:
            action: The action to perform (get_all, get_by_id, get_by_status)
            order_id: The ID of the order (for get_by_id)
            status: The status to filter by (for get_by_status)
            
        Returns:
            Dict containing order information
        """
        try:
            if action == "get_all":
                orders = shopify.Order.find()
                return [order.attributes for order in orders]
            
            elif action == "get_by_id" and order_id:
                order = shopify.Order.find(order_id)
                return order.attributes
            
            elif action == "get_by_status" and status:
                orders = shopify.Order.find(status=status)
                return [order.attributes for order in orders]
            
            return {"error": "Invalid parameters for order action"}
            
        except Exception as e:
            return {"error": str(e)}


class ShopifyCustomerTool(ShopifyBaseTool):
    name: str = "ShopifyCustomerTool"
    description: str = "Get information about customers and manage customers"

    def _run(self, action: str = "get_all", customer_id: Optional[int] = None) -> Dict:
        """
        Manage customers in Shopify.
        
        Args:
            action: The action to perform (get_all, get_by_id)
            customer_id: The ID of the customer (for get_by_id)
            
        Returns:
            Dict containing customer information
        """
        try:
            if action == "get_all":
                customers = shopify.Customer.find()
                return [customer.attributes for customer in customers]
            
            elif action == "get_by_id" and customer_id:
                customer = shopify.Customer.find(customer_id)
                return customer.attributes
            
            return {"error": "Invalid parameters for customer action"}
            
        except Exception as e:
            return {"error": str(e)}


class ShopifyAnalyticsTool(ShopifyBaseTool):
    name: str = "ShopifyAnalyticsTool"
    description: str = "Get analytics data from Shopify"

    def _run(self, report_type: str = "sales", date_range: str = "last_30_days") -> Dict:
        """
        Get analytics data from Shopify.
        
        Args:
            report_type: The type of report to get (sales, traffic, inventory)
            date_range: The date range to get data for (last_30_days, last_90_days, last_year)
            
        Returns:
            Dict containing analytics data
        """
        # This is a simplified implementation - Shopify Analytics API has more complex requirements
        # In a real implementation, you would use the Shopify Analytics API
        shop_url = os.getenv("SHOPIFY_STORE_URL")
        api_key = os.getenv("SHOPIFY_API_KEY")
        password = os.getenv("SHOPIFY_API_PWD")
        
        try:
            # Example request structure - you would need to adapt this to the actual API
            url = f"https://{api_key}:{password}@{shop_url}/admin/api/2023-10/reports.json"
            response = requests.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to fetch analytics data: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
