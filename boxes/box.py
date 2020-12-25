import discord
from discord.ext import commands
from redbot.core import commands, checks
from redbot.core.config import Config

import random


class Boxes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.event = ""
        self.num1 = 1
        self.num2 = 100
        self.prizeLevel1 = [
            "100,000 Nyte Bucks",
            "200,000 Nyte Bucks",
            "300,000 Nyte Bucks",
            "400,000 Nyte Bucks",
            "500,000 Nyte Bucks",
            "600,000 Nyte Bucks",
            "700,000 Nyte Bucks",
            "800,000 Nyte Bucks",
            "900,000 Nyte Bucks",
            "1,000,000 Nyte Bucks",
            "1,100,000 Nyte Bucks",
            "1,200,000 Nyte Bucks",
            "1,300,000 Nyte Bucks",
            "1,400,000 Nyte Bucks",
            "1,500,000 Nyte Bucks",
            "1,600,000 Nyte Bucks",
            "1,700,000 Nyte Bucks",
            "1,800,000 Nyte Bucks",
            "1,900,000 Nyte Bucks",
            "2,000,000 Nyte Bucks"
        ]

        self.prizeLevel2 = [
            "a nickname change",
            "any regular role colour from shop",
            "a custom command coupon",
            "a custom emote for 7 days",
            "empty",
            "a reroll"
        ]
        
        self.prizeLevel3 = []

    @commands.group()
    async def box(self, ctx):

        if ctx.invoked_subcommand == None:
            await ctx.send("that's not a subcommand you insubordinate piece of crap")

    
    @box.command()
    async def open(self, ctx, user: discord.User):

        reroll = True
        while reroll:

            reroll = False
            num = random.randint(self.num1, self.num2)

            if num > 0 and num < 60:
                await ctx.send(f"{user.mention} You have gotten **{random.choice(self.prizeLevel1)}** from your {self.event} Loot Box!")

            if num >= 60 and num < 85:
                var = random.choice(self.prizeLevel2)

                if var == "empty":
                    await ctx.send(f"{user.mention} Your {self.event} Loot Box was {var} :(")

                else:
                    await ctx.send(f"{user.mention} You have gotten **{var}** from your {self.event} Loot Box!")

                if var == "a reroll":
                    reroll = True

            if num >= 85 and num <= 100:
                if "Astro A40s" in self.prizeLevel3:
                    del self.prizeLevel3[self.prizeLevel3.index("Astro A40s")]
                    self.prizeLevel3.append("Astro A40s")

                    if num >= 85 and num <= 95:
                        await ctx.send(f"{user.mention} You have gotten **{random.choice(self.prizeLevel3[:-1])}** from your {self.event} Loot Box!")

                    elif num > 95 and num <= 100:
                        await ctx.send(f"{user.mention} You have gotten **{self.prizeLevel3[-1]}** from your {self.event} Loot Box!")
                        self.prizeLevel3.remove("Astro A40s")

                else:
                    await ctx.send(f"{user.mention} You have gotten **{random.choice(self.prizeLevel3)}** from your {self.event} Loot Box!")


    @box.command()
    async def add(self, ctx, prizelevel, *, prize):

        if int(prizelevel) == 1:
            self.prizeLevel1.append(prize)
            await ctx.send(f"**{prize}** has been added to prize level **{prizelevel}**")

        elif int(prizelevel) == 2:
            self.prizeLevel2.append(prize)
            await ctx.send(f"**{prize}** has been added to prize level **{prizelevel}**")

        elif int(prizelevel) == 3:
            self.prizeLevel3.append(prize)
            await ctx.send(f"**{prize}** has been added to prize level **{prizelevel}**")

        else:
            await ctx.send(f"use the read subcommand i made it for a reason")


    @box.command()
    async def remove(self, ctx, prizelevel, *, prize):

        if int(prizelevel) == 1 and prize in self.prizeLevel1:
            self.prizeLevel1.remove(prize)
            await ctx.send(f"**{prize}** has been removed from prize level **{prizelevel}**")

        elif int(prizelevel) == 2 and prize in self.prizeLevel2:
            self.prizeLevel2.remove(prize)
            await ctx.send(f"**{prize}** has been removed from prize level **{prizelevel}**")

        elif int(prizelevel) == 3 and prize in self.prizeLevel3:
            self.prizeLevel3.remove(prize)
            await ctx.send(f"**{prize}** has been removed from prize level **{prizelevel}**")

        elif prize not in self.prizeLevel1 or prize not in self.prizeLevel2 or prize not in self.prizeLevel3:
            await ctx.send("do you not listen what the frick channing")


    @box.command()
    async def read(self, ctx, *, prizelevel):

        if int(prizelevel) == 1:
            read = ""
            for string in self.prizeLevel1:
                read += f"{string}\n"
            await ctx.send(read)

        elif int(prizelevel) == 2:
            read = ""
            for string in self.prizeLevel2:
                read += f"{string}\n"
            await ctx.send(read)

        elif int(prizelevel) == 3:
            read = ""
            for string in self.prizeLevel3:
                read += f"{string}\n"
            await ctx.send(read)

        else:
            await ctx.send(f"learn your prize levels you dumb heck")


    @box.command()
    async def event(self, ctx, *, event):

        self.event = event
        await ctx.send(f"The event has been updated to **{event}**")


def setup(bot):
    bot.add_cog(Boxes(bot))
