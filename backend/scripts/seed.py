"""
Database Seeding Script.

Execution script to trigger the database seeder from the command line.
Usage: python -m scripts.seed
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add backend to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal, init_db, close_db
from app.db.seeder import seed_curriculum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Initialize DB connection and run seeder."""
    logger.info("Starting database seeder...")
    
    # Initialize DB connection pool
    await init_db()
    
    try:
        # Create a session and run the seeder
        async with SessionLocal() as session:
            await seed_curriculum(session)
    except Exception as e:
        logger.error(f"Seeding failed: {e}")
        raise
    finally:
        # Close DB connection pool
        await close_db()
        
    logger.info("Seeding script finished.")


if __name__ == "__main__":
    asyncio.run(main())
