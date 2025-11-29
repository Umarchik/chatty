from aiogram import Router, types
from .service import AntispamService

router = Router()

@router.message()
async def check_spam(message: types.Message):
    service = AntispamService()
    result = await service.check_message(message.text, user_id=message.from_user.id)

    if result.is_spam:
        await message.delete()
        await message.answer(f"🚫 Обнаружен спам ({result.rule})", reply=False)
