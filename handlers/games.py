import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

active_trivia = {}
active_guess = {}

def register(bot: Client):
    @bot.on_message(filters.command("trivia") & filters.group)
    async def trivia_command(client: Client, message: Message):
        questions = {
            "What is the capital of France?": "Paris",
            "Who painted the Mona Lisa?": "Leonardo da Vinci",
            "What is the largest planet in our solar system?": "Jupiter",
            "Which element has the chemical symbol 'O'?": "Oxygen",
            "Who wrote 'Romeo and Juliet'?": "Shakespeare"
        }
        q, a = random.choice(list(questions.items()))
        active_trivia[message.chat.id] = a
        await message.reply(
            f"**🎮 Trivia Time!**\n\n{q}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 Buzz!", callback_data=f"trivia_{message.chat.id}")
            ]])
        )

    @bot.on_message(filters.command("guess") & filters.group)
    async def guess_command(client: Client, message: Message):
        number = random.randint(1, 100)
        active_guess[message.chat.id] = number
        buttons = []
        row = []
        for i in range(1, 11):
            row.append(InlineKeyboardButton(str(i), callback_data=f"guess_{message.chat.id}_{i}"))
            if len(row) == 5:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        await message.reply(
            f"**🔢 Guess the Number!**\n\nI'm thinking of a number between 1 and 100.\nChoose a number:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    @bot.on_message(filters.command("slots") & filters.group)
    async def slots_command(client: Client, message: Message):
        emojis = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎"]
        result = [random.choice(emojis) for _ in range(3)]
        result_text = " | ".join(result)
        if result[0] == result[1] == result[2]:
            await message.reply(f"**🎰 SLOTS RESULT**\n\n{result_text}\n\n**JACKPOT! You win!** 🎉")
        else:
            await message.reply(f"**🎰 SLOTS RESULT**\n\n{result_text}\n\n**Better luck next time!**")

    @bot.on_callback_query()
    async def game_callback(client: Client, query: CallbackQuery):
        if query.data.startswith("trivia_"):
            chat_id = int(query.data.split("_")[1])
            correct_answer = active_trivia.get(chat_id)
            if correct_answer:
                await query.answer(f"Correct answer: {correct_answer}", show_alert=True)
                del active_trivia[chat_id]
            else:
                await query.answer("Game expired! Start a new one with /trivia", show_alert=True)
        elif query.data.startswith("guess_"):
            parts = query.data.split("_")
            chat_id = int(parts[1])
            guessed = int(parts[2])
            secret = active_guess.get(chat_id)
            if secret is None:
                await query.answer("Game expired! Start a new one with /guess", show_alert=True)
                return
            if guessed == secret:
                await query.message.reply(f"🎉 **Congratulations!** The number was {secret}. You win!")
                del active_guess[chat_id]
            elif guessed < secret:
                await query.answer("Too low! Try again.", show_alert=True)
            else:
                await query.answer("Too high! Try again.", show_alert=True)
