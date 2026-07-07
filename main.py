import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7638663833
CODE = "14889933556677"
PHOTO = "https://i.ibb.co/jZvgj6Bs/image.png"


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer_photo(
        photo=PHOTO,
        caption=(
            "🔐 <b>Код разблокировки</b>\n\n"
            "Получите персональный код после оплаты.\n\n"
            "🖼 Пример результата показан выше.\n\n"
            "⭐ Стоимость: <b>50 Telegram Stars</b>\n"
            "⚡ Выдача происходит автоматически."
        ),
        parse_mode="HTML"
    )

    await message.answer_invoice(
        title="Код разблокировки",
        description="Моментальное получение кода после оплаты.",
        payload="unlock_code",
        provider_token="",
        currency="XTR",
        prices=[
            LabeledPrice(
                label="Код разблокировки",
                amount=50
            )
        ]
    )


@dp.pre_checkout_query()
async def checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)


@dp.message(F.successful_payment)
async def payment(message: Message):

    user = message.from_user

    await message.answer(
        f"🎉 <b>Оплата прошла успешно!</b>\n\n"
        f"🔑 Ваш код:\n\n"
        f"<code>{CODE}</code>\n\n"
        f"Сохраните его.",
        parse_mode="HTML"
    )

    await bot.send_message(
        ADMIN_ID,
        f"💰 <b>Новая покупка</b>\n\n"
        f"👤 {user.full_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"📎 @{user.username if user.username else 'нет'}\n\n"
        f"🔑 Код: <code>{CODE}</code>",
        parse_mode="HTML"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())