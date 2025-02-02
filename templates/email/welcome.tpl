{% extends "email/base.tpl" %}

{% block subject %}
Welcome to Our Website - Your Access Tokens
{% endblock %}

{% block body %}
Dear {{ name }},

Welcome to our website! We're excited to have you join us.

Here are your access tokens:

Access Token: {{ access_token }}
Refresh Token: {{ refresh_token }}

Please keep these tokens secure and do not share them with anyone.

Best regards,
The Team
{% endblock %}

{% block html %}
<table cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
        <td align="center">
            <table cellpadding="0" cellspacing="0" border="0" width="600">
                <tr>
                    <td align="left" bgcolor="#ffffff">
                        <font face="Arial, sans-serif">
                            <h1><font color="#333333">Welcome to Our Website</font></h1>

                            <p>Dear {{ name }},</p>

                            <p>Welcome to our website! We're excited to have you join us.</p>

                            <div style="background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px;">
                                <h3>Your Access Tokens</h3>
                                <p><strong>Access Token:</strong><br>
                                <code style="word-break: break-all;">{{ access_token }}</code></p>

                                <p><strong>Refresh Token:</strong><br>
                                <code style="word-break: break-all;">{{ refresh_token }}</code></p>
                            </div>

                            <p style="color: #666; font-size: 12px;">
                                Please keep these tokens secure and do not share them with anyone.
                            </p>

                            <p>Best regards,<br>The Team</p>
                        </font>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
{% endblock %}