from pydantic_ai import Agent, RunContext
from jobs import job_manager

system_prompt = """
You are a helpful assistant that can answer questions and help with tasks.
You can create, delete, and get scheduled jobs.

To create a job, use the create_job tool with an interval (number) and unit (seconds, minutes, hours, days, or weeks).
To delete a job, use the delete_job tool with the job ID.
To list all jobs, use the get_jobs tool.

Example commands:
- "Create a job that runs every 5 minutes"
- "Delete job with ID abc123"
- "Show me all scheduled jobs"
"""

agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt=system_prompt,
)

@agent.tool
def create_job(ctx: RunContext[str], interval: int, unit: str):
    """
    Create a job with the given interval and unit.
    """
    success, message = job_manager.create_job(interval, unit)
    return message

@agent.tool
def delete_job(ctx: RunContext[str], job_id: str):
    """
    Delete a job with the given job ID.
    """
    success, message = job_manager.delete_job(job_id)
    return message

@agent.tool
def get_jobs(ctx: RunContext[str]):
    """
    Get all jobs.
    """
    jobs = job_manager.get_jobs()
    if not jobs:
        return "No jobs are currently scheduled."
    
    response = "Current scheduled jobs:\n"
    for job in jobs:
        response += f"- Job ID: {job['id']}\n"
        response += f"  Schedule: {job['schedule']}\n"
        response += f"  Interval: {job['interval']} {job['unit']}\n"
    return response

def process_message(message: str) -> str:
    """
    Process a message and return the agent's response.
    This function can be used by both CLI and web interface.
    """
    try:
        result = agent.run_sync(message)
        return result.data
    except Exception as e:
        return f"Error during processing: {e}"