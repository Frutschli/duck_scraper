from ollama import chat

class OllamaClient:

    def analyse_website_text(website_text, organisation):

        search_summary = f"""
        Title: {website_text.get('title')}
        URL: {website_text.get('href')}
        Description: {website_text.get('body')}
        """
        print("Thinking...")

        response = chat(
            model = 'llama3.2:3b',
            messages=[
                {'role': 'system', 'content':"You are a software engeneer analysing website results. Also answer in shot"},
                {'role': 'user', 'content': "Here is the search result for the company" + str(organisation) + ", is this the actual website of the company?: " + str(search_summary)},
            ],
            options={'temperature': 0}
        )
        print(response['message']['content'])