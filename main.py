import discord
from discord.ext import commands,tasks
import asyncio
import datetime
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

id_do_servidor = 1117960978559156268

bot = commands.Bot(command_prefix='<', intents=intents)
voice_check_interval = 180 


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    check_voice_channels.start()



# ================ Comando de teste ================
@bot.command()
@commands.has_permissions(administrator=True)
async def teste(ctx):
    await ctx.send('Estou funcionando!')



# ================ Boas vindas ================
@bot.event
async def on_member_join(member):
  guild = member.guild
  canal = discord.utils.get(guild.channels, id=1118342090506649680)
  
  embed = discord.Embed(
        title=f'Bem vindo(a) {member.name}#{member.discriminator}!',
        description="Olá! Você acabou de entrar no servidor! Aqui você poderá fazer novas amizades, jogar, conversar sobre programação, tecnologia e muito mais!!",
        color=discord.Color.blue()
    )
  
  embed.add_field(name='Importante!', value='Conheça todas as regras do servidor para não ter nenhum problema em  :scroll:丨regras')
  embed.add_field(name='Primeiros passos', value='Para receber um cargo siga as instruções em   :first_place:丨cargos')
  embed.add_field(name='Apresente-se!', value='Conte um pouco mais sobre você em    :microphone:丨apresentação')
  await canal.send(embed=embed)



# ================ <chamarstaff ================
@bot.command()
async def chamarstaff(ctx):
    canal_comandos = 1122237219529314364  
    canal_chamados_staff = 1122928890466271362 

    if ctx.channel.id != canal_comandos:
        return 

    admin_role = discord.utils.get(ctx.guild.roles, name='Staff CT')

    embed = discord.Embed(title='Chamado de Staff', description='', color=discord.Color.purple())
  
    embed.add_field(name='Você chamou um staff!', value='Aguarde, em breve um staff entrará em contato com você', inline=False)
    embed.set_thumbnail(url=bot.user.avatar.url)

    await ctx.send(embed=embed)

  
    staff_channel = bot.get_channel(canal_chamados_staff)
    if staff_channel:
        embed = discord.Embed(title='Chamado de Staff', description='Um membro pediu a presença de um staff!', color=discord.Color.purple())
      
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.add_field(name='Canal', value=ctx.channel.name, inline=False)

        author_mention = ctx.author.mention
        embed.add_field(name='Autor do Chamado', value=author_mention, inline=False)

        admin_mention = admin_role.mention if admin_role else 'Nenhum administrador encontrado'
        embed.add_field(name='Administrador', value=admin_mention, inline=False)

        await staff_channel.send(embed=embed)




# ================ Resposta do bot ao ser mencionado ================
# @bot.event(ctx)
# async def on_message(message):
#     if bot.user.mentioned_in(message):
#         user_mention = message.author.mention

#         embed = discord.Embed(
#             title=f"Olá {user_mention}! Me chamou?",
#             description="Como posso ajudar você?",
#             color=discord.Color.purple()
#         )

#         embed.set_thumbnail(url=bot.user.avatar_url)
#         embed.add_field(name="Sobre", value="Para saber mais sobre mim, digite <sobregrivy no canal 🤖┃comandos-grivy", inline=False)
#         embed.add_field(name="Staff", value="Para chamar um membro da equipe, digite <chamarstaff no canal 🤖┃comandos-grivy", inline=False)

#         await message.channel.send(embed=embed)

#     await bot.process_commands(message)

# @bot.event
# async def on_message(message):
#     if bot.user in message.mentions:
#         await message.channel.send("Você me mencionou! Em que posso ajudar?")

#     await bot.process_commands(message)










