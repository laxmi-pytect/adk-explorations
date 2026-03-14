import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session, InMemorySessionService 
from google.genai import types
from google.adk.runners import Runner
from typing import List, Dict


import os
from dotenv import load_dotenv

load_dotenv()
model_name = os.getenv("MODEL")

filepaths=os.getenv("FILEPATH")



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepaths}/adk-exploration/genai_service_account.json"


# Helper function to load an image from a local file path
def load_image_from_file(path: str) -> types.Part:
    """Load image from file and return a types.Part object."""
    with open(path, 'rb') as f:
        image_bytes = f.read()
    
    if path.lower().endswith('.png'):
        mime_type = 'image/png'
    elif path.lower().endswith(('.jpg', '.jpeg')):
        mime_type = 'image/jpeg'
    else:
        mime_type = 'image/jpeg' # Default

    return types.Part(
        inline_data=types.Blob(data=image_bytes, mime_type=mime_type)
    )


class MultimodelAnalyzer:

    def __init__(self):
        """Initialize product catalog analyzer."""
        self.catalog: List[Dict] = []
        app_name = "visual-catalog"
        self.catalog_agent = Agent(
            model='gemini-2.5-flash', name='catalog_agent',
            instruction="You are a product catalog writer. Analyze the provided image and generate a compelling marketing description. The image will be provided as part of the user's message."
        )

        # Create the session service and the runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            session_service=self.session_service,
            agent=self.catalog_agent,
            app_name=app_name
        )

    async def analyze_product(self, product_id: str, image_path: str):
        """Analyze a product image and create a catalog entry."""
        print(f"\n--- Analyzing Product: {product_id} ---")

        session = await self.session_service.create_session(app_name="visual-catalog", user_id="user1")

        image_part =load_image_from_file(image_path)

        # Combine image and text into a single message
        analysis_message = types.Content(
            role="user",
            parts=[image_part, types.Part(text="explain this image")]
        )

        catalog_text = ""
        async for event in self.runner.run_async(session_id=session.id, new_message=analysis_message, user_id="user1"):
            if event.content and event.content.parts:
                catalog_text += event.content.parts[0].text

        print(f"✅ Catalog Entry Generated:\n{catalog_text}\n")

        self.catalog.append({'product_id': product_id, 'catalog_entry': catalog_text}) 


async def main():

    ### define agent and invoke ###
    analyzer = MultimodelAnalyzer()

    product_list=[
        ('howarts-houses.jpg',f'{filepaths}/adk-exploration/multimodal_agent/imgs/howarts-houses.jpg'),
        ('wand1.jfif',f'{filepaths}/adk-exploration/multimodal_agent/imgs/wand1.jfif')
    ]



    for product_id, img_path in product_list:

        print(f"\n--- Analyzing Product: {product_id} --at --{img_path}")
        await analyzer.analyze_product(product_id, img_path)
        await asyncio.sleep(1)   




if __name__ == "__main__":
    asyncio.run(main())
    