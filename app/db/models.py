from tortoise.models import Model
from tortoise import fields


class UserData(Model):
    account_number = fields.CharField(max_length=512, null=True, blank=True, verbose_name="Номер счета")
    password = fields.CharField(max_length=512, null=True, blank=True, verbose_name="пароль")

    class Meta:
        table = "finance_tariffsubscription"

    def __str__(self):
        return self.account_number


class BalanceData(Model):
    account_number = fields.CharField(max_length=32, null=True, blank=True, verbose_name="Номер счета")
    report_dt = fields.DatetimeField(auto_now_add=True, verbose_name="Время записи")
    balance1 = fields.FloatField(verbose_name="Баланс")
    balance2 = fields.FloatField(verbose_name="Сумма баланса и прибыли или убытков по открытым сделкам")

    class Meta:
        table = "statistics_pilotbalancestatistic"

    def __str__(self):
        return self.account_number
