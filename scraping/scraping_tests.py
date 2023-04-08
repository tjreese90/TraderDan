import os

openai.organization = "org-1IQk4WTMCXA9V1m8mPeiZtD2"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()