# services/scheduler.py
"""
APScheduler integration for scheduled sync
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging
from services.sync_service import full_sync_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def start_scheduler(sync_interval_hours: int = 1):
    """Start the scheduler with specified interval"""
    try:
        # Add hourly sync job
        scheduler.add_job(
            func=full_sync_workflow,
            trigger=IntervalTrigger(hours=sync_interval_hours),
            id='hourly_sync',
            name='Hourly transaction sync and budget check',
            replace_existing=True
        )
        
        # Add daily sync job at midnight
        scheduler.add_job(
            func=full_sync_workflow,
            trigger=CronTrigger(hour=0, minute=0),
            id='daily_sync',
            name='Daily transaction sync and budget check',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info(f"Scheduler started with {sync_interval_hours}-hour interval")
        logger.info("Scheduled jobs:")
        for job in scheduler.get_jobs():
            logger.info(f"  - {job.name} (ID: {job.id})")
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")


def stop_scheduler():
    """Stop the scheduler"""
    try:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {str(e)}")

