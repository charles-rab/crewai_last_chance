import os
from dotenv import load_dotenv
from crewai_last_chance.crew import ShopifyCrewAI

def main():
    """Run the ShopifyCrewAI to automate store operations."""
    load_dotenv()
    
    print("Starting Shopify Store Automation with CrewAI...")
    
    # Initialize the ShopifyCrewAI
    shopify_crew = ShopifyCrewAI()
    
    # Run the crew
    store_url = os.getenv("SHOPIFY_STORE_URL", "vivamarket.com.co")
    result = shopify_crew.run_crew(store_url)
    
    # Print the result
    print("\n\n===== Shopify Automation Results =====")
    print(result)
    
    # Save the result to a file
    with open("output/shopify_automation_report.md", "w") as f:
        f.write(result)
    
    print("\nShopify automation report saved to output/shopify_automation_report.md")

if __name__ == "__main__":
    main()
