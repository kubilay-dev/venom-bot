from asyncio.tasks import sleep
import asyncio
import requests
import discord
import mysql.connector
from discord.ext import commands
from discord.ext.commands import has_permissions
import requests
import json
import datetime
from datetime import timedelta, date, datetime
import time


# z # # z # # z # # z # # z # # z #
token = 'bot token hier'
intents = discord.Intents.all()
client = commands.Bot(command_prefix='%', intents=intents)
client.remove_command('help')
# z # # z # # z # # z # # z # # z #

async def requestyes():
    channel = client.get_channel(931545216165507083)
    msgid = 931819058247118899
    req = requests.get("https://cdn.rage.mp/master/")
    data = json.loads(req.text)
    newdata = data["62.192.153.127:22005"]
    editembed = discord.Embed(title="Aktueller Serverstatus", timestamp=datetime.utcnow())
    editembed.set_thumbnail(url="https://www.uni-giessen.de/fbz/fb02/fb/professuren/bwl/data-science-digitalisierung/media/checkmark/download")
    editembed.add_field(name="Serverstatus", value="Online 🟢", inline=False)
    editembed.add_field(name="Spieler auf dem Server", value=newdata["players"], inline=False)
    editembed.add_field(name="Spielerpeak", value=newdata["peak"], inline=False)
    now = datetime.now()
    newtime=now.replace(microsecond=0)
    time=('%02d:%02d:%f'%(newtime.hour, newtime.minute, newtime.second))[:-4]
    editembed.add_field(name="Letzter Check", value=time, inline=False)
    editembed.set_footer(text="Venom API by kubilay")
    msg = await channel.fetch_message(msgid)
    await msg.edit(embed=editembed)


async def requestno():
    channel = client.get_channel(931545216165507083)
    await channel.purge(limit=100)
    embed=discord.Embed(title="Aktueller Serverstatus", timestamp=datetime.utcnow())
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Eo_circle_red_white_checkmark.svg/1024px-Eo_circle_red_white_checkmark.svg.png")
    embed.add_field(name="Serverstatus", value="Offline 🟢", inline=False)
    embed.set_footer(text="Venom API by kubilay")
    await channel.send(embed=embed)

@client.event
async def on_ready():
    print('Bot jetzt online, lol.')
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game(
            name=f"Venom API | %help")
    )
    while True:
        try:
            await requestyes()
            await sleep(60)
        except KeyError:
            await requestno()
            await sleep(60)


@client.command()
async def help(ctx: commands.Context):
    embed = discord.Embed(title='Alle Commands', colour=discord.Colour.purple(
    ), description=f'%help [Zeigt alle Commands]\n%ban user grund [bannt einen user mit grund]\n%kick user grund [kickt einen user mit grund]\n%purge [purged einen channel]\n%lock/unlock [Sperrt/Entsperrt einen Channel]\n%mute user grund [muted einen user]')
    embed.set_footer(text='Venom API')
    await ctx.send(embed=embed)

@client.command()
@commands.has_role("Bot Permission")
async def ahelp(ctx):
    embed = discord.Embed(title="Aktuelle Admin Commands", colour=discord.Color.purple(),
    description="**%whitelist Ingame_Name SocialName 01-01-2022** [whitelisted person auf server]\n**%delaccount Ingame_Name** [löscht einen account ingame]\n**%setrights Ingame_Name Rang** (1-6) [settet einen ingame rang nach belieben]\n**%changename Ingame_Name NeuerIngame_Name** [ändert einen ingame namen von a zu b]\n**%changesocial SocialClubAlt SocialClubNeu** [ändert den socialclub von einem account von a zu b]\n**%changelevel Ingame_Name Level** [settet level zu einem bestimmten account]")
    embed.set_footer(text="Venom API")
    await ctx.send(embed=embed)

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, reason=None):
    await ctx.send(f'User wurde gebannt. Grund: {reason}')
    await member.send(f'Du wurdest von dem Venom Roleplay gebannt. Grund: {reason}')
    await member.ban(reason=reason)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Wen soll ich bannen, Meister?')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Nonono, dont do that.')


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, reason=None):
    await ctx.send(f'User wurde gekickt. Grund: {reason}')
    await member.send(f'Du wurdest von dem Venom Roleplay gekickt. Grund: {reason}')
    await member.kick(reason=reason)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Wen soll ich kicken, Meister?')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Nonono, dont do that.')


@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send(f'{limit} Nachrichten wurden von {ctx.author.mention} gepurged.', delete_after=5)


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Wie viele Nachrichten soll ich löschen, Meister?')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Nonono, dont do that.')


@client.command()
@has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " hat jetzt Sendepause. ☕")


@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Nonono, dont do that.')


@client.command()
@has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ist jetzt wieder geöffnet. 👀")


@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Nonono, dont do that.')


