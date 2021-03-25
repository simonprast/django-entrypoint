{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.name }}
{% endblock %}

{% block body %}
This is a plain text message.
{% endblock %}