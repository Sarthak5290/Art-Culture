import os
from dotenv import load_dotenv
import google.generativeai as genai
import wikipedia
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote_plus
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Add a check for the API key and configure genai
if not GOOGLE_API_KEY:
    # In a real app, you might want to log this or show a more prominent warning
    print(
        "Error: GOOGLE_API_KEY not found in environment variables. Story generation disabled."
    )
    GENAI_CONFIGURED = False
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        GENAI_CONFIGURED = True
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        GENAI_CONFIGURED = False


class StoryGenerator:
    def __init__(self):
        self.model = None
        if GENAI_CONFIGURED:
            try:
                # Use a suitable model, 'gemini-pro' is generally available
                self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
            except Exception as e:
                print(f"Error initializing Gemini model: {e}")
                self.model = None

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def search_wikipedia(self, query):
        """Search Wikipedia for information about the art/culture"""
        try:
            # Use wikipedia library directly
            return wikipedia.summary(
                query, sentences=3, auto_suggest=False, redirect=True
            )
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for {query}."
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Wikipedia search for {query} is ambiguous. Possible options: {e.options[:5]}."
        except Exception as e:
            return f"Error searching Wikipedia: {e}"

    def search_web(self, query):
        """Search the web for additional information"""
        try:
            # Using a simplified web search approach for demonstration
            # A more robust approach would use a dedicated search API
            response = requests.get(
                f"https://www.google.com/search?q={quote_plus(query)}+art+history+culture",
                headers=self.headers,
            )
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract relevant text from search results (limiting to snippets)
            snippets = []
            # Use a more general selector for snippets
            for item in soup.select(".g"):
                snippet_element = item.select_one(".VwiC3b")
                if snippet_element:
                    snippets.append(snippet_element.get_text())
            return (
                " ".join(snippets[:3])
                if snippets
                else "No relevant web snippets found."
            )
        except requests.exceptions.RequestException as e:
            return f"Error during web search: {e}"
        except Exception as e:
            return f"An unexpected error occurred during web search: {e}"

    def gather_existing_stories(self, query):
        """Gather existing stories and articles about the art/culture"""
        stories = []
        search_terms = [
            f"{query} story",
            f"{query} history",
            f"{query} cultural significance",
            f"{query} art analysis",
        ]

        for term in search_terms:
            try:
                # Search for articles (using Google News search)
                response = requests.get(
                    f"https://www.google.com/search?q={quote_plus(term)}&tbm=nws",
                    headers=self.headers,
                )
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract news/article results
                # Use a more general selector for news results
                articles = soup.select(".SoaBEf")
                for article in articles[:2]:  # Limit to 2 articles per search term
                    title_element = article.select_one(".n0jPhd")
                    snippet_element = article.select_one(".GI74Re")
                    if title_element and snippet_element:
                        title = title_element.get_text()
                        snippet = snippet_element.get_text()
                        stories.append(f"Title: {title}\nContent: {snippet}\n")

                # Add delay to avoid rate limiting and respect servers
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"Error during news search for {term}: {e}")
                continue
            except Exception as e:
                print(
                    f"An unexpected error occurred during news search for {term}: {e}"
                )
                continue

        return "\n".join(stories) if stories else "No existing stories found."

    def generate_story_content(self, art_name):
        """Generate a story using the gathered information using Gemini"""
        if not self.model:
            return "Story generation is not available due to missing API key or model initialization failure."

        # Gather information
        wiki_info = self.search_wikipedia(art_name)
        web_info = self.search_web(art_name)
        existing_stories = self.gather_existing_stories(art_name)

        # Create prompt for story generation
        prompt = f"""
Create a compelling story about {art_name} using the following information:

Wikipedia Information:
{wiki_info}

Additional Web Information:
{web_info}

Existing Stories and Articles:
{existing_stories}

Please create a well-structured story that:
1. Introduces the art/culture
2. Explains its historical significance
3. Describes its cultural impact
4. Includes interesting facts and details
5. Concludes with its modern relevance

Format the story in a clear, engaging narrative style.
Incorporate relevant information from the existing stories while maintaining originality.
"""

        try:
            # Generate story using Gemini
            response = self.model.generate_content(prompt)
            # Check if response has text attribute and is not empty
            if hasattr(response, "text") and response.text.strip():
                return response.text
            else:
                return "Gemini generated an empty response."
        except Exception as e:
            return f"Error generating story with Gemini: {e}"


# Instantiate the generator (singleton pattern for Streamlit)
# This will load environment variables and configure the API once
story_generator_instance = None


def get_story_generator():
    global story_generator_instance
    if story_generator_instance is None:
        story_generator_instance = StoryGenerator()
    return story_generator_instance


def generate_story(title):
    """Generate a story for the given title using the StoryGenerator.
    This is the function called from item_detail.py"""
    generator = get_story_generator()
    # Simulate latency moved inside the actual generation call if needed, or keep for effect
    # time.sleep(2)
    # Ensure generator is initialized before calling generate_story_content
    if generator and generator.model:
        return generator.generate_story_content(title)
    else:
        return (
            "Story generation is not available. Please check API key and configuration."
        )
