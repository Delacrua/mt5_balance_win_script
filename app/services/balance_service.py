import MetaTrader5 as mt5

from utils.loggers import logger
from utils.schemes import AccountInfoResponse
from db.models import UserData, BalanceData
from settings import settings


class BalanceService:
    async def collect_accounts_data(self):
        try:
            account_objects = await UserData.all().select_related("tariff")
            acc_mapping = {acc.account_number: acc for acc in account_objects if acc.id == 855}
        except Exception as exc:
            logger.error(
                "Exception occurred while getting accounts data: %s",
                str(exc),
            )
        else:
            accounts_data = []

            #  unable to use asyncio.gather as it requires MT5 client to be logged in to connect to server
            for account in acc_mapping.values():
                if not (account.password and account.account_number):
                    logger.error(
                        "Wrong account number format or no password for account number %s",
                        account.account_number,
                    )
                    continue
                try:
                    account_data = await self._get_account_data(
                        account_number=int(account.account_number),
                        password=account.password,
                    )
                    if account_data is not None:
                        logger.info(f"Fetched account balance: %s", account_data)
                        accounts_data.append(account_data)
                except Exception as exc:
                    logger.error(
                        "Exception occurred while processing account %s data: %s",
                        account.account_number,
                        str(exc),
                    )
            if accounts_data:
                logger.info(
                    f"Saving balance data for accounts: %s",
                    [acc.login for acc in accounts_data],
                )
                await BalanceData.bulk_create(
                    [
                        BalanceData(
                            account_number=acc.login,
                            report_dt=acc.created_at,
                            balance1=(
                                acc.balance / 1000
                                if acc_mapping[str(acc.login)].tariff.name == "Pilot Base"
                                else acc.balance
                            ),
                            balance2=(
                                acc.equity / 1000
                                if acc_mapping[str(acc.login)].tariff.name == "Pilot Base"
                                else acc.equity
                            ),
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
                logger.error(
                    "No account balance data found for account number %s",
                    account_number,
                )
        except Exception as exc:
            logger.error(
                "Exception occurred while fetching account balance data for account number %s. Exception: %s",
                account_number,
                str(exc),
            )

        finally:
            mt5.shutdown()