# ================ Mensagem quando alguém apaga mensagem ================
@bot.event
async def on_message_delete(message):
    if message.author == bot.user:  
        return
    canal = bot.get_channel(1121797027127365662)

    embed = discord.Embed(
        title="Mensagem Apagada",
        description=f"Uma mensagem foi apagada.",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=message.author.avatar.url)
  
    embed.add_field(name="Autor", value=f"{message.author.mention}", inline=True)
    embed.add_field(name="Canal", value=f"{message.channel.mention}", inline=True)
    embed.add_field(name="Conteúdo", value=f"{message.content}", inline=False)

    await canal.send(embed=embed)




# ================ <anunciar ================
@bot.event
@commands.has_permissions(administrator=True)
async def on_message(message):
    if message.content == "<anunciar" and not message.author.bot and message.author.guild_permissions.administrator:
        await message.channel.send("Digite o anúncio que deseja fazer:")
        
        def check(m):
            return m.author == message.author and m.channel == message.channel
        
        try:
            response = await bot.wait_for("message", check=check, timeout=180)
            
            canal_anuncios = discord.utils.get(message.guild.channels, id=1121558643221995630)
            
            embed = discord.Embed(
                title="Anúncio",
                description=response.content,
                color=discord.Color.purple()
            )
            
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"Anunciado por {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar.url)
            
            await canal_anuncios.send(embed=embed)
        
        except asyncio.TimeoutError:
            await message.channel.send("Tempo limite excedido. O anúncio foi cancelado.")
    
    await bot.process_commands(message)



# ================ <textobot ================
@bot.command()
@commands.has_permissions(administrator=True)
async def textobot(ctx):
    await ctx.send("Em qual canal você deseja enviar o texto? Por favor, mencione o canal ou forneça o ID.")

    def check_channel(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        channel_response = await bot.wait_for("message", check=check_channel, timeout=180)
        channel_mention = channel_response.content.strip()

        channel_id = None
        if channel_mention.startswith("<#") and channel_mention.endswith(">"):
            channel_id = channel_mention[2:-1]
        elif channel_mention.isdigit():
            channel_id = channel_mention

        if channel_id:
            channel = bot.get_channel(int(channel_id))
        else:
            await ctx.send("Canal inválido. Certifique-se de mencionar corretamente ou fornecer um ID válido.")
            return

        if channel is None:
            await ctx.send("Canal não encontrado. Certifique-se de mencionar um canal existente.")
            return
    except asyncio.TimeoutError:
        await ctx.send("Tempo limite excedido. O comando foi cancelado.")
        return

    await ctx.send("Qual título você deseja para o embed?")

    try:
        title_response = await bot.wait_for("message", check=check_channel, timeout=180)
        title = title_response.content.strip()

        await ctx.send("Qual descrição você deseja para o embed?")

        description_response = await bot.wait_for("message", check=check_channel, timeout=180)
        description = description_response.content.strip()

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.purple()
        )

        await channel.send(embed=embed)
        await ctx.send("Texto enviado com sucesso!")
    except asyncio.TimeoutError:
        await ctx.send("Tempo limite excedido. O comando foi cancelado.")
        return



# ================ <sobregrivy ================
@bot.command()
async def sobregrivy(ctx):
    embed = discord.Embed(
        title="Um pouco sobre mim",
        description="Olá! Meu nome é **Grivy** e sou um bot criado em Python.\n"
                    "Fui criado para um trabalho da aula de Programação e Algoritmo na Etec.\n"
                    "Os alunos responsáveis pela minha criação foram:\n"
                    "Victor da Silva Teixeira, Robson Henrique Moura Machado, Isabel Mayumi Yafuso, Yasmin Arcanjo Martins e Guilherme Valton Franca de Oliveira!", color=discord.Color.purple()
    )

    embed.set_thumbnail(url=bot.user.avatar.url)
    
    await ctx.send(embed=embed)




# ================ Comando de apagar categorias ================
@bot.command()
@commands.has_permissions(administrator=True)
async def apagar_categoria(ctx, categoria_nome: str):
    for categoria in ctx.guild.categories:
        if categoria.name == categoria_nome:
            for canal in categoria.channels:
                await canal.delete()
            await categoria.delete()
            await ctx.send(f'A categoria {categoria.name} foi apagada.')
            return
    await ctx.send('A categoria especificada não foi encontrada.')




