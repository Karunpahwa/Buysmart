"""
Valuation Service for estimating fair market values
Uses OpenAI API to analyze pricing and market conditions
"""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
import openai
from ..config.settings import settings

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.openai_api_key


class ValuationService:
    """Service for estimating fair market values using OpenAI"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def estimate_value(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate fair market value for a listing
        
        Args:
            listing_data: Listing data with analysis
            
        Returns:
            Valuation analysis
        """
        try:
            # Prepare valuation request
            valuation_text = self._prepare_valuation_text(listing_data)
            
            # Get valuation from OpenAI
            valuation = await self._get_valuation_from_openai(valuation_text)
            
            # Add metadata
            valuation["estimated_at"] = datetime.utcnow().isoformat()
            valuation["listing_url"] = listing_data.get("url", "")
            
            return valuation
            
        except Exception as e:
            logger.error(f"Error estimating value: {e}")
            return {"error": str(e)}
    
    async def compare_values(self, listings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare values across multiple listings
        
        Args:
            listings: List of listing data
            
        Returns:
            Value comparison analysis
        """
        try:
            # Prepare comparison text
            comparison_text = "Compare the values of these listings:\n\n"
            for i, listing in enumerate(listings[:5], 1):  # Limit to 5
                comparison_text += f"Listing {i}:\n"
                comparison_text += self._prepare_valuation_text(listing)
                comparison_text += "\n\n"
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Compare the fair market values of these listings and provide insights in JSON format:
                        {
                            "best_value_deal": "listing number with best value for money",
                            "overpriced_listings": ["list of overpriced listing numbers"],
                            "fair_priced_listings": ["list of fairly priced listing numbers"],
                            "undervalued_listings": ["list of undervalued listing numbers"],
                            "price_range_analysis": "analysis of price distribution",
                            "negotiation_opportunities": ["list of listings with negotiation potential"],
                            "market_trends": "overall market pricing trends"
                        }"""
                    },
                    {
                        "role": "user",
                        "content": comparison_text
                    }
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"error": "Failed to parse comparison"}
                
        except Exception as e:
            logger.error(f"Error comparing values: {e}")
            return {"error": str(e)}
    
    async def get_market_insights(self, product_type: str, location: str = "") -> Dict[str, Any]:
        """
        Get market insights for a product type and location
        
        Args:
            product_type: Type of product (e.g., "iPhone", "laptop")
            location: Location for market analysis
            
        Returns:
            Market insights
        """
        try:
            prompt = f"Provide market insights for {product_type}"
            if location:
                prompt += f" in {location}"
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Provide market insights for the given product and location in JSON format:
                        {
                            "average_price_range": "low-high price range",
                            "price_factors": ["list of factors affecting price"],
                            "market_demand": "high/medium/low",
                            "seasonal_trends": "any seasonal price variations",
                            "negotiation_tips": ["tips for negotiating price"],
                            "red_flags": ["common issues to watch out for"],
                            "recommendations": ["general buying recommendations"]
                        }"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            content = response.choices[0].message.content
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"error": "Failed to parse market insights"}
                
        except Exception as e:
            logger.error(f"Error getting market insights: {e}")
            return {"error": str(e)}
    
    def _prepare_valuation_text(self, listing_data: Dict[str, Any]) -> str:
        """Prepare text for valuation analysis"""
        parts = []
        
        # Basic listing info
        if listing_data.get("title"):
            parts.append(f"Product: {listing_data['title']}")
        
        if listing_data.get("price"):
            parts.append(f"Listed Price: ₹{listing_data['price']}")
        
        if listing_data.get("location"):
            parts.append(f"Location: {listing_data['location']}")
        
        # Analysis data
        if listing_data.get("analysis"):
            analysis = listing_data["analysis"]
            
            if analysis.get("product_type"):
                parts.append(f"Product Type: {analysis['product_type']}")
            
            if analysis.get("brand"):
                parts.append(f"Brand: {analysis['brand']}")
            
            if analysis.get("condition"):
                parts.append(f"Condition: {analysis['condition']}")
            
            if analysis.get("price_analysis"):
                price_analysis = analysis["price_analysis"]
                if price_analysis.get("price_range"):
                    parts.append(f"Price Range: {price_analysis['price_range']}")
                if price_analysis.get("is_negotiable"):
                    parts.append(f"Negotiable: {price_analysis['is_negotiable']}")
            
            if analysis.get("listing_quality"):
                quality = analysis["listing_quality"]
                if quality.get("description_quality"):
                    parts.append(f"Description Quality: {quality['description_quality']}")
                if quality.get("completeness_score"):
                    parts.append(f"Completeness: {quality['completeness_score']}/10")
        
        # Description
        if listing_data.get("description"):
            parts.append(f"Description: {listing_data['description']}")
        
        # Attributes
        if listing_data.get("attributes"):
            parts.append("Attributes:")
            for key, value in listing_data["attributes"].items():
                parts.append(f"  {key}: {value}")
        
        return "\n".join(parts)
    
    async def _get_valuation_from_openai(self, valuation_text: str) -> Dict[str, Any]:
        """Get valuation from OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at valuing used products in the Indian market. 
                        Analyze the listing and provide a fair market value estimate.
                        
                        Return a JSON object with the following structure:
                        {
                            "fair_market_value": "estimated fair market value in INR",
                            "value_range": {
                                "min": "minimum reasonable price",
                                "max": "maximum reasonable price"
                            },
                            "confidence_score": "1-10 confidence in the estimate",
                            "price_analysis": {
                                "is_overpriced": boolean,
                                "is_undervalued": boolean,
                                "price_difference": "difference from listed price"
                            },
                            "factors_considered": ["list of factors that influenced the valuation"],
                            "negotiation_advice": "advice for price negotiation",
                            "market_comparison": "how this compares to similar items"
                        }"""
                    },
                    {
                        "role": "user",
                        "content": f"Estimate the fair market value for this listing:\n\n{valuation_text}"
                    }
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                logger.warning("Failed to parse valuation response as JSON")
                return {"error": "Failed to parse valuation"}
                
        except Exception as e:
            logger.error(f"OpenAI API error in valuation: {e}")
            return {"error": str(e)}
    
    async def batch_valuate_listings(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Valuate multiple listings in batch
        
        Args:
            listings: List of listing data
            
        Returns:
            List of listings with valuations
        """
        valuated_listings = []
        
        for listing in listings:
            try:
                valuation = await self.estimate_value(listing)
                listing["valuation"] = valuation
                valuated_listings.append(listing)
            except Exception as e:
                logger.error(f"Error valuating listing {listing.get('url', 'unknown')}: {e}")
                listing["valuation"] = {"error": str(e)}
                valuated_listings.append(listing)
        
        return valuated_listings


# Global valuation service instance
valuation_service = ValuationService()


async def estimate_value(listing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Estimate value for a single listing"""
    return await valuation_service.estimate_value(listing_data)


async def compare_values(listings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compare values across multiple listings"""
    return await valuation_service.compare_values(listings)


async def get_market_insights(product_type: str, location: str = "") -> Dict[str, Any]:
    """Get market insights for a product type"""
    return await valuation_service.get_market_insights(product_type, location)


async def batch_valuate_listings(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Valuate multiple listings in batch"""
    return await valuation_service.batch_valuate_listings(listings) 