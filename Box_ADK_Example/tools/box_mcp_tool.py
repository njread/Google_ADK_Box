import os
import logging
import asyncio
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
MCP_SERVER_URL = "https://api-dev-test.box.com/mcp"
BOX_DEVELOPER_TOKEN = os.getenv("BOX_DEVELOPER_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


async def box_mcp_ask(prompt: str) -> str:
    """
    Sends a prompt to the Box MCP server to get answers based on Box content.

    Args:
        prompt: The question or prompt to ask the MCP server.

    Returns:
        The answer provided by the MCP server, or an error message.
    """
    logger.info(f"Asking Box MCP server: '{prompt}'")
    
    if not BOX_DEVELOPER_TOKEN:
        logger.error("BOX_DEVELOPER_TOKEN environment variable not set")
        return "Error: BOX_DEVELOPER_TOKEN environment variable not set."
    
    if not ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        return "Error: ANTHROPIC_API_KEY environment variable not set."

    try:
        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        
        response = await client.beta.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            mcp_servers=[
                {
                    "type": "url",
                    "url": MCP_SERVER_URL,
                    "name": "box-remote-mcp",
                    "authorization_token": BOX_DEVELOPER_TOKEN,
                }
            ],
            betas=["mcp-client-2025-04-04"]
        )
        
        assistant_response_text = ""
        for content_block in response.content:
            if content_block.type == 'text':
                assistant_response_text += content_block.text
        
        logger.info(f"MCP server response received, length: {len(assistant_response_text)} characters")
        
        if assistant_response_text:
            return assistant_response_text
        else:
            logger.warning("MCP server did not provide an answer")
            return "MCP server did not provide an answer."

    except Exception as e:
        logger.error(f"Error during MCP API call: {e}", exc_info=True)
        return f"An error occurred: {e}"


async def main():
    """Main chat loop for testing the box_mcp_ask function."""
    
    logger.info("Starting MCP chatbot")
    print("Starting MCP chatbot. Type 'quit' or 'exit' to end.")
    
    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            logger.info("Received interrupt signal, exiting")
            print("\nExiting...")
            break
        
        if user_input.lower() in ["quit", "exit"]:
            logger.info("User requested exit")
            print("Exiting...")
            break
        
        if not user_input.strip():
            continue
        
        print("Assistant: ", end="", flush=True)
        
        # Use the box_mcp_ask function
        response = await box_mcp_ask(user_input)
        print(response)


if __name__ == "__main__":
    asyncio.run(main())