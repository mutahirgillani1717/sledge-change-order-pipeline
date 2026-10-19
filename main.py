import json
import pdfplumber
from src.extractor import ChangeOrderExtractor

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

if __name__ == "__main__":
    # Ensure Ollama is running locally before executing
    pipeline = ChangeOrderExtractor(model_name="llama3")
    
    # Example raw text (In production, you'd pass the extract_text_from_pdf output)
    sample_text = """
    CHANGE ORDER #104
    Project: Downtown Metro Station Renovation
    Date: October 15, 2026
    Description: Upgrading HVAC ducting due to unforeseen structural beams.
    Cost Impact: Add $15,500.00
    Time Extension: 4 days
    """
    
    print("Processing document...")
    result_json = pipeline.extract(sample_text)
    
    print("\nValidated JSON Output:")
    print(json.dumps(result_json, indent=2))