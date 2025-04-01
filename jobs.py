import schedule
import time
import uuid
from typing import List, Dict, Tuple, Any, Callable, Optional
from datetime import datetime

class JobManager:
    def __init__(self):
        self.jobs_list: List[Dict[str, Any]] = []
        self._running = False
        self._execution_callback: Optional[Callable[[str, datetime], None]] = None

    def set_execution_callback(self, callback: Callable[[str, datetime], None]) -> None:
        """Set a callback function to be called when a job executes."""
        self._execution_callback = callback

    def job(self, job_id: str) -> str:
        """Default job function that prints when executed."""
        current_time = datetime.now()
        execution_message = f"Job {job_id} is running at {current_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
        print(execution_message)  # Keep console output for debugging
        
        # Call the callback if set
        if self._execution_callback:
            self._execution_callback(job_id, current_time)
            
        return job_id

    def get_jobs(self) -> List[Dict[str, Any]]:
        """Returns a list of all scheduled jobs with their IDs and schedule details."""
        job_info_list = []
        for job_item in schedule.get_jobs():
            job_id = None
            interval = None
            unit = None
            for item in self.jobs_list:
                if item['job'] == job_item:
                    job_id = item['id']
                    interval = item['interval']
                    unit = item['unit']
                    break
            job_info_list.append({
                'id': job_id,
                'schedule': str(job_item),
                'interval': interval,
                'unit': unit
            })
        return job_info_list

    def delete_job(self, job_id_to_delete: str) -> Tuple[bool, str]:
        """Deletes a scheduled job by its ID."""
        initial_job_count = len(schedule.get_jobs())
        self.jobs_list = [item for item in self.jobs_list if str(item['id']) != str(job_id_to_delete)]
        schedule.clear()  # Clear all scheduled jobs
        
        # Reschedule remaining jobs
        for job_info in self.jobs_list:
            self._schedule_job(job_info)

        if len(schedule.get_jobs()) < initial_job_count:
            return True, f"Job with ID {job_id_to_delete} deleted successfully."
        return False, f"No job found with ID {job_id_to_delete}."

    def create_job(self, interval: int, unit: str) -> Tuple[bool, str]:
        """Creates a new job to be run at the specified interval and unit."""
        job_id = str(uuid.uuid4())
        
        if unit not in ['seconds', 'minutes', 'hours', 'days', 'weeks']:
            return False, "Invalid time unit. Choose from seconds, minutes, hours, days, weeks."

        job_info = {
            'id': job_id,
            'interval': interval,
            'unit': unit
        }
        
        self._schedule_job(job_info)
        self.jobs_list.append(job_info)
        
        return True, f"Job with ID {job_id} created to run every {interval} {unit}."

    def _schedule_job(self, job_info: Dict[str, Any]) -> None:
        """Helper method to schedule a job based on its parameters."""
        if job_info['unit'] == 'seconds':
            job_info['job'] = schedule.every(job_info['interval']).seconds.do(self.job, job_info['id'])
        elif job_info['unit'] == 'minutes':
            job_info['job'] = schedule.every(job_info['interval']).minutes.do(self.job, job_info['id'])
        elif job_info['unit'] == 'hours':
            job_info['job'] = schedule.every(job_info['interval']).hours.do(self.job, job_info['id'])
        elif job_info['unit'] == 'days':
            job_info['job'] = schedule.every(job_info['interval']).days.do(self.job, job_info['id'])
        elif job_info['unit'] == 'weeks':
            job_info['job'] = schedule.every(job_info['interval']).weeks.do(self.job, job_info['id'])

    def start(self) -> None:
        """Start the job scheduler."""
        self._running = True
        while self._running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self) -> None:
        """Stop the job scheduler."""
        self._running = False

# Create a global instance of JobManager
job_manager = JobManager()

if __name__ == "__main__":
    job_manager.start()