# ================ Comando de apagar mensagens ================
@bot.command()
@commands.has_permissions(administrator=True)
async def limpar(ctx, quantidade: int = None):
    if quantidade is None:
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("Digite a quantidade de mensagens que deseja limpar:")

        try:
            mensagem = await bot.wait_for("message", check=check, timeout=30.0)
            quantidade = int(mensagem.content)
        except asyncio.TimeoutError:
            return await ctx.send("Tempo limite excedido. Comando cancelado.")
        except ValueError:
            return await ctx.send("Quantidade inválida. Comando cancelado.")

    author_mention = ctx.author.mention
    messages = await ctx.channel.purge(limit=quantidade + 1)
    deleted_messages = len(messages) - 1
    await ctx.send(f'{deleted_messages} mensagens foram limpas por {author_mention}.')



# ================ O bot checa se ele está sozinho na call para sair ================
@tasks.loop(seconds=voice_check_interval)
async def check_voice_channels():
    for voice_client in bot.voice_clients:
        if voice_client.is_playing() or voice_client.is_paused():
            continue 

        if len(voice_client.channel.members) == 1:  
            await asyncio.sleep(voice_check_interval)
            if len(voice_client.channel.members) == 1: 
                await voice_client.disconnect()
                await voice_client.channel.send("Fui desconectado da chamada de voz porque não há mais membros presentes.")



# ================ Comando de entrar na call ================
@bot.command()
async def puxar(ctx):
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em uma chamada de voz para usar esse comando.')
        return

    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_disconnected():
        await voice_client.move_to(voice_channel)
    else:
        await voice_channel.connect()

    await ctx.send(f'Conectado à chamada de voz em "{voice_channel}".')


# ================ Comando de tirar da call ================
@bot.command()
async def tirar(ctx):
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em uma chamada de voz para usar esse comando.')
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.channel.id == ctx.author.voice.channel.id:
        await voice_client.disconnect()
        await ctx.send('Desconectado da chamada de voz.')
    else:
        await ctx.send('Desculpe, mas eu não estou na mesma chamada de voz que você.')



# ================ Comandos para a apresentação ================
@bot.command()
@commands.has_permissions(administrator=True)
async def iniciar(ctx):
    current_hour = datetime.datetime.now().hour

    if 6 <= current_hour < 12:
        greeting = 'Bom dia!'
    elif 12 <= current_hour < 18:
        greeting = 'Boa tarde!'
    else:
        greeting = 'Boa noite!'
    
    
    await ctx.send(f'{greeting} pessoal! Tudo bem com vocês?\n**Vamos começar!**')



