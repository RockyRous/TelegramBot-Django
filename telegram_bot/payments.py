import uuid
import asyncio
from yookassa import Configuration, Payment
from config import YOOKASSA_API_KEY, SHOPLD

Configuration.account_id = SHOPLD
Configuration.secret_key = YOOKASSA_API_KEY


class YookassaGateway:
    def __init__(self, amount: float, description: str, return_url: str ="https://www.example.com/return_url"):
        self.amount = amount
        self.return_url = return_url
        self.description = description

    async def create_payment(self):
        """Создание платежа на Юкасса и возврат URL для оплаты."""
        payment = await self._create_payment_async()
        payment_url = payment.confirmation.confirmation_url
        return payment_url, payment.id

    @staticmethod
    async def check_payment_status(payment_id: str, timeout: int = 60*10, interval: int = 10) -> str:
        """Проверка статуса платежа с таймаутом."""
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed_time = asyncio.get_event_loop().time() - start_time
            if elapsed_time > timeout:
                return "timeout"

            payment = await YookassaGateway._get_payment_status_async(payment_id)
            status = payment.status
            if status == "succeeded":
                return 'succeeded'
            elif status == "canceled":
                return 'canceled'

            # Задержка перед следующим запросом
            await asyncio.sleep(interval)

    async def _create_payment_async(self):
        """Асинхронное создание платежа."""
        payment_data = {
            "amount": {
                "value": self.amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": self.return_url
            },
            "capture": True,
            "description": self.description
        }
        payment = Payment.create(payment_data, uuid.uuid4())
        return payment

    @staticmethod
    async def _get_payment_status_async(payment_id: str):
        """Асинхронное получение статуса платежа."""
        payment = Payment.find_one(payment_id)
        return payment


async def main():
    # Пример использования
    # Используйте карту 5555555555554477 и любые цифры для оплаты (дату больше текущей)
    gateway = YookassaGateway(amount=100.00, description="Заказ №1")

    # Создаем платеж
    payment_url, payment_id = await gateway.create_payment()
    print(f"Ссылка на оплату: {payment_url}")

    # Проверяем статус платежа с таймаутом 10 минут и интервалом 10 секунд
    status = await YookassaGateway.check_payment_status(payment_id, timeout=60*10, interval=10)
    if status == 'succeeded':
        print("Платёж прошёл удачно!")
    elif status == 'canceled':
        print("Платёж был отменён.")
    else:
        print("Тайм-аут проверки статуса платежа.")


if __name__ == "__main__":
    asyncio.run(main())
