import requests
import time

class GithubScraper:
    def __init__(self, token=None):
        """
        Initializes the scraper with a GitHub token.
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
            print("Authentication enabled.")
        else:
            print("Warning: Unauthenticated mode (rate-limited).")

    def get_readme(self, owner, repo_name):
        """
        Retrieves the raw text of a repository's README file.
        """
        url = f"{self.base_url}/repos/{owner}/{repo_name}/readme"
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.raw" # Raw format
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception:
            return None

    def search_repositories(self, keywords, max_repos=5):
        """
        Searches for repositories using a list of keywords and retrieves their READMEs.
        Parameter 'max_repos': Limits the number of results per keyword.
        """
        all_results = []
        seen_ids = set() 
        
        # If 'keywords' is a single string, convert it to a list
        if isinstance(keywords, str):
            keywords = [keywords]

        for kw in keywords:
            # Build the URL
            url = f"{self.base_url}/search/repositories"
            params = {
                'q': kw,
                'sort': 'stars',
                'order': 'desc',
                'per_page': max_repos 
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    items = response.json().get('items', [])
                    
                    for item in items:
                        repo_id = item['id']
                        
                        if repo_id not in seen_ids:
                            # Retrieve the README
                            readme_text = self.get_readme(item['owner']['login'], item['name'])
                            
                            if readme_text:
                                all_results.append({
                                    'id': repo_id,
                                    'name': item['name'],
                                    'url': item['html_url'],
                                    'description': item['description'],
                                    'readme': readme_text,
                                    'keyword_source': kw
                                })
                                seen_ids.add(repo_id)
                            # else: No README found, ignore the repository
                            
                elif response.status_code == 403 or response.status_code == 429:
                    print("API rate limit reached. Sleeping for 60 seconds...")
                    time.sleep(60)
                else:
                    print(f"API error on '{kw}': {response.status_code}")
                    
            except Exception as e:
                print(f"Technical error: {e}")
                
        return all_results