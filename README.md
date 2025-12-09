# wpu-cli

CLI application for make some automation tasks.

## Environment Variables

### Taxes App

- `API_BASE_URL`: URL for used API  
- `API_VERSION`: API version  
- `DEFAULT_GROSS_SALARY`: Default gross salary for calculate salary tax e.g. 837000  
- `DEFAULT_GENERATE_AMOUNT`: Default amount for generate salary sequence e.g. 1000000  
- `DEFAULT_GENERATE_COMPENSATIONS_RATE`: Default compensations rate for generate salary sequence e.g. 0.75  

### Edutech App

- `EDUTECH_USERNAME`: Edutech username
- `EDUTECH_PASSWORD`: Edutech password

### Fuzz App

- `DEFAULT_ACCURACY`: Default accuracy for fuzzy matching e.g. `60`
- `DEFAULT_LIMIT`: Default limit for fuzzy matching e.g. `5`
- `DEFAULT_SCORER`: Default scorer for fuzzy matching e.g. `q`
- `DEFAULT_REMOVE_DUPLICATED`: Default remove duplicated for fuzzy matching e.g. `1` for `True`
- `DEFAULT_WRITER`: Default writer for fuzzy matching e.g. `choices-xlsx`

### Whatsapp App

- `DEFAULT_TIMEOUT_BETWEEN_MESSAGES`: Default timeout between messages for whatsapp app e.g. `3`
- `DEFAULT_PAGELOAD_TIMEOUT`: Default pageload timeout for whatsapp app e.g. `10000`

### Common

- `SALARIES_EXCEL_FILE_PASSWORD`: Password for Salaries.xlsb file
- `PLAYWRIGHT_TIMEOUT`: Timeout for playwright e.g. 5000
