from openai import OpenAI
import os


def generate_keywords(input_keywords):
    """
    Uses the configured LLM to generate additional technical keywords.
    """
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: The GROQ_API_KEY environment variable is not set.")
        return []

    client = OpenAI(
        base_url = "https://api.groq.com/openai/v1",
        api_key = api_key
    )
    
    keywords_str =", ".join(input_keywords)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert in software engineering and Digital Twins."
                },
                {
                    "role": "user", 
                    "content": f"Based on these keywords: {keywords_str}.\n"
                               f"Generate a list of 15 NEW specific keywords or technologies (in English) relevant for finding GitHub repositories on this topic.\n"
                               f"Expected format: Only the keywords separated by commas. No bullet points."
                }
            ],
            temperature=0.7,
        )

        # Retrieval and cleaning
        raw_text = response.choices[0].message.content
        # Split by comma and remove unnecessary spaces around words
        new_keywords = [word.strip() for word in raw_text.split(',')]
        
        print(f"Generation successful: {len(new_keywords)} new keywords.")
        return new_keywords

    except Exception as e:
        print(f"Error during the API call: {e}")
        return []
    
# Test zone
if __name__ == "__main__":
    test = ["Digital Twin", "IoT"]
    print(generate_keywords(test))