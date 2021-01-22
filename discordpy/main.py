import discord
from discord import member
from discord.ext import commands
import datetime
from discord.utils import get
import random

client = commands.Bot( command_prefix = '$' )
client.remove_command( 'help' )
#$

#words
hello_Words = [ 'hello', 'hi', 'привет', 'здарова', 'ку', 'q', 'privet', 'приветик', 'приветики', 'qq' ]
answer_Words = [ 'узнать сведенья о сервере', 'узнать, что здесь можно делать?', 'что здесь делать?', 'команды', 'скажи команды' ]
goobye_Words = [ 'bye', 'пока', 'досвидос', 'покедова', 'goodbye', 'до свидания', 'я пошёл' ]
bad_words = [ 'блять','урод', 'сука', 'нахуй','пидора ответ', 'иди в жопу','пидорас' 'пиздуй', 'еби', 'привет упырь','Нахуй тебя послать', 'упырь', 'еблан', 'пизда', 'хуй', 'бляха муха', 'ты даун', 'лох']
number = ['50']
role2 = ['VIP', 'Гость']
#words

#command line

@client.event
async def on_ready():
    activity = discord.Game(name="иди нахуй богдан", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")

#command line

#ex pass
@client.event
async def on_command_error( ctx, error ):
    pass


#clear
@client.command( pass_context = True )
@commands.has_any_role( 'Создатель','Надзиратель','Главный модер' )

async def clear( ctx, amount : int ):
    await ctx.channel.purge( limit = amount )
#clear

#clear error
@clear.error
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( f'{ctx.author.name}, обязательно укажите число!' )

    if isinstance( error,  commands.MissingPermissions):
        await ctx.send( f'{ctx.author.name}, у вас недостаточно прав!')
#clear error  

#play
@client.command( pass_content = True )

async def play( ctx, message ):
    numberOfTrites = 0
    while True:
        Number = random.random() * 100 + 1
        guess = await ctx.author.send(await ctx.send('напишите число от 1 до 100:'))
        guess = message.content.lower()
        if guess in number:
            while guess != Number:
                if guess < Number:
                    await ctx.send('Загаданое число больше, попробуй ещё раз')
                if guess > Number:
                    await ctx.send('Загаданное число меньше, попробуй ещё раз')
                else:
                    await ctx.send(guess +  'Правильный ответ!')
                numberOfTrites = numberOfTrites + 1
            await ctx.send('число попыток'  + numberOfTrites)
#play 

# @client.command( pass_context = True )
# @commands.has_any_role( 'Создатель','Надзиратель','Главный модер' )

# async def text(ctx,*args):
#     emb = discord.Embed( title = 'Навигация по командам ', colour = discord.Color.red() )


@commands.command()
async def guilds(self, ctx):
    if ctx.author.id == 590044748321128459: #сюда ваш id
        emb = discord.Embed(title = 'GameServer;3', color = discord.Color.green())
        for guild in self.client.guilds:
            if not guild.system_channel is None:
                channel = guild.system_channel
                link = await channel.create_invite()
            else:
                link = 'Отсутствует'
            emb.add_field(name = f'{guild.name}', value = f"Овнер - {guild.owner}\nИнвайт - {link}", inline = False)
        await ctx.send(embed = emb)
    else:
        await ctx.send('у вас нет доступа к этой команде!')
        
#kick
@client.command( pass_context = True )
@commands.has_any_role( 'Создатель','Надзиратель','Главный модер' )

async def kick( ctx, member: discord.Member, *, reason = None ):
    emb = discord.Embed( title = 'Kick', colour = discord.Color.red() )
    await ctx.channel.purge( limit = 1 )

    await member.kick( reason = reason )

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = 'Kick user' , value = 'Kick user : {}'.format( member.mention ) )
    emb.set_footer( text = 'был кикнут GameServerAdmin по команде администратора {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url )

    await ctx.send( embed = emb )
#kick

#ban
@client.command( pass_context = True )
@commands.has_any_role( 'Создатель','Надзиратель','Главный модер' )

async def ban( ctx, member: discord.Member, *, reason = None ):
    emb = discord.Embed( title = 'Ban', colour = discord.Color.red() )
    await ctx.channel.purge( limit = 1 )

    await member.ban( reason = reason )

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = 'Baned user', value = 'Baned user : {}'.format( member.mention ) )
    emb.set_footer( text = 'был забанен securityBOT по команде аминистратора {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url )
    
     
async def send_m( ctx, member: discord.Member ):
    await member.send( f'{member.name}, ты забанен на Games Server' )
#ban
    
#unban
@client.command( pass_context = True )
@commands.has_any_role( 'Создатель','Надзиратель','Главный модер' )

async def unban( ctx, *, member ):
    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )
        await ctx.send(f'user { member.mention } was unban ')

        return
#unban

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get( client.voice_clients, guild = ctx.guild )

    if voice and voice.is_connected(): 
        await voice.move_to( channel )
    else:
        voice = await channel.connect()
        await ctx.send( f'Бот присоединился к каналу: {channel}' )


