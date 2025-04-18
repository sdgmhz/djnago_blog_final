{% extends "mail_templated/base.tpl" %}

{% block subject %}
Password reset link for user: {{ email }}
{% endblock %}

{% block html %}
Dear user : {{ email }}<br>
Some body requested for password reset link for your account. If it wasn't you, just ignore this message.<br>
Here is your password reset link:<br>
http://127.0.0.1:8000/accounts/api/v1/password/reset/confirm/{{ token }}/
<p>This link is valid for 5 minutes and also it's one-time use!</p>
</p>Regards</p>
{% endblock %}