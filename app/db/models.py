from tortoise.models import Model
from tortoise import fields


class Tariff(Model):
    name = fields.CharField(max_length=50, verbose_name="Наименование тарифа")

    class Meta:
        table = "finance_tariff"

    def __str__(self):
        return self.name


class UserData(Model):
    account_number = fields.CharField(max_length=512, null=True, blank=True, verbose_name="Номер счета")
    password = fields.CharField(max_length=512, null=True, blank=True, verbose_name="пароль")
    tariff = fields.relational.ForeignKeyField("models.Tariff", on_delete=fields.CASCADE, verbose_name="Тариф")

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
