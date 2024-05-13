import MetaTrader5 as mt5

from utils.schemes import AccountInfoResponse
from db.models import UserData, BalanceData


class BalanceService:
    async def collect_accounts_data(self):
        account_objects = await UserData.all()
        accounts_data = []
        for account in account_objects:
            account_data = await self._get_account_data(
                account_number=int(account.account_number),
                password=account.password,
            )
            accounts_data.append(account_data)

        await BalanceData.bulk_create([
            BalanceData(
                account_number=acc.login,
                created_at=acc.created_at,
                balance=acc.balance,
                equity=acc.equity,
            ) for acc in accounts_data]
        )

    async def _get_account_data(self, account_number: int, password: str):
        try:
            initialized = mt5.initialize(
                login=account_number,
                password=password,
                server="RoboForex-Pro",
            )
            if not initialized:
                print("initialize() failed, error code =", mt5.last_error())

            account_info = mt5.account_info()
            if account_info is not None:
                account_info_dict = mt5.account_info()._asdict()
                account_data = AccountInfoResponse.model_validate(account_info_dict)
                return account_data

        finally:
            mt5.shutdown()
