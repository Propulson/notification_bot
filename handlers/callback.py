from aiogram import Router, types
from keyboards.inline import get_inline_actions

router = Router()

@router.callback_query(lambda callback: callback.data == "rating")
async def handle_rating_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("⭐️ <b>Ваш рейтинг:</b> 5.0\n\nСпасибо за использование бота!",
                                   parse_mode="HTML")

@router.callback_query(lambda callback: callback.data == "subscribe")
async def handle_subscribe_callback(callback: types.CallbackQuery):
    await callback.answer("✅ Вы подписались на обновления!", show_alert=True)

@router.callback_query(lambda callback: callback.data == "contact")
async def handle_contact_callback(callback: types.CallbackQuery):
    await callback.message.answer("📞 Для связи: @username")

@router.callback_query(lambda callback: callback.data == "confirm")
async def handle_confirm_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("✅ Действие подтверждено!",
                                   reply_markup=get_inline_actions())

@router.callback_query(lambda callback: callback.data == "cancel")
async def handle_cancel_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Действие отменено!",
                                   reply_markup=get_inline_actions())

@router.callback_query(lambda callback: callback.data == "refresh")
async def handle_refresh_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("🔄 Данные обновлены!\n\nТекущее время: ...",
                                   reply_markup=get_inline_actions())

@router.callback_query(lambda callback: callback.data == "settings")
async def handle_settings_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("⚙️ <b>Настройки:</b>\n\nИспользуйте команду /keyboard для основных настроек",
                                   parse_mode="HTML",
                                   reply_markup=get_inline_actions())