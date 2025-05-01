import os
from typing import List
from crewai import Agent, Task, Crew, Process
from crewai.tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
from crewai_last_chance.custom_tools.shopify_tools import (
    ShopifyInventoryTool, 
    ShopifyProductTool,
    ShopifyOrderTool,
    ShopifyCustomerTool,
    ShopifyAnalyticsTool
)

load_dotenv()

class ShopifyCrewAI:
    def __init__(self):
        # Initialize tools
        self.search_tool = SerperDevTool()
        self.website_tool = WebsiteSearchTool()
        
        # Initialize Shopify-specific tools
        self.inventory_tool = ShopifyInventoryTool()
        self.product_tool = ShopifyProductTool()
        self.order_tool = ShopifyOrderTool()
        self.customer_tool = ShopifyCustomerTool()
        self.analytics_tool = ShopifyAnalyticsTool()
        
    def create_agents(self):
        # Create agents with appropriate tools
        inventory_manager = Agent(
            role="Shopify Inventory Manager",
            goal="Maintain optimal inventory levels, track stock, and provide alerts for restocking",
            backstory="An experienced e-commerce inventory specialist with years of experience optimizing stock levels and preventing stockouts while minimizing excess inventory",
            tools=[self.inventory_tool, self.product_tool, self.search_tool],
            verbose=True
        )
        
        marketing_analyst = Agent(
            role="Shopify Marketing Analyst",
            goal="Analyze marketing performance, identify opportunities, and suggest marketing strategies",
            backstory="A digital marketing expert specialized in e-commerce with deep knowledge of SEO, social media marketing, and customer engagement strategies",
            tools=[self.analytics_tool, self.search_tool, self.website_tool],
            verbose=True
        )
        
        product_researcher = Agent(
            role="Product Researcher and Analyst",
            goal="Research market trends, identify potential new products, and analyze product performance",
            backstory="A market research expert who excels at identifying emerging trends and finding products with high profit potential",
            tools=[self.product_tool, self.search_tool, self.website_tool],
            verbose=True
        )
        
        customer_service_assistant = Agent(
            role="Customer Service Assistant",
            goal="Monitor customer inquiries, prepare response templates, and identify common customer issues",
            backstory="A customer support specialist with experience in e-commerce and a talent for clear communication and problem resolution",
            tools=[self.customer_tool, self.order_tool],
            verbose=True
        )
        
        store_optimizer = Agent(
            role="Shopify Store Optimizer",
            goal="Continuously analyze and improve the store's performance, layout, and user experience",
            backstory="A Shopify expert with a deep understanding of e-commerce UX/UI principles and conversion optimization techniques",
            tools=[self.analytics_tool, self.website_tool],
            verbose=True
        )
        
        return {
            "inventory_manager": inventory_manager,
            "marketing_analyst": marketing_analyst,
            "product_researcher": product_researcher,
            "customer_service_assistant": customer_service_assistant,
            "store_optimizer": store_optimizer
        }
        
    def create_tasks(self, agents, store_url):
        # Create tasks for each agent
        inventory_analysis = Task(
            description=f"Analyze current inventory levels for {store_url}, identify products at risk of stockout, and recommend restocking quantities",
            expected_output="A detailed inventory report with actionable recommendations",
            agent=agents["inventory_manager"]
        )
        
        marketing_analysis = Task(
            description=f"Analyze marketing channel performance for {store_url}, identify opportunities, and recommend marketing strategies",
            expected_output="A marketing performance report with channel analysis and strategy recommendations",
            agent=agents["marketing_analyst"]
        )
        
        product_research = Task(
            description=f"Research market trends and identify potential new products that align with {store_url}'s current offerings",
            expected_output="A list of potential new products with market analysis and profit projections",
            agent=agents["product_researcher"]
        )
        
        customer_analysis = Task(
            description=f"Analyze customer feedback for {store_url}, identify common issues, and prepare response templates",
            expected_output="A report of common customer issues with prepared response templates",
            agent=agents["customer_service_assistant"]
        )
        
        store_optimization = Task(
            description=f"Analyze {store_url}'s performance, layout, and user experience, and recommend improvements",
            expected_output="A store optimization report with actionable recommendations",
            agent=agents["store_optimizer"],
            context=[inventory_analysis, marketing_analysis, product_research, customer_analysis]
        )
        
        return [inventory_analysis, marketing_analysis, product_research, customer_analysis, store_optimization]
    
    def run_crew(self, store_url="vivamarket.com.co"):
        agents = self.create_agents()
        tasks = self.create_tasks(agents, store_url)
        
        # Create the crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Run the crew and get the result
        result = crew.kickoff()
        
        return result
