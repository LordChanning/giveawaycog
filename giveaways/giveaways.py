import discord
from discord.ext import tasks, commands
from redbot.core import commands
import asyncio
from datetime import datetime, date
import time
import random


def findN(string, n, item=':'):
    '''For example, if n = 3, this will find the third occurence of {item} (throughout this program, {item} will be ':') in the string, and return it's index.'''

    val = -1
    for i in range(0, n): 
        val = string.find(item, val + 1) 

    return val



class Giveaway(commands.Cog):
    '''Coded by Gianna and Joey <3'''

    def __init__(self, bot):
        self.bot = bot
        self.text = ""
        self.giveaways = 0
        self.emote = '🎉'
        self.taskLoopActive = False
        self.config = {}


    def newEmbed(self, key):
        '''Returns a new embed object with the newest information to edit over the old one.'''

        embed = discord.Embed(title=f"{self.config[key]['prize']}", description=f"Hosted by: {self.config[key]['host'].mention}\nReact with 🎉 to enter", colour=0xcbab58)
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        if self.config[key]['message'] != "":
            if self.config[key]['numWinners'] > 1:
                embed.add_field(name="Status: Running", value=f"Time remaining: **{self.config[key]['days']}** days, **{self.config[key]['hours']}** hours, **{self.config[key]['minutes']}** minutes, **{self.config[key]['seconds']}** seconds", inline=False)
                embed.set_footer(text=f"{self.config[key]['numWinners']} winners  |  Ends: {self.config[key]['totalSecondsRemaining']}s\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

            else:
                embed.add_field(name="Status: Running", value=f"Time remaining: **{self.config[key]['days']}** days, **{self.config[key]['hours']}** hours, **{self.config[key]['minutes']}** minutes, **{self.config[key]['seconds']}** seconds", inline=False)
                embed.set_footer(text=f"{self.config[key]['numWinners']} winner  |  Ends: {self.config[key]['totalSecondsRemaining']}s\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        return embed


    def tenSecondEmbed(self, key):
        '''Returns an embed object that counts the remaining 10 seconds by the second.'''

        embed = discord.Embed(title=f"{self.config[key]['prize']}", description=f"**Last chance to enter!**\nHosted by: {self.config[key]['host'].mention}\nReact with 🎉 to enter", colour=0xc90c3f)
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        if self.config[key]['numWinners'] > 1:
            embed.add_field(name="Status: Running", value=f"Time remaining: **{self.config[key]['days']}** days, **{self.config[key]['hours']}** hours, **{self.config[key]['minutes']}** minutes, **{self.config[key]['seconds']}** seconds", inline=False)
            embed.set_footer(text=f"{self.config[key]['numWinners']} winners  |  Ends: {self.config[key]['totalSecondsRemaining']}s\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        else:
            embed.add_field(name="Status: Running", value=f"Time remaining: **{self.config[key]['days']}** days, **{self.config[key]['hours']}** hours, **{self.config[key]['minutes']}** minutes, **{self.config[key]['seconds']}** seconds", inline=False)
            embed.set_footer(text=f"{self.config[key]['numWinners']} winner  |  Ends: {self.config[key]['totalSecondsRemaining']}s\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        return embed


    def finalEmbed(self, key):
        '''Chooses the winners for giveaways that ended, and returns an embed object to display the winners.'''

        strWinners = '\n'.join([user.mention for user in self.config[key]['winners']])

        if self.config[key]['numWinners'] > 1 and self.config[key]['totalEntrants'] > 0:
            embed = discord.Embed(title=f"{self.config[key]['prize']}", description=f"Hosted by: {self.config[key]['host'].mention}\n\n**Winners:**\n{strWinners}", colour=0x46d412)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=f"{self.config[key]['numWinners']} winners  |  Ended: {self.config[key]['endDate']}\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        elif self.config[key]['numWinners'] == 1 and self.config[key]['totalEntrants'] > 0:
            embed = discord.Embed(title=f"{self.config[key]['prize']}", description=f"Hosted by: {self.config[key]['host'].mention}\n\n**Winner:** {strWinners}", colour=0x46d412)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=f"{self.config[key]['numWinners']} winner  |  Ended: {self.config[key]['endDate']}\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        elif self.config[key]['numWinners'] > 1 and self.config[key]['totalEntrants'] == 0:
            embed = discord.Embed(title=f"{self.config[key]['prize']}", description=f"Hosted by: {self.config[key]['host'].mention}\n\n**No winners could be determined.**", colour=0x46d412)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=f"{self.config[key]['numWinners']} winners  |  Ended: {self.config[key]['endDate']}\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        else:
            embed = discord.Embed(title=f"{self.config[key]['prize']}", description=f"Hosted by: {self.config[key]['host'].mention}\n\n**No winner could be determined.**", colour=0x46d412)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=f"{self.config[key]['numWinners']} winner  |  Ended: {self.config[key]['endDate']}\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        return embed


    def rerollEmbed(self, key):
        '''If all rerolls have been called, this embed will be displayed.'''

        embed = discord.Embed(title=f"{self.config[key]['prize']}", description=f"Hosted by: {self.config[key]['host'].mention}\n\n**All entrants have been chosen.**", colour=0x46d412)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"{self.config[key]['numWinners']} winners  |  Ended: {self.config[key]['endDate']}\nStarted by: {self.config[key]['ctx'].message.author}\nGiveaway ID: {self.config[key]['message'].id}")

        return embed



    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        for key in self.config.keys():
            if self.config[key]['message'] != "":
                if reaction.message.id == self.config[key]['message'].id:
                    if user not in self.config[key]['entered'] and user.id != self.bot.user.id:
                        if reaction.emoji == self.emote:
                            self.config[key]['entered'].append(user)


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

        for key in self.config.keys():
            if self.config[key]['message'] != "":
                if reaction.message.id == self.config[key]['message'].id:
                    if user in self.config[key]['entered']:
                        if reaction.emoji == self.emote:
                            self.config[key]['entered'].remove(user)


    @tasks.loop(seconds=1.0)
    async def updateTime(self):

        for key in self.config.keys():
            if self.config[key]['finished']:
                continue

            secRemaining = self.config[key]['totalSecondsRemaining']

            self.config[key]['days'] = secRemaining // 86400
            self.config[key]['hours'] = (secRemaining - self.config[key]['days'] * 86400) // 3600
            self.config[key]['minutes'] = (secRemaining - self.config[key]['days'] * 86400 - self.config[key]['hours'] * 3600) // 60
            self.config[key]['seconds'] = secRemaining- self.config[key]['days'] * 86400 - self.config[key]['hours'] * 3600 - self.config[key]['minutes'] * 60


            if secRemaining <= 0:
                self.config[key]['totalEntrants'] = len(self.config[key]['entered'])

                for i in range(self.config[key]['numWinners']):
                    if len(self.config[key]['entered']) > 0:
                        winner = random.choice(self.config[key]['entered'])
                        self.config[key]['winners'].append(winner)
                        self.config[key]['entered'].remove(winner)

                    else:
                        break

                strWinners = ', '.join([user.mention for user in self.config[key]['winners']])
                prize = self.config[key]['prize']
                totalEntrants = self.config[key]['totalEntrants']
                self.config[key]['endDate'] = f"{time.asctime(time.localtime(time.time()))[:-14]} at {time.asctime(time.localtime(time.time()))[11:-8]}"

                updatedEmbed = self.finalEmbed(key)
                await self.config[key]['message'].edit(embed=updatedEmbed, content="🎉 ***GIVEAWAY ENDED*** 🎉")

                if self.config[key]['totalEntrants'] == 1:
                    await self.config[key]['channel'].send(f'Congratulations, {strWinners}!\nYou won **{prize}**, out of {totalEntrants} entry!')

                elif self.config[key]['totalEntrants'] > 1:
                    await self.config[key]['channel'].send(f'Congratulations, {strWinners}!\nYou won **{prize}**, out of {totalEntrants} entries!')

                else:
                    await self.config[key]['channel'].send("No winners could be determined.")

                self.config[key]['loop'] = 0
                self.config[key]['finished'] = True
                self.giveaways -= 1


            elif secRemaining > 10 and self.config[key]['loop'] == 10:
                self.config[key]['loop'] = 0
                updatedEmbed = self.newEmbed(key)
                await self.config[key]['message'].edit(embed = updatedEmbed)

            elif secRemaining <= 10:
                updatedEmbed = self.tenSecondEmbed(key)
                await self.config[key]['message'].edit(embed = updatedEmbed)

            self.config[key]['loop'] = self.config[key]['loop'] + 1
            self.config[key]['totalSecondsRemaining'] = self.config[key]['totalSecondsRemaining'] - 1


        if self.giveaways == 0:
            self.taskLoopActive = False
            self.updateTime.cancel()



    @commands.group()
    async def g(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send("invalid g command passed")


    @g.command()
    async def start(self, ctx, channelid, winners, *, prize):

        channel = self.bot.get_channel(int(channelid))
        find = prize.find('user=')

        if "user=" in prize:
            user = prize[find+5:]
            prize = prize[:find]
            user_name, user_discriminator = user.split('#')
            user = discord.utils.get(ctx.message.channel.guild.members, name = user_name, discriminator = user_discriminator)

        else:
            user = ctx.message.author

        await ctx.send("How long will the giveaway run for? (d:h\:m:s)")


        while True:
            text = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author)
            time = text.content
            separators = time.count(':')
            days, hours, minutes, seconds = 0, 0, 0, 0
            colonIndex = [findN(time, 1), findN(time, 2), findN(time, 3), findN(time, 4)]

            if separators == 3:
                days = time[: colonIndex[0]]
                hours = time[colonIndex[0]+1 : colonIndex[1]]
                minutes = time[colonIndex[1]+1 : colonIndex[2]]
                seconds = time[colonIndex[2]+1 :]

            elif separators == 2:
                hours = time[: colonIndex[0]]
                minutes = time[colonIndex[0]+1 : colonIndex[1]]
                seconds = time[colonIndex[1]+1 :]

            elif separators == 1:
                minutes = time[: colonIndex[0]]
                seconds = time[colonIndex[0]+1 :]
            
            else:
                seconds = time


            try:
                if "?g start" in time:
                    self.config[self.giveaways]['finished'] = True

                else:
                    sleepTime = (int(days) * 86400) + (int(hours) * 3600) + (int(minutes) * 60) + int(seconds)
                    break

            except ValueError:
                pass
 

        embed = discord.Embed(title=f"{prize}", description=f"Hosted by: {user}\nReact with 🎉 to enter", colour=0xcbab58)
        embed.set_thumbnail(url=self.bot.user.avatar_url)


        self.config[self.giveaways] = {
            'channel': channel,
            'prize': prize,
            'ctx': ctx, 
            'numWinners': int(winners),
            'embed': embed,
            'host': user,
            'totalSecondsRemaining': sleepTime,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'loop': 0,
            'message': "",
            'entered': [],
            'totalEntrants': 0,
            'winners': [],
            'finished': False
        }


        if time != None:
            if sleepTime >= 10:
                embed = self.newEmbed(self.giveaways)
                self.config[self.giveaways]['message'] = await channel.send("🎉 ***GIVEAWAY*** 🎉", embed=embed)

                updatedEmbed = self.newEmbed(self.giveaways)
                await self.config[self.giveaways]['message'].edit(embed = updatedEmbed)
                await self.config[self.giveaways]['message'].add_reaction(self.emote)

                if not self.taskLoopActive:
                    self.updateTime.start()
                    self.taskLoopActive = True

                self.giveaways += 1

            else:
                await ctx.send("Must be at least 10 seconds.")


    @g.command()
    async def stop(self, ctx, messageid):

        for key in self.config.keys():
            if self.config[key]['message'].id == int(messageid):
                self.config[key]['totalSecondsRemaining'] = 0

    
    @g.command()
    async def reroll(self, ctx, messageid):

        for key in self.config.keys():
            if self.config[key]['message'].id == int(messageid) and self.config[key]['finished'] == True:
                self.config[key]['winners'].clear()

                for i in range(1):
                    if len(self.config[key]['entered']) > 0:
                        winner = random.choice(self.config[key]['entered'])
                        self.config[key]['winners'].append(winner)
                        self.config[key]['entered'].remove(winner)

                    else:
                        break


                strWinners = ', '.join([user.mention for user in self.config[key]['winners']])
                prize = self.config[key]['prize']
                totalEntrants = self.config[key]['totalEntrants']
                self.config[key]['endDate'] = f"{time.asctime(time.localtime(time.time()))[:-14]} at {time.asctime(time.localtime(time.time()))[11:-8]}"


                if self.config[key]['totalEntrants'] == 1 and len(self.config[key]['winners']) > 0:
                    updatedEmbed = self.finalEmbed(key)
                    await self.config[key]['message'].edit(embed=updatedEmbed, content="🎉 ***GIVEAWAY ENDED*** 🎉")
                    await self.config[key]['channel'].send(f'Congratulations, {strWinners}!\nYou won **{prize}**, out of {totalEntrants} entry!')

                elif self.config[key]['totalEntrants'] > 1 and len(self.config[key]['winners']) > 0:
                    updatedEmbed = self.finalEmbed(key)
                    await self.config[key]['message'].edit(embed=updatedEmbed, content="🎉 ***GIVEAWAY ENDED*** 🎉")
                    await self.config[key]['channel'].send(f'Congratulations, {strWinners}!\nYou won **{prize}**, out of {totalEntrants} entries!')

                elif len(self.config[key]['winners']) == 0:
                    updatedEmbed = self.rerollEmbed(key)
                    await self.config[key]['message'].edit(embed=updatedEmbed, content="🎉 ***GIVEAWAY ENDED*** 🎉")
                    await self.config[key]['channel'].send("All entrants have been chosen.")



def setup(bot):
    bot.add_cog(Giveaway(bot))
