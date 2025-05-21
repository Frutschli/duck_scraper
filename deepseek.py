from openai import OpenAI

def deepseek_chat(website_texts, company, topic):
    formatted_results = ""

    for i, website_text in enumerate(website_texts, start=1):
        title = website_text.get('title', '')
        url = website_text.get('href', '')
        description = website_text.get('body', '')
        formatted_results += (
            f"Result {i}:\n"
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Description: {description}\n\n"
        )

    user_prompt = (
        f"Company Name: {company}\n\n"
        f"Here are the search results:\n\n"
        f"{formatted_results}"
        f"Which of these websites would you click to get more information about: {company} for this Use-Case: {topic}? "
        "If you need further information, reply with 'show more search results'. "
    )

    client = OpenAI(api_key="sk-13fc4f165342489eb5014647fe67d9a0", base_url="https://api.deepseek.com") 

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a software engineer checking if a search result matches a company. "
                                            "Reply only with 'show more search results' OR '[URL of the matching website]'"},
            {"role": "user", "content": user_prompt},
        ],
        stream=False
    )   

    content = response.choices[0].message.content.strip()
    print(content)  

    if content.lower() == "show more search results":
        return False, None
    else:
        content = content.removeprefix("[URL of the matching website] ").strip()
        return True, content