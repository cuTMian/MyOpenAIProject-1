from openai import OpenAI

client = OpenAI()

model = "gpt-3.5-turbo"
msg = [{"role":"user", "content":"三国演义讲了一个什么故事"}]

response = client.chat.completions.create(
    model=model,
    messages=msg
)

print(response.choices[0].message.content)
