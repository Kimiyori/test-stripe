from django.http import HttpRequest


def convert_to_stripe_currency(amount: int | str) -> int:
    return int(round(int(amount), 2) * 100)


def create_urls(request: HttpRequest) -> tuple[str, str]:
    domain = f"http://{request.get_host()}"
    success_url = f"{domain}/success"
    cancel_url = f"{domain}/fail"
    return success_url, cancel_url
