from django.http import JsonResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def refresh_captcha(request):
    new_key = CaptchaStore.generate_key()
    new_image_url = captcha_image_url(new_key)
    return JsonResponse({"image_url": new_image_url, "key": new_key})
