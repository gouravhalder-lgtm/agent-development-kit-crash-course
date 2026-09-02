from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search

def get_current_time() -> dict:
     """
     Get the current time in the format YYYY-MM-DD HH:MM:SS
     """
     return {
         "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
     }

# Correct callback signature expected by ADK
def inspect_event_stream(callback_context, llm_response):
    try:
        # Check model output for function calls
        if hasattr(llm_response, "content") and llm_response.content:
            for part in getattr(llm_response.content, "parts", []):
                if hasattr(part, "function_call") and part.function_call:
                    print(f"\n🔧 [EVENT STREAM - FUNCTION CALL]: {part.function_call.name}")
                    print(f"   Args: {part.function_call.args}")
    except Exception as e:
        print(f"Inspection error: {e}")
        
    # Crucial: Return None so ADK doesn't override the model's response
    return None

root_agent = Agent(
    name="tool_agent",
    model="gemini-3.6-flash",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get_current_time
    """,
    # tools=[google_search],
      tools=[get_current_time],
    # tools=[google_search, get_current_time], # <--- Doesn't work
      after_model_callback=inspect_event_stream
)