@client.command()
@commands.has_role("Bot Permission")
async def whitelist(ctx, name, scname, birthdate):
    venomrp = mysql.connector.connect(
        host="62.192.153.127",
        user="kubilay",
        passwd="3ILbcK2)Y(A@c2F5",
        database="gvrp",
        auth_plugin="mysql_native_password",
    )

    mycursor = venomrp.cursor()

    latestid = "SELECT MAX(id) FROM `player`"
    mycursor.execute(latestid)
    latestidresult = mycursor.fetchall()
    finalnumber = str(latestidresult)
    finalfinalnumber = finalnumber.translate(
        str.maketrans({'(': '', ')': '', ',': '', '[': '', ']': ''}))
    finalnegerfinalnegernumber = int(finalfinalnumber) + 1
    usersql = f"INSERT INTO `player` (`id`, `Name`, `forumid`, `handy`, `rankId`, `team`, `rang`, `Level`, `duty`, `isCuffed`, `isTied`, `hp`, `swat`, `xmasLast`, `drugcreatelast`, `uhaft`, `einwanderung`, `swatduty`, `teamfight`, `nsalic`, `suspendate`, `w_dutytime`, `marrylic`, `mediclic`, `gov_level`, `racing_besttime`, `armor`, `visibleArmorType`, `blackmoneybank`, `online`, `Money`, `BankMoney`, `payday`, `rp`, `ownHouse`, `wanteds`, `Lic_Car`, `Lic_LKW`, `Lic_Bike`, `Lic_PlaneA`, `Lic_PlaneB`, `Lic_Boot`, `Lic_Gun`, `Lic_Biz`, `spawnchange`, `job`, `jobskills`, `jailtime`, `Perso`, `Donator`, `uni_points`, `uni_economy`, `uni_business`, `birthday`, `fspawn`, `hasPed`, `Lic_FirstAID`, `timeban`, `job_skills`, `warns`, `fgehalt`, `paycheck`, `pedlicense`, `guthaben`, `lic_transfer`, `married`, `Lic_Taxi`, `pos_x`, `pos_y`, `pos_z`, `pos_heading`, `dimension`, `grade`, `drink`, `food`, `fitness`, `SCName`, `dimensionType`, `weapons`, `lasthandychange`, `Pass`, `Salt`, `blackmoney`, `uni_workaholic`, `lastuninvite`, `tax_sum`, `workstation_id`, `klingeltonId`, `wallpaperId`, `customization`, `animation_shortcuts`, `phone`, `ucname`, `deadstatus`, `equiped_props`, `deadtime`, `dead_x`, `dead_y`, `dead_z`, `ignore_maxplayers`, `LastLogin`, `teamid`, `lastSaved`, `wallpaper`, `gender`, `pw`) VALUES ({finalnegerfinalnegernumber}, '{name}', 2147483647, 0, 0, 0, 0, 15, 0, 0, 0, 100, 0, '2021-05-08 20:52:17', '2021-05-08 20:52:17', 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', 0, 0, 0, 0, 0, 25000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, '{birthdate}', 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -975.1, -2653.23, 13.4736, 314.181, 0, 0, 0, 0, 0, '{scname}', 0, '[]', '2021-05-10 12:13:58', '', '', 0, 0, '2021-05-14 22:17:06', 0, 0, 0, 0, '', '', 0, '', 0, '', 0, 0, 0, 0, 0, 0, 0, '0000-00-00 00:00:00', '0', 0, 0);"
    substring = "-"
    substringname = "_"
    if substring in birthdate:
        if substringname in name:
            mycursor.execute(usersql)
            venomrp.commit()
            embed = discord.Embed(title="Erfolgreich!",
                                  description=f"Du hast {name} mit dem Social {scname} und dem Geburtsdatum {birthdate} erfolgreich die Whitelist gestattet.", color=0x489118)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/icons/863796497740202006/357c26b404fb30e0781d58b1f534412a.png?size=4096")
            embed.add_field(name="undefined", value="undefined", inline=False)
            embed.set_footer(text=ctx.author)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Bitte überprüfe deine Angaben. Fehler: (Name)")
    else:
        await ctx.send("Bitte überprüfe deine Angaben. Fehler: (Geburtsdatum)")


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Dir fehlt ein Argument. Syntax: Ingame_Name, Socialclubname, 01-01-2022')
    elif isinstance(error, commands.MissingRole):
        await ctx.send('Nonono, dont do that.')


@client.command()
@commands.has_role("Bot Permission")
async def delaccount(ctx, name):

    venomrp = mysql.connector.connect(
        host="62.192.153.127",
        user="kubilay",
        passwd="3ILbcK2)Y(A@c2F5",
        database="gvrp",
        auth_plugin="mysql_native_password",
    )
    mycursor = venomrp.cursor()
    try:
        usersql = f"DELETE FROM `player` WHERE Name = '{name}'"
        mycursor.execute(usersql)
        venomrp.commit()
        embed = discord.Embed(title="Erfolgreich!",
            description=f"Du hast den Account {name} gelöscht.", color=0x489118)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/863796497740202006/357c26b404fb30e0781d58b1f534412a.png?size=4096")
        embed.add_field(name="undefined", value="undefined", inline=False)
        embed.set_footer(text=ctx.author)
        await ctx.send(embed=embed)

    except:
        await ctx.send("Fehler! Account nicht vorhanden oder Bot kaputt bre. <:sadge:928783666564436029>")


