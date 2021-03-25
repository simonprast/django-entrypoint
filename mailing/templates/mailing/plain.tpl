{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.username }}
{% endblock %}

{% block body %}
This is a plain text message.
{% endblock %}