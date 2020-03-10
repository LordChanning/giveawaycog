from .giveaway import Giveaway


def setup(bot):
    cog = {{Giveaway}}(bot)
    bot.add_cog(Giveaway(bot))
