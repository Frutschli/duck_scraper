from ollama import chat

def analyse_website_text(website_text, organisation):
    title = website_text.get('title', '')
    url = website_text.get('href', '')
    description = website_text.get('body', '')

    print(f"\nWebsite_Title: {title}\nWebsite_URL: {url}\nWebsite_Description: {description}\n")
    print(f"Organisation: {organisation}")
    print("Thinking...")

    user_prompt = (
        f"Company Name from Excel: {organisation}\n"
        f"Search Result Title: {title}\n"
        f"Search Result URL: {url}\n"
        f"Search Result Description: {description}\n\n"
        "Does the search result likely match the company name? Just answer 'Yes!' or 'No!'."
    )

    try:
        response = chat(
            model='llama3.2:3b',
            messages=[
                {
                    'role': 'system',
                    'content': "You are a software engineer checking if a search result matches a company. "
                               "Answer with 'Yes!' if you think it's a match, 'No!' otherwise."
                },
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ],
            options={'temperature': 0}
        )

        reply = response['message']['content'].strip()
        print(f"LLM Response: {reply}")

        if reply == "Yes!":
            return True
        elif reply == "No!":
            return False
        else:
            print(f"⚠️ Unexpected response: {reply}")
            return None  # or raise an exception if you prefer

    except Exception as e:
        print(f"❌ Error during LLM analysis: {e}")
        return None
