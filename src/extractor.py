import json
import logging
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser
from src.schema import ChangeOrderOutput

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# ... (leave the rest of the code exactly the same)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChangeOrderExtractor:
    def __init__(self, model_name: str = "llama3"):
        """
        Initializes the extractor using a local LLM via Ollama for zero-cost, secure inference.
        """
        self.llm = OllamaLLM(model=model_name, temperature=0.0)       
        self.parser = PydanticOutputParser(pydantic_object=ChangeOrderOutput)
        
        self.prompt = PromptTemplate(
            template="You are an expert data extraction algorithm reading construction change orders.\n"
                     "Extract the required fields from the text below.\n"
                     "If a field is missing, output null for the value and 0.0 for confidence.\n"
                     "Assign a confidence score between 0.0 and 1.0 based on text clarity.\n\n"
                     "{format_instructions}\n\n"
                     "Raw Document Text:\n{text}\n",
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.chain = self.prompt | self.llm | self.parser

    def extract(self, text: str) -> dict:
        logger.info("Initiating extraction pipeline...")
        if not text or len(text.strip()) < 10:
            logger.warning("Input text is empty or too short.")
            return ChangeOrderOutput().model_dump()
            
        try:
            result = self.chain.invoke({"text": text})
            logger.info("Extraction completed successfully.")
            return result.model_dump()
        except Exception as e:
            logger.error(f"Pipeline extraction failed: {e}")
            return ChangeOrderOutput().model_dump()