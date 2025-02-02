{% extends "email/base.tpl" %}
{% block subject %}
Verify Your Email Address
{% endblock %}
{% block body %}
Dear {{ name }},
Thank you for registering! To verify your email address, please click on the link below:
{{ site_url }}/verify-email/{{ verification_token }}/
This link will expire in 24 hours.
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
                            <h1><font color="#333333">Verify Your Email Address</font></h1>

                            <p>Dear {{ name }},</p>

                            <p>Thank you for registering! To verify your email address, please click on the button below:</p>

                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{{ site_url }}/verify-email/{{ verification_token }}/"
                                   style="background-color: #4CAF50; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
                                    Verify Email
                                </a>
                            </div>

                            <p style="color: #666; font-size: 12px;">
                                This link will expire in 24 hours. If you did not create an account, please ignore this email.
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