@client.command()
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get( client.voice_clients, guild = ctx.guild )

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send( f'Бот отсоединился от канала : {channel}' )

#chat
@client.event
async def on_message( message ):
    await client.process_commands( message )

    msg = message.content.lower()

    if msg in hello_Words:
        await message.channel.send( 'Привет, чего хотел?😀' )
    
    if msg in answer_Words:
        await message.channel.send( 'Пропиши команду $help, и ты всё узнаешь)' )

    if msg in goobye_Words:
        await message.channel.send( 'Пока-пока, было приятно с тобой общаться🙂' )
    #badwords
    if msg in bad_words:
        await message.delete()
        await message.author.send( f'{message.author.name}, нельзя писать плохие слова!' )
        await message.channel.send( 'нельзя писать плохие слова!' )
    #badwords
#chat

#mute
@client.command( pass_context = True )
@commands.has_any_role( 'Создатель','Надзиратель','Главный модер' )

async def mute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )
    

    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Mute' )

    await member.add_roles( mute_role )
    await ctx.send( f'У {member.mention} ограничение чата. за нарушение!' )
#mute

@client.event

async def role( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    mute_role = discord.utils.get( ctx.message.guild.roles, name = role )

    await member.add_roles( mute_role )
    await ctx.send('.........')


@commands.command( pass_context = True ) # начало команды
@commands.has_any_role( 'Создатель','Надзиратель','Главный модер' ) # нужны права администратора? - да
async def ar(self, ctx, autoroles): #сама команда и что ей надо указать, это prefix, комаду и НАЗВАНИЕ роли.
    for guild in self.bot.guilds: # оно ищет на сервере людей
        for member in guild.members: # и тут делается все работа для member-a
            autoroles2 = discord.utils.get(ctx.message.guild.roles, name = autoroles) # нахождение айди по названию, иначе будет ошибка(у меня)
            await member.add_roles(autoroles2) # само добавление роли
    emb = discord.Embed(description = 'Роли успешно добавлены ВСЕМ участникам Discord сервера.')
    await ctx.send(embed = emb) # теперь бот сообщает что всё вышло.

#unmute
@client.command( pass_context = True )
@commands.has_any_role( 'Создатель','Надзиратель','Главный модер' )

async def unmute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Mute' )

    await member.remove_roles( mute_role )
    await ctx.send( f'У {member.mention} ограничение чата убрано' )
#unmutes

#roles
@client.event

async def on_member_join( member ):
    channel = client.get_channel( 754328009758081034 )

    role = discord.utils.get( member.guild.roles, name = 'новичёк' )

    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'Пользователь ``{member.name}``, присоединился к нам!', color = 'red') )
#roles

#time
@client.command( pass_context = True )

async def time( ctx ):
    emb = discord.Embed( title = 'Точное время', colour = discord.Color.red(), url = 'https://www.timeserver.ru/cities/ru/ufa' )

    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer( text = 'спасибо за то использовали GameServerAdmin')
    emb.set_thumbnail( url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRnZtsxKrQP2yz033xiRu4NmtboJ8oeLjX6kg&usqp=CAU' )
    
    now_date = datetime.datetime.now()

    emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ))


    await ctx.send( embed = emb )
#time

#help
@client.command( pass_context = True )

async def help( ctx ):
    emb = discord.Embed( title = 'Навигация по командам ', colour = discord.Color.red() )

    emb.add_field( name = '{}clear'.format( '$' ), value = 'Очистка чата ($clear) через пробел можно указать сколько очистить сообщений до 100 (доступно только администрации!!!)' )
    emb.add_field( name = '{}kick'.format( '$' ), value = 'Кик ($kick) после команды через пробел нужно сделать упоменание @(кого кикнуть) (доступно только администрации!!!)' )
    emb.add_field( name = '{}ban'.format( '$' ), value = 'Бан ($ban)  после команды через пробел нужно сделать упоменание @(кого забанить) и можно через пробел указать причину (доступно только администрации!!!)' )
    emb.add_field( name = '{}unban'.format( '$' ), value = 'Разбанить ($unban) после команды через пробел нужно сделать упоменание @(кого разбанить) (доступно только администрации!!!)' )
    emb.add_field( name = '{}mute'.format( '$' ), value = 'Замутить можно с помощью команды ($mute) после команды через пробел нужно сделать упоменание @(кого замутить) (доступно только администрации!!!)' )
    emb.add_field( name = '{}time'.format( '$' ), value = 'Посмотреть точное время можно с помощю команды ($time) доступно всем)))' )

    emb.set_footer( text = 'спасибо за то использовали GameServerAdmin')
    await ctx.send( embed = emb )
#help

#connect
token = open( 'token.txt', 'r' ).readline()

client.run(token)
#connect

#await ctx.author.send()
#heroku
#console.cloud.google.com
#pythonanywhere.com