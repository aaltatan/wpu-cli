# wpu-cli

CLI application for make some automation tasks.

## Environment Variables

```env
# Edutech App
EDUTECH_USERNAME=your_username # edutech username
EDUTECH_PASSWORD=your_password # edutech password
EDUTECH_TIMEOUT_AFTER_INSERTING_ROWS=5000 # timeout for playwright between rows insertion
EDUTECH_GENERAL_ACCOUNTING_URL=http://edu/?sc=504#/_FIN/ACT/menu.php


# Fuzz App
FUZZ_DEFAULT_ACCURACY=60 # default accuracy for fuzzy matching
FUZZ_DEFAULT_LIMIT=5 # default limit for fuzzy matching
FUZZ_DEFAULT_SCORER=q # default scorer for fuzzy matching
FUZZ_DEFAULT_REMOVE_DUPLICATED=1 # default remove duplicated for fuzzy matching
FUZZ_DEFAULT_WRITER=choices-xlsx # default writer for fuzzy matching

# Whatsapp App
## web
WHATSAPP_WEB_DEFAULT_BASE_URL=https://web.whatsapp.com # default base url for whatsapp app
WHATSAPP_WEB_DEFAULT_MIN_TIMEOUT_BETWEEN_MESSAGES=3 # default min timeout between messages in seconds for whatsapp app
WHATSAPP_WEB_DEFAULT_MAX_TIMEOUT_BETWEEN_MESSAGES=6 # default max timeout between messages in seconds for whatsapp app
WHATSAPP_WEB_DEFAULT_MIN_SEND_SELECTOR_TIMEOUT=10000 # default min send selector timeout in milliseconds for whatsapp app
WHATSAPP_WEB_DEFAULT_MAX_SEND_SELECTOR_TIMEOUT=15000 # default max send selector timeout in milliseconds for whatsapp app
WHATSAPP_WEB_DEFAULT_PAGELOAD_TIMEOUT=60000 # default pageload timeout in milliseconds for whatsapp app
## desktop
WHATSAPP_DESKTOP_DEFAULT_TIMEOUT_AFTER_OPENING=2 # default timeout after opening hyperlink in seconds for whatsapp desktop app
WHATSAPP_DESKTOP_DEFAULT_BETWEEN_MESSAGES=1 # default timeout between messages in seconds for whatsapp desktop app
WHATSAPP_DESKTOP_DEFAULT_CHECKING_LOOP=15 # default checking loop in seconds for whatsapp desktop app

# Template App
TEMPLATES_DEFAULT_SINGLE_DOCX_TEMPLATE_DATA_VARIABLE=data # default data key for generated single file
TEMPLATES_DEFAULT_XLSX_MULTIPLE_ROWS_TEMPLATE_GROUP_VARIABLE=data # default grouped key for generated multiple rows
```
