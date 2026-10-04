import os
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class NewsIntelligence(BaseModel):
    sentiment: str = Field(description="Strictly 'Positive', 'Negative', or 'Neutral'")
    sentiment_confidence: int = Field(description="Confidence percentage from 0 to 100")
    event_type: str = Field(description="e.g., Earnings, Product Launch, Acquisition, Regulatory, Lawsuit, Management, Dividend, Analyst, Layoffs, Guidance")
    impact_level: str = Field(description="Strictly 'Low', 'Medium', or 'High'")
    impact_score: int = Field(description="Market impact score from 0 to 100")
    novelty: str = Field(description="Strictly 'New', 'Continuation', or 'Duplicate'")
    explanation: str = Field(description="1-2 sentences explaining the rationale for the impact score and event type.")
    sector_ripple_amd: int = Field(default=0, description="Expected market impact on AMD (-100 to 100)")
    sector_ripple_tsm: int = Field(default=0, description="Expected market impact on TSM (-100 to 100)")
    sector_ripple_intc: int = Field(default=0, description="Expected market impact on INTC (-100 to 100)")

class LLMProcessor:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def analyze_headline(self, ticker: str, headline: str) -> dict:
        system_prompt = (
            f"You are an elite quantitative financial analyst. Analyze the following news headline for the stock {ticker}. "
            f"Evaluate the sentiment, determine the core financial event type, assess the novelty, "
            f"predict the market impact (0-100) along with an explanation, and predict the ripple effect "
            f"this news will have on competitors like AMD, TSM, and INTC (-100 to 100)."
        )

        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Headline: {headline}"}
                ],
                response_format=NewsIntelligence,
                temperature=0.0
            )

            result = completion.choices[0].message.parsed.model_dump()
            
            sector_ripple = {
                "AMD": result.get("sector_ripple_amd", 0),
                "TSM": result.get("sector_ripple_tsm", 0),
                "INTC": result.get("sector_ripple_intc", 0)
            }
            
            result["sector_ripple"] = sector_ripple
            return result
            
        except Exception as e:
            return {
                "sentiment": "Neutral",
                "sentiment_confidence": 0,
                "event_type": "Unknown",
                "impact_level": "Low",
                "impact_score": 0,
                "novelty": "Duplicate",
                "explanation": f"LLM API Error: {str(e)}",
                "sector_ripple": {}
            }
