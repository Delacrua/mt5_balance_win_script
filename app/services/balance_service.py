import MetaTrader5 as mt5

from utils.loggers import logger
from utils.schemes import AccountInfoResponse
from db.models import UserData, BalanceData
from settings import settings


class BalanceService:
    async def collect_accounts_data(self):
        try:
            account_objects = await UserData.all()
        except Exception as exc:
            logger.error(
                "Exception occurred while getting accounts data: %s",
                str(exc),
            )
        else:
            accounts_data = []

            #  unable to use asyncio.gather as it requires MT5 client to be logged in to connect to server
            for account in account_objects:
                account_data = await self._get_account_data(
                    account_number=int(account.account_number),
                    password=account.password_vps,
                )
                if account_data is not None:
                    logger.info(f"Fetched account balance: %s", account_data)
                    accounts_data.append(account_data)

            if accounts_data:
                logger.info(f"Saving balance data for accounts: %s", [acc.login for acc in accounts_data])
                await BalanceData.bulk_create(
                    [
                        BalanceData(
                            account_number=acc.login,
                            report_dt=acc.created_at,
                            balance1=acc.balance,
                            balance2=acc.equity,
                        )
                        for acc in accounts_data
                    ]
                )

    async def _get_account_data(self, account_number: int, password: str) -> AccountInfoResponse | None:
        logger.info("Fetching account balance data for account number %s", account_number)
        try:
            initialized = mt5.initialize(
                login=account_number,
                password=password,
                server=settings.SERVER,
            )
            if not initialized:
                logger.error(
                    "mt5 initialize failed for account number %s, error code = %s.",
                    account_number,
                    mt5.last_error(),
                )

            account_info = mt5.account_info()
            if account_info is not None:
                account_info_dict = mt5.account_info()._asdict()
                account_data = AccountInfoResponse.model_validate(account_info_dict)
                return account_data
            else:
                logger.error("No account balance data found for account number %s", account_number)
        except Exception as exc:
            logger.error(
                "Exception occurred while fetching account balance data for account number %s. Exception: %s",
                account_number,
                str(exc),
            )

        finally:
            mt5.shutdown()
