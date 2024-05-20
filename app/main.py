import asyncio

from tortoise import run_async

from db.base import tortoise_init
from services.balance_service import BalanceService
from utils.loggers import logger


if __name__ == "__main__":
    run_async(tortoise_init())
    logger.info("Starting balance collection")
    asyncio.run(BalanceService().collect_accounts_data())
