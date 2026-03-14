##from google.adk.agents.llm_agent import Agent
import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv()
model_name = os.getenv("MODEL")

filepaths=os.getenv("FILEPATH")



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepaths}/adk-exploration/genai_service_account.json"



root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

async def main():
    app_name="soccer_info_buddy"

    user_id_1 = 'user1'

    # 3. Define Your Agent
    root_agent = Agent(
        model=model_name,
        name="soccer_runner_agent",
        description="A helpful assistant for user questions related to soccer",
        instruction="Answer questions.",
    )

    # 4. Create a Runner
    runner = InMemoryRunner(
        agent=root_agent,
        app_name=app_name,
    )
     # 5. Create a session
    my_session = await runner.session_service.create_session(
        app_name=app_name, user_id=user_id_1
    )
     # 6. Prepare a function to package a user's message as
    # genai.types.Content, run it asynchronously, and iterate
    # through the response 
    async def run_prompt(session: Session, new_message: str):
        content = types.Content(
                role='user', parts=[types.Part.from_text(text=new_message)])
        
        print('** User says:', content.model_dump(exclude_none=True))
        
        async for event in runner.run_async(user_id=user_id_1,session_id=session.id,new_message=content,):
            if event.content.parts and event.content.parts[0].text:
                print(f'** {event.author}: {event.content.parts[0].text}')
        
    # 7. Use this function on a new query
    query = "What is golden boot  in soccer?"
    await run_prompt(my_session, query)




if __name__ == "__main__":
    asyncio.run(main())




