{% if macos and not one_password_agent %}
ssh-add --apple-use-keychain
{% endif %}
