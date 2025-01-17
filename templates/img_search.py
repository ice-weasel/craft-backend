from langchain_core.messages import HumanMessage
import base64, httpx
from langchain_groq import ChatGroq
import getpass
import os


# Initialize the model
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = "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"

model = ChatGroq(
    model="llama-3.2-11b-vision-preview",

)
# Download and encode the image
fruits = ['https://storage.googleapis.com/vectrix-public/fruit/apple.jpeg',
          'https://storage.googleapis.com/vectrix-public/fruit/banana.jpeg',
          'https://storage.googleapis.com/vectrix-public/fruit/kiwi.jpeg',
          'https://storage.googleapis.com/vectrix-public/fruit/peach.jpeg',
          'https://storage.googleapis.com/vectrix-public/fruit/plum.jpeg']
image_data = base64.b64encode(httpx.get(fruits[0]).content).decode("utf-8")

# Create a message with the image
message = HumanMessage(
    content=[
        {"type": "text", "text": "describe the fruit in this image"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
    ],
)

# Invoke the model with the message
response = model.invoke([message])

# Print the model's response
print(response.content)