@delaccount.error
async def delaccount_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Dir fehlt ein Argument. Syntax: Ingame_Name')
    elif isinstance(error, commands.MissingRole):
        await ctx.send('Nonono, dont do that.')


@client.command()
@commands.has_role("Bot Permission")
async def setrights(ctx, name, rang):

    venomrp = mysql.connector.connect(
        host="62.192.153.127",
        user="kubilay",
        passwd="3ILbcK2)Y(A@c2F5",
        database="gvrp",
        auth_plugin="mysql_native_password",
    )
    mycursor = venomrp.cursor()
    try:
        usersql = f"UPDATE player SET rankId = {rang} WHERE Name = '{name}'"
        mycursor.execute(usersql)
        venomrp.commit()
        embed = discord.Embed(colour=discord.Colour.green(),
                              description="Du hast dem Account " + name + " Rang " + rang + " gesetzt.")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Venom API")
        await ctx.send(embed=embed)

    except:
        await ctx.send("Fehler! Account nicht vorhanden oder Bot kaputt bre. <:sadge:928783666564436029>")


@setrights.error
async def setrights_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Dir fehlt ein Argument. Syntax: Ingame_Name Rang')
    elif isinstance(error, commands.MissingRole):
        await ctx.send('Nonono, dont do that.')


@client.command()
@commands.has_role("Bot Permission")
async def changename(ctx, name, newname):

    venomrp = mysql.connector.connect(
        host="62.192.153.127",
        user="kubilay",
        passwd="3ILbcK2)Y(A@c2F5",
        database="gvrp",
        auth_plugin="mysql_native_password",
    )
    mycursor = venomrp.cursor()
    try:
        charmap = {ord("-"): "_"}
        translatedname = name.translate(charmap)
        translatednewname = newname.translate(charmap)
        usersql = f"UPDATE player SET Name = '{translatednewname}' WHERE name = '{translatedname}'"
        mycursor.execute(usersql)
        venomrp.commit()
        embed = discord.Embed(colour=discord.Colour.green(),
                              description="Du hast den Namen von " + translatedname + " zu " + translatednewname + " geändert.")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Venom API")
        await ctx.send(embed=embed)

    except:
        await ctx.send("Fehler! Account nicht vorhanden oder Bot kaputt bre. <:sadge:928783666564436029>")


@changename.error
async def changename_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Dir fehlt ein Argument. Syntax: Ingame**-**Name NeuerIngame**-**Name (Das - nicht vergessen!)')
    elif isinstance(error, commands.MissingRole):
        await ctx.send('Nonono, dont do that.')


@client.command()
@commands.has_role("Bot Permission")
async def changesocial(ctx, social, newsocial):

    venomrp = mysql.connector.connect(
        host="62.192.153.127",
        user="kubilay",
        passwd="3ILbcK2)Y(A@c2F5",
        database="gvrp",
        auth_plugin="mysql_native_password",
    )
    mycursor = venomrp.cursor()
    try:
        usersql = f"UPDATE player SET SCName = '{newsocial}' WHERE SCName = '{social}'"
        mycursor.execute(usersql)
        venomrp.commit()
        embed = discord.Embed(colour=discord.Colour.green(),
                              description="Du hast den Social Club Namen von " + social + " zu " + newsocial + " geändert.")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Venom API")
        await ctx.send(embed=embed)

    except:
        await ctx.send("Fehler! Account nicht vorhanden oder Bot kaputt bre. <:sadge:928783666564436029>")


@changesocial.error
async def changesocial_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Dir fehlt ein Argument. Syntax: SocialName SocialNeuerName')
    elif isinstance(error, commands.MissingRole):
        await ctx.send('Nonono, dont do that.')


@client.command()
@commands.has_role("Bot Permission")
async def changelevel(ctx, name, level):

    venomrp = mysql.connector.connect(
        host="62.192.153.127",
        user="kubilay",
        passwd="3ILbcK2)Y(A@c2F5",
        database="gvrp",
        auth_plugin="mysql_native_password",
    )
    mycursor = venomrp.cursor()
    try:
        usersql = f"UPDATE player SET Level = {level} WHERE Name = '{name}'"
        mycursor.execute(usersql)
        venomrp.commit()
        embed = discord.Embed(colour=discord.Colour.green(),
                              description="Du hast das Level von " + name + " zu Level " + level + " geändert.")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Venom API")
        await ctx.send(embed=embed)

    except:
        await ctx.send("Fehler! Account nicht vorhanden oder Bot kaputt bre. <:sadge:928783666564436029>")


@changelevel.error
async def changelevel_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Dir fehlt ein Argument. Syntax: Ingame_Name Level')
    elif isinstance(error, commands.MissingRole):
        await ctx.send('Nonono, dont do that.')

client.run(token)
