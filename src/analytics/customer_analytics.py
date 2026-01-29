"""
Customer Analytics Module
Analyzes customer behavior, sales data, and provides insights
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from langchain_core.prompts import ChatPromptTemplate

from ..utils.llm_helper import get_llm


class CustomerAnalyticsModule:
    """Module for customer analytics and insights"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.3)  # Lower temperature for more analytical responses
    
    def analyze_sales_data(
        self,
        sales_data: Dict[str, Any],
        time_period: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze sales data and provide insights
        
        Args:
            sales_data: Sales data dictionary with metrics
            time_period: Time period of the data
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert retail analytics consultant.
            Analyze sales data and provide actionable insights."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Time Period: {time_period}
            
            Sales Data:
            {sales_data}
            
            Provide analysis including:
            1. Key performance indicators (KPIs) summary
            2. Top performing products/categories
            3. Underperforming areas
            4. Sales trends and patterns
            5. Seasonal variations
            6. Customer segment analysis
            7. Actionable recommendations
            8. Growth opportunities
            
            Be specific and data-driven in your insights.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "time_period": time_period,
            "sales_data": json.dumps(sales_data, indent=2)
        })
        
        analysis = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "analysis": analysis,
            "time_period": time_period,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def segment_customers(
        self,
        customer_data: List[Dict[str, Any]],
        segmentation_criteria: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Segment customers based on behavior and characteristics
        
        Args:
            customer_data: List of customer records
            segmentation_criteria: Criteria for segmentation (RFM, demographics, behavior)
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in customer segmentation and targeting.
            Create meaningful customer segments for personalized marketing."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Segmentation Criteria: {segmentation_criteria}
            
            Customer Data Summary:
            - Total Customers: {customer_count}
            
            Create customer segments including:
            1. Segment names and descriptions
            2. Size of each segment
            3. Key characteristics of each segment
            4. Purchase behavior patterns
            5. Lifetime value potential
            6. Recommended marketing strategies for each segment
            7. Personalization opportunities
            
            Create 4-6 actionable segments.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "segmentation_criteria": segmentation_criteria,
            "customer_count": len(customer_data)
        })
        
        segmentation = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "segmentation": segmentation,
            "criteria": segmentation_criteria,
            "total_customers": len(customer_data),
            "created_at": datetime.now().isoformat()
        }
    
    def analyze_shopping_patterns(
        self,
        transaction_data: List[Dict[str, Any]],
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze shopping patterns and basket analysis
        
        Args:
            transaction_data: List of transaction records
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in retail analytics and market basket analysis.
            Identify shopping patterns that can improve merchandising and promotions."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            
            Transaction Data:
            - Total Transactions: {transaction_count}
            
            Analyze shopping patterns including:
            1. Peak shopping times and days
            2. Average basket size and value
            3. Product affinity (what's bought together)
            4. Cross-selling opportunities
            5. Bundle recommendations
            6. Shopping journey insights
            7. Payment method preferences
            8. Actionable merchandising recommendations
            
            Focus on opportunities to increase basket size and frequency.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "transaction_count": len(transaction_data)
        })
        
        pattern_analysis = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "pattern_analysis": pattern_analysis,
            "transactions_analyzed": len(transaction_data),
            "analyzed_at": datetime.now().isoformat()
        }
    
    def process_customer_feedback(
        self,
        feedback_data: List[Dict[str, Any]],
        feedback_type: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process and analyze customer feedback
        
        Args:
            feedback_data: List of feedback records (reviews, surveys, comments)
            feedback_type: Type of feedback (reviews, surveys, social_media)
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in customer sentiment analysis and feedback processing.
            Extract insights from customer feedback to improve service and offerings."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Feedback Type: {feedback_type}
            
            Feedback Summary:
            - Total Feedback Items: {feedback_count}
            
            Analyze feedback including:
            1. Overall sentiment (positive, neutral, negative)
            2. Common themes and topics
            3. Most praised aspects
            4. Most criticized aspects
            5. Product-specific feedback
            6. Service quality insights
            7. Competitive mentions
            8. Actionable improvement recommendations
            
            Be objective and specific in identifying issues and opportunities.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "feedback_type": feedback_type,
            "feedback_count": len(feedback_data)
        })
        
        feedback_analysis = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "feedback_analysis": feedback_analysis,
            "feedback_type": feedback_type,
            "items_processed": len(feedback_data),
            "analyzed_at": datetime.now().isoformat()
        }
    
    def predict_customer_lifetime_value(
        self,
        customer_profile: Dict[str, Any],
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict customer lifetime value and retention probability
        
        Args:
            customer_profile: Customer data and purchase history
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in predictive customer analytics and CLV modeling.
            Assess customer value and retention probability."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            
            Customer Profile:
            {customer_profile}
            
            Provide prediction including:
            1. Estimated lifetime value (CLV) range
            2. Retention probability
            3. Churn risk assessment
            4. Next purchase prediction
            5. Product recommendations
            6. Engagement level
            7. Value tier classification
            8. Recommended retention strategies
            
            Base predictions on behavior patterns and industry benchmarks.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "customer_profile": json.dumps(customer_profile, indent=2)
        })
        
        prediction = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "prediction": prediction,
            "customer_id": customer_profile.get("id", "unknown"),
            "predicted_at": datetime.now().isoformat()
        }
    
    def generate_performance_report(
        self,
        metrics: Dict[str, Any],
        comparison_period: Optional[str],
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive performance report
        
        Args:
            metrics: Dictionary of performance metrics
            comparison_period: Previous period to compare against
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert retail business analyst.
            Create comprehensive performance reports with insights and recommendations."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Comparison Period: {comparison_period}
            
            Performance Metrics:
            {metrics}
            
            Generate a performance report including:
            1. Executive summary
            2. Key metrics overview
            3. Period-over-period comparison
            4. Achievement vs. targets
            5. Notable trends
            6. Areas of concern
            7. Success stories
            8. Strategic recommendations
            9. Action items
            
            Make the report clear, concise, and actionable.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "comparison_period": comparison_period or "N/A",
            "metrics": json.dumps(metrics, indent=2)
        })
        
        report = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "report": report,
            "report_date": datetime.now().isoformat(),
            "comparison_period": comparison_period
        }
