import discord
from discord.ext import commands
import os
from model import load_model

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

SAVE_DIR = 'downloaded_images'
os.makedirs(SAVE_DIR, exist_ok=True)


@bot.event
async def on_ready():
    print(f'Бот вошёл как {bot.user}')

@bot.command()
async def img(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("**Прикрепите фото , а не файл.**")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.content_type.startswith('image/'):
        await ctx.send("❌ **Прикрепите верное фото.**")
        return

    image_data = await attachment.read()
    image_path = os.path.join(SAVE_DIR, f'downloaded_image_{attachment.filename}')
    with open(image_path, 'wb') as f:
        f.write(image_data)

    class_name, confidence_score = load_model('model.savedmodel', 'labels.txt', image_path)

    if confidence_score < 0.6:
        await ctx.send("🤔 **Я не уверен, что на фото.**")
    else:
        embed = discord.Embed(title="Результат классификации", color=0x00ff00)
        embed.add_field(name="Класс", value=class_name, inline=True)
        embed.add_field(name="Уверенность", value=f"{confidence_score:.2f}", inline=True)
        embed.set_thumbnail(url=attachment.url)
        await ctx.send(embed=embed)

bot.run('sus')

