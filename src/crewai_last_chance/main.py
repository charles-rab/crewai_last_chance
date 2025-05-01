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
    import os
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "shopify_automation_report.md")
    
    with open(output_file, "w") as f:
        f.write(result)
    
    print(f"\nShopify automation report saved to {output_file}")

if __name__ == "__main__":
    main()
