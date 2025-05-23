from openai import OpenAI
import re

class DeepseekManager:



    def find_website(website_texts, company, topic):
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

        print(user_prompt)

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
        


    def analyse_website(html, company, topic):
        user_prompt = (
            f"Company Name: {company}\n\n"
            f"Here is the search html results:\n\n"
            f"{html}\n\n"
            f"What useful information can you gather from the above html element about this Company: {company} for this Use-Case: {topic}? " 
        )   

        client = OpenAI(api_key="sk-13fc4f165342489eb5014647fe67d9a0", base_url="https://api.deepseek.com")     

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a software engineer extracting data about a company from the companies website. "
                        "(Ignore the Auditor of the information) "
                        "Answer in short. Compress Data from Diagrams into short paragraphs summarising the data in a few words, not in a list! "
                        "Only provide useful information about the Use-Case. Label different parts of the answer. "
                        "If there is restricted Data label the paragraph like this '### **Restricted Data**:' and just plainly provide the type of information that is missing, "
                        "like 'Mitarbeiter' or 'Umsatz', nothing else, no '- ' because the information will be used in automated scripts!"
                    )
                },
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )

        content = response.choices[0].message.content.strip()

        # Split the content into restricted_data and general content
        restricted_data = []
        general_content = []

        # Use regex to split content based on '### **Restricted Data**:' header
        pattern = r'### \*\*Restricted Data\*\*:\s*(.*?)(?=(### \*\*Restricted Data\*\*:|$))'
        matches = re.finditer(pattern, content, re.DOTALL)

        # Extract restricted data, excluding the header
        restricted_positions = []
        for match in matches:
            restricted_text = match.group(1).strip()  # Capture only the content after the header
            if restricted_text:  # Only append non-empty text
                restricted_data.append(restricted_text)
            restricted_positions.append((match.start(), match.end()))

        # Extract general content (everything outside restricted data sections)
        if restricted_positions:
            last_end = 0
            for start, end in restricted_positions:
                if last_end < start:
                    general_part = content[last_end:start].strip()
                    if general_part:
                        general_content.append(general_part)
                last_end = end
            if last_end < len(content):
                final_part = content[last_end:].strip()
                if final_part:
                    general_content.append(final_part)
        else:
            general_content.append(content)

        # Combine content, filtering out empty strings
        general_content_str = "\n\n".join([part for part in general_content if part])
        restricted_data_str = "\n\n".join(restricted_data) if restricted_data else ""

        # Return dictionary with proper keys
        return {
            "restricted_data": restricted_data_str,
            "general_content": general_content_str
        }