# ================ Comando de criar categorias ou canais ================
@bot.command()
@commands.has_permissions(administrator=True)
async def criar(ctx):
    await ctx.send("O que você deseja criar?\n[Categoria | Canal]")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        resposta = await bot.wait_for('message', check=check, timeout=60)

        if resposta.content.lower() == 'categoria':
            while True:
                await ctx.send("Qual o nome da categoria que deseja criar?")
                nome_categoria = await bot.wait_for('message', check=check, timeout=60)

                categoria = discord.utils.get(ctx.guild.categories, name=nome_categoria.content)
                if categoria:
                    await ctx.send("Já existe uma categoria com esse nome. Escolha outro nome.")
                else:
                    await ctx.guild.create_category(nome_categoria.content)
                    await ctx.send(f"A categoria {nome_categoria.content} foi criada com sucesso!")
                    break

        elif resposta.content.lower() == 'canal de texto':
            while True:
                await ctx.send("Qual o nome do canal de texto que deseja criar?")
                nome_canal = await bot.wait_for('message', check=check, timeout=60)

                canal_texto = discord.utils.get(ctx.guild.channels, name=nome_canal.content, type=discord.ChannelType.text)
                if canal_texto:
                    await ctx.send("Já existe um canal de texto com esse nome. Escolha outro nome.")
                else:
                    while True:
                        await ctx.send("Em qual categoria deseja criar o canal de texto?")
                        nome_categoria = await bot.wait_for('message', check=check, timeout=60)

                        categoria = discord.utils.get(ctx.guild.categories, name=nome_categoria.content)
                        if not categoria:
                            await ctx.send("A categoria especificada não existe. Informe o nome de uma categoria que já existe")
                        else:
                            await ctx.guild.create_text_channel(nome_canal.content, category=categoria)
                            await ctx.send(f"O canal de texto {nome_canal.content} foi criado com sucesso!")
                            break
                    break

        elif resposta.content.lower() == 'canal de voz':
            while True:
                await ctx.send("Qual o nome do canal de voz que deseja criar?")
                nome_canal = await bot.wait_for('message', check=check, timeout=60)

                canal_voz = discord.utils.get(ctx.guild.channels, name=nome_canal.content, type=discord.ChannelType.voice)
                if canal_voz:
                    await ctx.send("Já existe um canal de voz com esse nome. Escolha outro nome.")
                else:
                    while True:
                        await ctx.send("Em qual categoria deseja criar o canal de voz?")
                        nome_categoria = await bot.wait_for('message', check=check, timeout=60)

                        categoria = discord.utils.get(ctx.guild.categories, name=nome_categoria.content)
                        if not categoria:
                            await ctx.send("A categoria especificada não existe. Informe o nome de uma categoria que já existe")
                        else:
                            await ctx.guild.create_voice_channel(nome_canal.content, category=categoria)
                            await ctx.send(f"O canal de voz {nome_canal.content} foi criado com sucesso!")
                            break
                    break

        elif resposta.content.lower() == 'canal':
            await ctx.send("Qual tipo de canal você deseja criar?{[Voz | Texto]")

            tipo_canal = await bot.wait_for('message', check=check, timeout=60)
            if tipo_canal.content.lower() == 'texto':
                while True:
                    await ctx.send("Qual o nome do canal de texto que deseja criar?")
                    nome_canal = await bot.wait_for('message', check=check, timeout=60)

                    canal_texto = discord.utils.get(ctx.guild.channels, name=nome_canal.content, type=discord.ChannelType.text)
                    if canal_texto:
                        await ctx.send("Já existe um canal de texto com esse nome. Escolha outro nome.")
                    else:
                        while True:
                            await ctx.send("Em qual categoria deseja criar o canal de texto?")
                            nome_categoria = await bot.wait_for('message', check=check, timeout=60)

                            categoria = discord.utils.get(ctx.guild.categories, name=nome_categoria.content)
                            if not categoria:
                                await ctx.send("A categoria especificada não existe. Informe o nome de uma categoria que já existe")
                            else:
                                await ctx.guild.create_text_channel(nome_canal.content, category=categoria)
                                await ctx.send(f"O canal de texto {nome_canal.content} foi criado com sucesso!")
                                break
                        break

            elif tipo_canal.content.lower() == 'voz':
                while True:
                    await ctx.send("Qual o nome do canal de voz que deseja criar?")
                    nome_canal = await bot.wait_for('message', check=check, timeout=60)

                    canal_voz = discord.utils.get(ctx.guild.channels, name=nome_canal.content, type=discord.ChannelType.voice)
                    if canal_voz:
                        await ctx.send("Já existe um canal de voz com esse nome. Escolha outro nome.")
                    else:
                        while True:
                            await ctx.send("Em qual categoria deseja criar o canal de voz?")
                            nome_categoria = await bot.wait_for('message', check=check, timeout=60)

                            categoria = discord.utils.get(ctx.guild.categories, name=nome_categoria.content)
                            if not categoria:
                                await ctx.send("A categoria especificada não existe. Informe o nome de uma categoria que já existe")
                            else:
                                await ctx.guild.create_voice_channel(nome_canal.content, category=categoria)
                                await ctx.send(f"O canal de voz {nome_canal.content} foi criado com sucesso!")
                                break
                        break

        else:
            await ctx.send("Opção inválida.")

    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. O comando foi cancelado.")




