# Google ADK Box Integration

## Overview

This repository demonstrates the integration between Google's Agent Development Kit (ADK) and Box's content management platform. The integration enables AI-powered agents to interact with Box content, providing intelligent document management capabilities through a flexible and customizable framework.

## Key Features

- **Document Access**: Retrieve, list, and search documents stored in Box
- **Content Analysis**: Analyze document content using Google's AI capabilities
- **Metadata Management**: View and modify Box file metadata using ADK agents
- **Workflow Automation**: Create automated workflows between Box and other systems
- **Multi-Agent Architecture**: Utilize specialized agents for different Box-related tasks

## Prerequisites

- Python 3.9+
- Google ADK (Agent Development Kit) installed
- Box Developer account with API credentials
- Google Cloud account (for Vertex AI integration, optional but recommended)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/njread/Google_ADK_Box.git
   cd Google_ADK_Box
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # Or for Windows:
   # .venv\Scripts\activate.bat  # CMD
   # .venv\Scripts\Activate.ps1  # PowerShell
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Fill in your Box API credentials and Google Cloud configuration

## Project Structure

```
Google_ADK_Box/
├── Box_ADK_Example/
│   ├── __init__.py
│   ├── agent.py                   # Main agent definition
│   ├── tools/                     # Box API integration tools
│   │   ├── __init__.py
│   │   ├── box_generic_search.py  # Box API function tools
│   │   └── box_AI_ask.py          # Helper utilities
│   └── sub_agents/                # Specialized agents
│   |    ├── Box_hub_agent.py
│   |   └── Box_search_agent.py
|   |
|   └── agents/           # example google agents
├── .env.example          # Example environment variables
├── README.md             # This file
```

## Box API Tools

The integration includes several tools to interact with Box content:

- Document retrieval and searching
- File upload and download
- Metadata operations
- Content analysis 
- Collaboration management

## Usage

### Running the Agent Locally

1. Navigate to the parent directory:
   ```bash
   cd Google_ADK_Box
   ```

2. Start the ADK development server:
   ```bash
   adk web
   ```

3. Open your browser and navigate to the provided URL (typically http://localhost:8000)

4. Select the Box_ADK_Example agent from the dropdown menu to start interacting with it

### Example Interactions

The agent can handle queries like:

- "Find all documents in my Box account related to Q3 financials"
- "Summarize the contents of the file 'Project Proposal.docx'"
- "Upload this spreadsheet to my Box account and share it with the finance team"
- "Extract key information from my recent Box documents about customer feedback"

## Authentication

This integration uses Box OAuth 2.0 for authentication. The agent will guide users through the authentication process if needed, or you can pre-configure authentication in the `.env` file.

## Development

### Adding New Box Tools

1. Create a new function in `tools/box_tools.py`
2. Register the function as a tool in the agent definition
3. Update the agent instructions to include the new capability

### Testing

Run the test suite:
```bash
pytest tests/
```

## Deployment

This agent can be deployed to Google Cloud using the ADK deployment tools:

```bash
adk deploy cloud_run
```

See the ADK documentation for detailed deployment instructions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Acknowledgements

- Google Agent Development Kit (ADK) team
- Box Platform API
