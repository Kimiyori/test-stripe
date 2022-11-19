from dependency_injector import containers, providers

from stripe_app.stripe import StripeAPI

class StripeContainer(containers.DeclarativeContainer):
    stripe_session = providers.Factory(StripeAPI)