# ================ Jokenpô ================
@bot.command()
async def jokenpo(ctx):
    opcoes = ['pedra', 'papel', 'tesoura']
    emojis = ['✊', '🖐', '✌']

    mensagem = "Escolha uma opção:\n"
    for i in range(3):
        mensagem += f"{emojis[i]} - {opcoes[i]}\n"
    mensagem += "Reaja com o emoji correspondente à opção."

    embed = discord.Embed(
        title="Jokenpo",
        description=mensagem,
        color=discord.Color.blue()
    )

    msg = await ctx.send(embed=embed)

    for i in range(3):
        await msg.add_reaction(emojis[i])

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in emojis

    try:
        reaction, _ = await bot.wait_for('reaction_add', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Tente novamente.")
        return

    escolha = opcoes[emojis.index(reaction.emoji)]
    escolha_bot = random.choice(opcoes)

    if escolha == escolha_bot:
        resultado = 'Empate!'
        color = discord.Color.gold()
    elif (escolha == 'pedra' and escolha_bot == 'tesoura') or (escolha == 'papel' and escolha_bot == 'pedra') or (escolha == 'tesoura' and escolha_bot == 'papel'):
        resultado = 'Você ganhou!'
        color = discord.Color.green()
    else:
        resultado = 'Você perdeu!'
        color = discord.Color.red()

    embed_resultado = discord.Embed(
        title="Jokenpo - Resultado",
        color=color
    )
    embed_resultado.add_field(name="Jogador", value=ctx.author.mention, inline=False)
    embed_resultado.add_field(name="Escolha do Jogador", value=f"{reaction.emoji} - {escolha.capitalize()}", inline=False)
    embed_resultado.add_field(name="Escolha do Bot", value=f"{emojis[opcoes.index(escolha_bot)]} - {escolha_bot.capitalize()}", inline=False)
    embed_resultado.add_field(name="Resultado", value=resultado, inline=False)
    embed_resultado.add_field(name="Jogar novamente?", value="Reaja com '✅' para recomeçar ou com '❌' para encerrar o jogo.", inline=False)

    mensagem_resultado = await ctx.send(embed=embed_resultado)
    await mensagem_resultado.add_reaction('✅')  
    await mensagem_resultado.add_reaction('❌')  

    def check_reacao(reaction, user):
        return user == ctx.author and reaction.message.id == mensagem_resultado.id and str(reaction.emoji) in ['✅', '❌']

    try:
        reaction, _ = await bot.wait_for('reaction_add', check=check_reacao, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. O jogo será encerrado.")
        return

    if str(reaction.emoji) == '✅':
        await jokenpo(ctx) 
    else:
        await ctx.send("O jogo foi encerrado.")



# ================ Atribuir cargo por reação em mensagem ================
@bot.command()
async def emoji_message(ctx):
    message = await ctx.send("Reaja com os emojis abaixo para atribuir um cargo:")
    emojis = ["🚹", "🚺"]

    for emoji in emojis:
        await message.add_reaction(emoji)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1122249852621955102:  
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        role = discord.utils.get(guild.roles, name="🚹|Masculino") 

        if payload.emoji.name == "🚹":
            await payload.member.add_roles(role)
        elif payload.emoji.name == "🚺":
            role = discord.utils.get(guild.roles, name="🚺|Feminino")  
            await payload.member.add_roles(role)



bot.run('MTExNzk2MTMwMjIzMzU5NTkwNA.Gch4bQ.B5Nj-P7Hr32xnxf6hba0jQloFBfg8mjweTIPRY')
