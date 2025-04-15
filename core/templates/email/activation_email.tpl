{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation
{% endblock %}

{% block html %}
dear user : {{ email }}<br>
here is your account activation url:<br>
http://185.226.118.52/accounts/api/v1/activation/confirm/{{ token }}/
<br>
<p>This link is valid for 5 minutes and also it's one-time use!</p>
</p>Regards</p>
{% endblock %}