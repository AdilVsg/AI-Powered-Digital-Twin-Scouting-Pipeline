import os
import json
import time
from src.github_scraper import GithubScraper
from src.rdm_keywords import generate_keywords

OUTPUT_FILE = "data/dataset_final.jsonl"
MAX_REPOS_PER_KEYWORD = 10  # Start small for testing (increase to 50 or 100 later)

def save_repo_to_jsonl(repo_data, filename):
    """Saves a repository line by line (crash-safe approach)"""
    with open(filename, 'a', encoding='utf-8') as f:
        json.dump(repo_data, f, ensure_ascii=False)
        f.write('\n')

def main():
    print("Starting Digital Twin Data Mining...")
    
    # 1. Check API Tokens
    groq_key = os.getenv("GROQ_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not groq_key:
        print("Warning: GROQ_API_KEY is not set. Keyword expansion will be disabled.")
    if not github_token:
        print("Warning: GITHUB_TOKEN is not set. Scraping will be severely rate-limited.")
        
    # 2. Keyword Preparation
    base_keywords = ["Digital Twin", "Cyber-Physical System", "Digital Shadow"]
    print(f"\nBase keywords: {base_keywords}")
    
    # Ask AI to generate additional keywords
    try:
        ai_keywords = generate_keywords(base_keywords)
        # Merge both lists and remove duplicates
        all_keywords = list(set(base_keywords + ai_keywords))
    except Exception as e:
        print(f"AI Error, proceeding with base keywords only. Details: {e}")
        all_keywords = base_keywords

    print(f"Final keyword list ({len(all_keywords)} keywords): {all_keywords}")
    print("-" * 50)

    # 3. Initialize Scraper
    scraper = GithubScraper(token=github_token)
    
    # Create data directory if it does not exist
    os.makedirs('data', exist_ok=True)

    # Load already processed IDs (to avoid duplicate scraping on restart)
    seen_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    repo = json.loads(line)
                    seen_ids.add(repo['id'])
                except:
                    pass
        print(f"Resuming: {len(seen_ids)} repositories already in the database.")

    # 4. Main Mining Loop
    total_new = 0
    
    for kw in all_keywords:
        print(f"\nProcessing keyword: '{kw}'")
        
        # Execute the search
        results = scraper.search_repositories([kw], max_repos=MAX_REPOS_PER_KEYWORD)
        
        for repo in results:
            repo_id = repo['id']
            
            # Check if it is a new repository
            if repo_id not in seen_ids:
                # Add useful metadata: which keyword found this repo
                repo['search_query'] = kw 
                
                # Immediate save to file
                save_repo_to_jsonl(repo, OUTPUT_FILE)
                
                seen_ids.add(repo_id)
                total_new += 1
                print(f" Saved: {repo['name']}")
            else:
                print(f" Ignored duplicate: {repo['name']}")
                
        # Short pause to respect API rate limits between keywords
        time.sleep(2)

    print("\n" + "="*30)
    print(f"FINISHED! {total_new} new repositories added.")
    print(f"Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()