from src.groq_client import client

response = client.chat.completions.create(

    model="llama-3.3-70b-versatile",

    messages=[

        {
            "role": "user",
            "content": "Reply with only: Groq Working"
        }

    ]

)

print(response.choices[0].message.content)