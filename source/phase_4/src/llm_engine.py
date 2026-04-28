import os
import json
import logging
import sys
from groq import Groq
from dotenv import load_dotenv

# Setup logging for phase_4
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(log_dir, "llm_engine.log"))
    ]
)
logger = logging.getLogger("llm_engine")

class LLMRecommendationEngine:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        """
        Initializes the Groq API client and sets up the System Prompt persona.
        """
        # Try root directory first (four levels up from source/phase_4/src/llm_engine.py)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        env_path_root = os.path.join(root_dir, ".env")
        
        # Try phase_1 directory (previous location)
        env_path_phase1 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "phase_1", ".env")
        
        if os.path.exists(env_path_root):
            load_dotenv(env_path_root)
            logger.info(f"Loaded environment variables from {env_path_root}")
        elif os.path.exists(env_path_phase1):
            load_dotenv(env_path_phase1)
            logger.info(f"Loaded environment variables from {env_path_phase1}")
        else:
            # Try default load_dotenv() which searches upwards
            load_dotenv()
            logger.info("Attempted default load_dotenv() search")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY is not set. Please ensure your .env file is in the root directory or phase_1 folder.")
            
        self.client = Groq(api_key=api_key)
        self.model_name = model_name
        
        # Define System Persona
        self.system_prompt = """You are an expert food concierge. Your goal is to recommend the best restaurants based on the user's specific query.
Rules:
1. ONLY recommend restaurants from the provided "Context Block". Do not hallucinate or suggest outside options.
2. You MUST recommend EXACTLY the number of restaurants available in the context block, up to a maximum of 5. If there are 3-5 restaurants, recommend all of them. If there are more than 5, recommend the top 5 best matches.
3. NEVER recommend the same restaurant twice. Each recommendation must be unique.
4. Keep explanations concise, compelling, and human-like (2-3 sentences each).
5. Output your response ONLY in valid JSON format. The JSON must have a single key "recommendations" containing a list of objects with "name" and "explanation" keys.
Example structure:
{
  "recommendations": [
    {
      "name": "Restaurant Name",
      "explanation": "Brief explanation of why it fits the user's query."
    },
    {
      "name": "Restaurant Name 2",
      "explanation": "Brief explanation of why it fits the user's query."
    }
  ]
}
Do not include any other text, markdown formatting, or preamble. Just valid JSON."""

    def generate_recommendations(self, user_query: str, context_block: str) -> list:
        """
        Sends the user query and pre-filtered context block to the LLM and returns parsed JSON recommendations.
        """
        if not context_block or context_block == "No matching restaurants found.":
            logger.info("No context provided. Skipping LLM call.")
            return []
            
        # Define User Prompt
        user_prompt = f"""User Query: "{user_query}"

Context Block (Available Restaurants):
{context_block}

Remember to return ONLY valid JSON matching the required schema."""

        logger.info(f"Invoking LLM ({self.model_name}) for recommendations...")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model_name,
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=1024,
            )
            
            response_text = chat_completion.choices[0].message.content
            logger.info("Successfully received LLM response.")
            
            # Response Parsing
            try:
                parsed_response = json.loads(response_text)
                recommendations = parsed_response.get("recommendations", [])
                logger.info(f"Parsed {len(recommendations)} recommendations from the LLM.")
                return recommendations
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw Response: {response_text}")
                return []
                
        except Exception as e:
            logger.error(f"Error during LLM invocation: {e}")
            return []

if __name__ == "__main__":
    # Ensure the script doesn't crash immediately if the API key is a placeholder
    if os.getenv("GROQ_API_KEY") and os.getenv("GROQ_API_KEY") != "your_groq_api_key_here":
        engine = LLMRecommendationEngine()
        
        sample_query = "Looking for a romantic Italian place for an anniversary dinner"
        sample_context = '''Name: Chianti, Cuisine: Italian, Rating: 4.5, Cost: 1500, Location: Indiranagar
Name: Truffles, Cuisine: Cafe, American, Rating: 4.7, Cost: 400, Location: Koramangala
Name: Toscano, Cuisine: Italian, Rating: 4.4, Cost: 1200, Location: UB City'''
        
        logger.info("Running test recommendation...")
        results = engine.generate_recommendations(sample_query, sample_context)
        
        print("\n--- LLM Recommendations ---")
        for r in results:
            print(f"Restaurant: {r.get('name')}")
            print(f"Why: {r.get('explanation')}\n")
        print("---------------------------")
    else:
        print("Skipping execution test because GROQ_API_KEY is not configured yet.")
