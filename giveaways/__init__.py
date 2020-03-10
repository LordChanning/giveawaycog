from .giveaways import Giveaways


async def setup(bot):
    bot.add_cog(Giveaways(bot))
