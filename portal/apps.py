from django.apps import AppConfig
import subprocess
import webbrowser
import os

class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal'

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    def ready(self):
        # Path to your Shopify MCP server
        mcp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shopify_mcp')

        # Prevent running MCP twice during Django autoreload
        if os.environ.get('RUN_MAIN') == 'true':
            return

        # Start the MCP server automatically
        try:
            subprocess.Popen(["npm", "run", "start"], cwd=mcp_path)
            print(" Shopify MCP Server started successfully!")
        except Exception as e:
            print(f" Could not start MCP server: {e}")

        # Give MCP a few seconds to boot
        time.sleep(5)

        # Auto-open Shopify Admin Dashboard
        store_url = "https://8s88kc-cm.myshopify.com/admin"
        webbrowser.open(store_url)
        print(f" Opening Shopify Dashboard → {store_url}")

        # (Optional) Open your Django Create Product page
        webbrowser.open("http://127.0.0.1:8000/create/")
        print(" Opening Django Product Creation Page...")
