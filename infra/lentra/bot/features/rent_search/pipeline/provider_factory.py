from lentra.bot.features.rent_search.providers.sea.sea_provider import SEAProvider
from lentra.bot.features.rent_search.providers.sea.thailand_provider import ThailandProvider
from lentra.bot.features.rent_search.providers.social.social_provider import SocialProvider


class ProviderFactory:

    @staticmethod
    def build():

        return SEAProvider(
            providers=[
                ThailandProvider(),
                SocialProvider()
            ]
        )
