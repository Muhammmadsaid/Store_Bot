from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import DB_NAME
from keyboards.admin_inline_keyboards import categories_kb_4_products
from states.admin_states import ProductStates, ProductState
from utils.database import Database

product_router = Router()
db = Database(DB_NAME)


@product_router.message(Command('add_product'))
async def add_product_handler(message: Message, state: FSMContext):
    await state.set_state(ProductStates.add_SelectCategoryProdState)
    await message.answer(
        text="Please choose a category which you want to add product",
        reply_markup=categories_kb_4_products()
    )


@product_router.callback_query(ProductStates.add_SelectCategoryProdState)
async def add_product_category_handler(query: CallbackQuery, state: FSMContext):
    await state.update_data(product_category=query.data)
    await state.set_state(ProductStates.add_TitleProdState)
    await query.message.answer("Please, send title for your product...")
    await query.message.delete()


@product_router.message(ProductStates.add_TitleProdState)
async def add_product_title_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(product_title=message.text)
        await state.set_state(ProductStates.add_TextProdState)
        await message.answer("Please,send full description text for you product:")
    else:
        await message.answer("Please, send only text...")


@product_router.message(ProductStates.add_TextProdState)
async def add_product_text_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(product_text=message.text)
        await state.set_state(ProductStates.add_ImageProdState)
        await message.answer("Please,send photo for you product:")
    else:
        await message.answer("Please, send only text...")


@product_router.message(ProductStates.add_ImageProdState)
async def add_product_image_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(product_image=message.photo[-1].file_id)
        await state.set_state(ProductStates.add_PriceProdState)
        await message.answer("Please,send you product's price:")
    else:
        await message.answer("Please, send only photo...")


@product_router.message(ProductStates.add_PriceProdState)
async def add_product_price_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(product_price=int(message.text))
        await state.set_state(ProductStates.add_PhoneProdState)
        await message.answer("Please,send phone number for contact with you:")
    else:
        await message.answer("Please, send only numbers...")


@product_router.message(ProductStates.add_PhoneProdState)
async def add_product_title_handler(message: Message, state: FSMContext):
    if message.text or message.contact:
        phone = message.text if message.text else message.contact.phone_number
        all_date = await state.get_data()
        print(all_date)
        result = db.add_product(
            title=all_date.get('product_title'),
            text=all_date.get('product_text'),
            image=all_date.get('product_image'),
            price=all_date.get('product_price'),
            phone=phone,
            cat_id=all_date.get('product_category'),
            u_id=message.from_user.id
        )
        if result:
            await message.answer("Your product successfully added!")
            product = db.get_my_last_product(message.from_user.id)
            await message.answer_photo(
                photo=product[3],
                caption=f"<b>{product[1]}<b/>\n\n<b>{product[2]}<b/>\n\nPrice:{product[4]}\n\nContact: {product[-1]}"
            )
        else:
            await message.answer("Something went wrong,please try again!")
        await state.clear()
    else:
        await message.answer("Please, send only text...")
