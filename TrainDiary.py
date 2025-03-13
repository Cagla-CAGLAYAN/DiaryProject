from pydantic_ai import Agent, RunContext
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key

class ResponseModel(BaseModel):
    response: str

class TrainDiary:
    def __init__(self):
        self.model_name = 'groq:llama-3.3-70b-versatile'
        self.diary_analysis_agent = Agent(
            model=self.model_name,
            result_type=ResponseModel,
            system_prompt=(
                'You are a diary analyzer. Analyze the input and give your suggestions based on input in plain text. '
                'Do not use tools or structured formats. Output: "Advice based on input."'
            ),
        )

    async def diary_analyze(self, response: str) -> str:
        print(f"Starting async diary analysis for: {response}")
        try:
            result = await self.diary_analysis_agent.run(response)
            print(f"Async analysis result: {result.data.response}")
            return result.data.response
        except Exception as e:
            print(f"Error in async diary analysis: {e}")
            return f"Sorry, I couldn’t analyze your diary due to an error: {e}"

    def diary_analyze_sync(self, response: str) -> str:
        print(f"Starting sync diary analysis for: {response}")
        try:
            result = asyncio.run(self.diary_analyze(response))
            print(f"Sync analysis result: {result}")
            return result
        except Exception as e:
            print(f"Error in sync diary analysis: {e}")
            return f"Error in sync diary analysis: {e}"