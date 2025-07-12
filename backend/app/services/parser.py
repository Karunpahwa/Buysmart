"""
Parser Service for analyzing listing responses
Uses OpenAI API to extract structured data from listing text
"""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
import openai
from ..config.settings import settings
from ..models.listing import Listing

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.openai_api_key


class ParserService:
    """Service for parsing and analyzing listing data using OpenAI"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def analyze_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a listing and extract structured information
        
        Args:
            listing_data: Raw listing data from scraper
            
        Returns:
            Analyzed listing data with extracted information
        """
        try:
            # Prepare text for analysis
            text_content = self._prepare_text_content(listing_data)
            
            # Analyze with OpenAI
            analysis = await self._analyze_with_openai(text_content)
            
            # Combine original data with analysis
            result = {
                **listing_data,
                "analysis": analysis,
                "parsed_at": datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing listing: {e}")
            return listing_data
    
    async def analyze_multiple_listings(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple listings in batch
        
        Args:
            listings: List of raw listing data
            
        Returns:
            List of analyzed listings
        """
        analyzed_listings = []
        
        for listing in listings:
            try:
                analyzed = await self.analyze_listing(listing)
                analyzed_listings.append(analyzed)
            except Exception as e:
                logger.error(f"Error analyzing listing {listing.get('url', 'unknown')}: {e}")
                analyzed_listings.append(listing)  # Keep original if analysis fails
        
        return analyzed_listings
    
    def _prepare_text_content(self, listing_data: Dict[str, Any]) -> str:
        """Prepare text content for OpenAI analysis"""
        content_parts = []
        
        # Title
        if listing_data.get("title"):
            content_parts.append(f"Title: {listing_data['title']}")
        
        # Description
        if listing_data.get("description"):
            content_parts.append(f"Description: {listing_data['description']}")
        
        # Price
        if listing_data.get("price"):
            content_parts.append(f"Price: ₹{listing_data['price']}")
        
        # Location
        if listing_data.get("location"):
            content_parts.append(f"Location: {listing_data['location']}")
        
        # Attributes
        if listing_data.get("attributes"):
            for key, value in listing_data["attributes"].items():
                content_parts.append(f"{key}: {value}")
        
        # Posted date
        if listing_data.get("posted_date"):
            content_parts.append(f"Posted: {listing_data['posted_date']}")
        
        return "\n".join(content_parts)
    
    async def _analyze_with_openai(self, text_content: str) -> Dict[str, Any]:
        """Analyze text content using OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at analyzing online marketplace listings. 
                        Extract structured information from the listing text and provide insights.
                        
                        Return a JSON object with the following structure:
                        {
                            "product_type": "string",
                            "brand": "string or null",
                            "model": "string or null",
                            "condition": "new/used/refurbished",
                            "price_analysis": {
                                "is_negotiable": boolean,
                                "price_range": "low/medium/high",
                                "market_value": "estimated market value"
                            },
                            "seller_analysis": {
                                "seller_type": "individual/dealer",
                                "response_time": "fast/medium/slow",
                                "reliability_score": 1-10
                            },
                            "listing_quality": {
                                "photos_count": number,
                                "description_quality": "poor/fair/good/excellent",
                                "completeness_score": 1-10
                            },
                            "red_flags": ["list of potential issues"],
                            "recommendations": ["list of suggestions"]
                        }"""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this OLX listing:\n\n{text_content}"
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse response
            content = response.choices[0].message.content
            import json
            try:
                analysis = json.loads(content)
                return analysis
            except json.JSONDecodeError:
                logger.warning("Failed to parse OpenAI response as JSON")
                return {"error": "Failed to parse analysis"}
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {"error": str(e)}
    
    async def extract_key_information(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key information from listing for quick analysis
        
        Args:
            listing_data: Listing data
            
        Returns:
            Extracted key information
        """
        try:
            text_content = self._prepare_text_content(listing_data)
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Extract key information from this listing in JSON format:
                        {
                            "product_name": "string",
                            "price": "number or null",
                            "condition": "new/used/refurbished",
                            "location": "string",
                            "seller_type": "individual/dealer",
                            "key_features": ["list of key features"],
                            "urgency": "low/medium/high"
                        }"""
                    },
                    {
                        "role": "user",
                        "content": text_content
                    }
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"error": "Failed to parse key information"}
                
        except Exception as e:
            logger.error(f"Error extracting key information: {e}")
            return {"error": str(e)}
    
    async def compare_listings(self, listings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple listings and provide insights
        
        Args:
            listings: List of listing data
            
        Returns:
            Comparison analysis
        """
        try:
            # Prepare comparison text
            comparison_text = "Compare these listings:\n\n"
            for i, listing in enumerate(listings[:5], 1):  # Limit to 5 for analysis
                comparison_text += f"Listing {i}:\n"
                comparison_text += self._prepare_text_content(listing)
                comparison_text += "\n\n"
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Compare these listings and provide insights in JSON format:
                        {
                            "best_value": "listing number with best value",
                            "price_comparison": "analysis of price differences",
                            "quality_comparison": "analysis of listing quality",
                            "recommendations": ["list of recommendations"],
                            "market_insights": "overall market analysis"
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
            logger.error(f"Error comparing listings: {e}")
            return {"error": str(e)}


# Global parser service instance
parser_service = ParserService()


async def analyze_listing(listing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a single listing"""
    return await parser_service.analyze_listing(listing_data)


async def analyze_multiple_listings(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze multiple listings"""
    return await parser_service.analyze_multiple_listings(listings)


async def extract_key_information(listing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key information from listing"""
    return await parser_service.extract_key_information(listing_data)


async def compare_listings(listings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compare multiple listings"""
    return await parser_service.compare_listings(listings) 