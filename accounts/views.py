import hashlib
import hmac
import time

from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages


class AuthTelegramView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("factory-detail")

        request_data = request.GET.copy()

        received_hash = request_data.get('hash', '')
        auth_date = request_data.get('auth_date', '')

        request_data.pop('hash', None)
        request_data_alphabetical_order = sorted(request_data.items(), key=lambda x: x[0])

        data_check_string = []

        for data_pair in request_data_alphabetical_order:
            key, value = data_pair[0], data_pair[1]
            data_check_string.append(key + '=' + value)

        data_check_string = '\n'.join(data_check_string)

        secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
        _hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

        unix_time_now = int(time.time())
        unix_time_auth_date = int(auth_date)

        # 86400 - ONE_DAY_IN_SECONDS
        if unix_time_now - unix_time_auth_date > 86400:
            messages.add_message(request, messages.ERROR, "Ты не робот :(")
            return redirect("login")

        if _hash != received_hash:
            messages.add_message(request, messages.ERROR, "Ты не робот :(")
            return redirect("login")

        return redirect("factory-detail")
