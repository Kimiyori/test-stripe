from dependency_injector import containers, providers

from stripe_app.stripe import StripeAPI


class StripeContainer(containers.DeclarativeContainer):
    """Container for stripe api"""

    stripe_session: providers.Factory[StripeAPI] = providers.Factory(StripeAPI)
