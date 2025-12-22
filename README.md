# wpu-cli

CLI application for make some automation tasks.

## Environment Variables

```env
# Edutech App
EDUTECH_USERNAME=your_username # edutech username
EDUTECH_PASSWORD=your_password # edutech password
EDUTECH_TIMEOUT_AFTER_INSERTING_ROWS=5000 # timeout for playwright between rows insertion

# Fuzz App
FUZZ_DEFAULT_ACCURACY=60 # default accuracy for fuzzy matching
FUZZ_DEFAULT_LIMIT=5 # default limit for fuzzy matching
FUZZ_DEFAULT_SCORER=q # default scorer for fuzzy matching
FUZZ_DEFAULT_REMOVE_DUPLICATED=1 # default remove duplicated for fuzzy matching
FUZZ_DEFAULT_WRITER=choices-xlsx # default writer for fuzzy matching

# Whatsapp App
WHATSAPP_DEFAULT_BASE_URL=https://web.whatsapp.com # default base url for whatsapp app
WHATSAPP_DEFAULT_MIN_TIMEOUT_BETWEEN_MESSAGES=3 # default min timeout between messages in seconds for whatsapp app
WHATSAPP_DEFAULT_MAX_TIMEOUT_BETWEEN_MESSAGES=6 # default max timeout between messages in seconds for whatsapp app
WHATSAPP_DEFAULT_MIN_SEND_SELECTOR_TIMEOUT=10000 # default min send selector timeout in milliseconds for whatsapp app
WHATSAPP_DEFAULT_MAX_SEND_SELECTOR_TIMEOUT=15000 # default max send selector timeout in milliseconds for whatsapp app
WHATSAPP_DEFAULT_PAGELOAD_TIMEOUT=60000 # default pageload timeout in milliseconds for whatsapp app

# Template App
TEMPLATES_DEFAULT_SINGLE_DOCX_TEMPLATE_DATA_VARIABLE=data # default data key for generated single file
TEMPLATES_DEFAULT_XLSX_MULTIPLE_ROWS_TEMPLATE_GROUP_VARIABLE=data # default grouped key for generated multiple rows

# Taxes App
TAXES_BRACKET_TAX_MINS=0 837000 850000 1100000 # default brackets mins for taxes app
TAXES_BRACKET_TAX_MAXS=837000 850000 1100000 25000000 # default brackets maxes for taxes app
TAXES_BRACKET_TAX_RATES=0 0.11 0.13 0.15 # default brackets rates for taxes app
TAXES_MIN_ALLOWED_SALARY=837000 # default min allowed salary for taxes app
TAXES_TAXES_ROUNDING_METHOD=ROUND_CEILING # default taxes rounding method for taxes app
TAXES_TAXES_ROUND_TO_NEAREST=100 # default taxes round to nearest for taxes app
TAXES_SS_ROUNDING_METHOD=ROUND_CEILING # default ss rounding method for taxes app
TAXES_SS_ROUND_TO_NEAREST=1 # default ss round to nearest for taxes app
TAXES_MIN_SS_ALLOWED_SALARY=750000 # default min ss allowed salary for taxes app
TAXES_SS_DEDUCTION_RATE=0.07 # default ss deduction rate for taxes app
TAXES_FIXED_TAX_RATE=0.05 # default fixed tax rate for taxes app
TAXES_DEFAULT_COMPENSATIONS_RATE=0.75 # default compensations rate for taxes app
```
