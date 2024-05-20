import asyncio

from tortoise import run_async

from db.base import tortoise_init
from services.balance_service import BalanceService
from utils.loggers import logger


if __name__ == "__main__":
    try:
        run_async(tortoise_init())
        logger.info("Starting balance collecting")
        asyncio.run(BalanceService().collect_accounts_data())
        logger.info("Finished balance collecting")
    except Exception as exc:
        logger.critical("An unexpected error occurred while running script: %s", str(exc))
