# Autonomous Research Notifier Agent

A Flask-based web application that provides an AI-powered assistant capable of managing scheduled jobs. The assistant can create, delete, and monitor scheduled tasks through a natural language interface.

## Features

- 🤖 AI-powered assistant using Gemini 1.5 Flash
- 📅 Job scheduling system with support for various time intervals
- 🔒 Secure login system
- 💬 Natural language interface for job management
- 📊 Real-time job execution monitoring

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A Google Cloud API key for Gemini AI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/autonomous-research-notifier-agent.git
cd autonomous-research-notifier-agent
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```env
USERNAME=your_username
PASSWORD=your_password
GOOGLE_API_KEY=your_google_api_key
```

## Running the Application

### Local Development

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

### Production Deployment

The application is configured to run on Heroku using the following Procfile:
```
web: flask run --host=0.0.0.0 --port=$PORT
```

## Usage

1. Log in using your credentials
2. Navigate to the chat interface
3. Use natural language to interact with the assistant. Examples:
   - "Create a job that runs every 5 minutes"
   - "Show me all scheduled jobs"
   - "Delete job with ID abc123"

## Job Scheduling

The application supports the following time units:
- seconds
- minutes
- hours
- days
- weeks

## Project Structure

```
autonomous-research-notifier-agent/
├── app.py              # Main Flask application
├── agent.py           # AI agent implementation
├── jobs.py            # Job management system
├── templates/         # HTML templates
│   ├── login.html
│   └── chat.html
├── static/           # Static files (CSS, JS)
├── requirements.txt  # Python dependencies
└── Procfile         # Heroku deployment configuration
```

## Development

### Adding New Features

1. The AI agent's capabilities are defined in `agent.py` using the `@agent.tool` decorator
2. Job management logic is handled in `jobs.py`
3. Web interface is managed in `app.py` and the templates directory

### Testing

To test the application locally:
1. Start the Flask server
2. Create a test job with a short interval
3. Monitor the console for job execution messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask web framework
- Google Gemini AI
- Schedule library for job management 