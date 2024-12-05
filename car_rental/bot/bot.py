import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# Токен бота напрямую в файле
TELEGRAM_BOT_TOKEN = "8036773336:AAGe7CEVAB2Pzh8KpQYEINXt78OAPqK-aSU"

# Логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# База данных машин
cars = {
    1: {
        "name": "Toyota Corolla",
        "price": 50,
        "status": "available",
        "features": {
            "color": "Белый",
            "transmission": "Автомат",
            "year": 2020,
        },
        "photo_url": "https://avatars.mds.yandex.net/get-verba/787013/2a000001609d717fcd037b415d00b0ee388c/cattouchret",
    },
    2: {
        "name": "Ford Mustang",
        "price": 100,
        "status": "available",
        "features": {
            "color": "Красный",
            "transmission": "Механика",
            "year": 2018,
        },
        "photo_url": "https://media.ed.edmunds-media.com/ford/mustang/2025/oem/2025_ford_mustang_coupe_dark-horse_fq_oem_1_1600.jpg",
    },
    3: {
        "name": "Tesla Model 3",
        "price": 120,
        "status": "available",
        "features": {
            "color": "Черный",
            "transmission": "Автомат",
            "year": 2021,
        },
        "photo_url": "https://avatars.mds.yandex.net/get-verba/3587101/2a0000018a747aef42d8a776cc3f953ddc33/cattouchret",
    },
    4: {
        "name": "BMW X5",
        "price": 150,
        "status": "available",
        "features": {
            "color": "Синий",
            "transmission": "Автомат",
            "year": 2019,
        },
        "photo_url": "https://media.ed.edmunds-media.com/bmw/x5/2025/oem/2025_bmw_x5_4dr-suv_xdrive40i_fq_oem_1_600.jpg",
    },
}

# Генерация клавиатуры с машинами
def generate_car_buttons():
    keyboard = []
    for car_id, car_info in cars.items():
        status = "✅ Доступно" if car_info["status"] == "available" else "❌ Занято"
        keyboard.append(
            [InlineKeyboardButton(f"{car_info['name']} ({status})", callback_data=f"view_{car_id}")]
        )
    return keyboard


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = "Добро пожаловать в автопрокат! Выберите машину для просмотра характеристик или бронирования:"
    keyboard = generate_car_buttons()
    await update.message.reply_text(welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))

# Обработчик нажатий кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("view_"):
        car_id = int(query.data.split("_")[1])
        car = cars[car_id]
        features = car["features"]
        message = (
            f"**{car['name']}**\n"
            f"Цена: {car['price']}$ в день\n"
            f"Характеристики:\n"
            f"- Цвет: {features['color']}\n"
            f"- Коробка: {features['transmission']}\n"
            f"- Год: {features['year']}\n\n"
            "Нажмите кнопку ниже, чтобы забронировать."
        )
        keyboard = [[InlineKeyboardButton("Забронировать", callback_data=f"book_{car_id}")]]
        await query.message.reply_photo(
            photo=car["photo_url"],
            caption=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif query.data.startswith("book_"):
        car_id = int(query.data.split("_")[1])
        car = cars[car_id]
        car["status"] = "booked"
        await query.edit_message_caption(
            caption=f"Вы успешно забронировали {car['name']} за {car['price']}$ в день.\n"
                    "Список машин обновлен.",
            reply_markup=None,
        )
        keyboard = generate_car_buttons()
        await query.message.reply_text(
            "Обновленный список машин:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

if __name__ == "__main__":
    import asyncio
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Запуск бота в асинхронном режиме
    asyncio.create_task(application.run_polling())  # Запуск polling в текущем цикле событий

