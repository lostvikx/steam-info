import os

from langchain.tools import tool
from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# @tool(description="Write ")

google_api_key = os.getenv("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

def main():
    print("Hello from game-info!")


if __name__ == "__main__":
    main()
