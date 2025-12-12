# wpu-cli

CLI application for make some automation tasks.

## Environment Variables

### Edutech App

- `EDUTECH_USERNAME`: Edutech username
- `EDUTECH_PASSWORD`: Edutech password
- `TIMEOUT_AFTER_INSERTING_ROWS`: Timeout for playwright e.g. 5000

### Fuzz App

- `DEFAULT_ACCURACY`: Default accuracy for fuzzy matching e.g. `60`
- `DEFAULT_LIMIT`: Default limit for fuzzy matching e.g. `5`
- `DEFAULT_SCORER`: Default scorer for fuzzy matching e.g. `q`
- `DEFAULT_REMOVE_DUPLICATED`: Default remove duplicated for fuzzy matching e.g. `1` for `True`
- `DEFAULT_WRITER`: Default writer for fuzzy matching e.g. `choices-xlsx`

### Whatsapp App

- `DEFAULT_TIMEOUT_BETWEEN_MESSAGES`: Default timeout between messages for whatsapp app e.g. `3`
- `DEFAULT_PAGELOAD_TIMEOUT`: Default pageload timeout for whatsapp app e.g. `10000`

### Template App

- `DEFAULT_TEMPLATE_GENERATED_SINGLE_FILE_NAME`: Default filename for generated single file e.g. `output`
- `DEFAULT_TEMPLATE_GENERATE_SINGLE_FILE_DATA_KEY`: Default data key for generated single file e.g. `data`
- `DEFAULT_TEMPLATE_MULTIPLE_ROWS_GROUPED_KEY`: Default grouped key for generated multiple rows e.g. `data`
