import asyncio

from tortoise import run_async

from db.base import tortoise_init
from services.balance_service import BalanceService


if __name__ == "__main__":
    run_async(tortoise_init())
    asyncio.run(BalanceService().collect_accounts_data())
