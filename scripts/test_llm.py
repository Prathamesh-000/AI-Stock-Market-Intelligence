from src.nlp.llm_processor import LLMProcessor
import json

def test_llm():
    print("Initializing OpenAI Processor...")
    llm = LLMProcessor()
    
    ticker = "NVDA"
    headline = "Nvidia announces massive delay in next-generation AI chips due to TSMC manufacturing defects, slashing Q4 revenue guidance."
    
    print(f"\nAnalyzing Headline for {ticker}: '{headline}'")
    print("-" * 50)
    
    result = llm.analyze_headline(ticker, headline)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_llm()
