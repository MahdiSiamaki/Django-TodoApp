{% extends "email/base.tpl" %}
{% block subject %}
Welcome to Our Website
{% endblock %}
{% block body %}
Dear {{ name }},
Welcome to our website! We're excited to have you join us.
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

                            <table cellpadding="20" cellspacing="0" border="0">
                                <tr>
                                    <td>
                                        <img src="https://via.placeholder.com/150" alt="Company Logo" width="150" />
                                    </td>
                                </tr>
                            </table>

                            <p>Best regards,<br>The Team</p>
                        </font>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
{% endblock %}