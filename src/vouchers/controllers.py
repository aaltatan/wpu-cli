import math
from pathlib import Path
from typing import Literal, Any

from playwright.sync_api import sync_playwright, Page
from selectolax.parser import HTMLParser
from xlwings import Sheet
from rich.progress import track

from src import utils as src_utils


def _get_cost_center(
    faculty: str, account_id: str, chapter: Literal['1', '2', '3'] = '1'
) -> str:
    """
    get cost center from string e.g.:  
    - account_id = 4111, faculty = 'Management', chapter = 1 -> '131'  
    - account_id = 4111, faculty = 'Pharmacy', chapter = 3 -> '163'  
    - account_id = 15322, faculty = 'Management', chapter = 1 -> ''  
    """
    if account_id.startswith('1') or account_id.startswith('2'):
        return ''
    
    cost_centers: dict[str, str] = {
        'Employee': '11',
        'Architecture': '12',
        'Management': '13',
        'Engineering': '14',
        'Dentistry': '15',
        'Dentist Clinics': '15',
        'Pharmacy': '16',
        'Civil': '17',
    }
    
    return cost_centers.get(faculty, '11') + chapter


def get_salaries_voucher_data(
    filepath: Path, chapter: Literal['1', '2', '3'] = '1', 
) -> list[list[str]]:
    """
    read voucher data from salaries/partial `Journal Entry Template` file
    """
    wb = src_utils.get_salaries_workbook(filepath)
    ws: Sheet = wb.sheets['Journal Entry Template']
    
    lr = ws.range('C1').end('down').row
    rg = ws.range(f'A2:G{lr}').value
    
    data: list[list[str]] = []
    
    for r in rg:

        _, faculty, string_account, notes, debit, credit, account_id = r
        
        debit = str(int(debit or 0))
        credit = str(int(credit or 0))
        account_id = str(int(account_id or 15322))
        
        notes = f'{string_account} | {faculty or ""} \n{notes or ""}'
        
        cost_center = _get_cost_center(faculty, account_id, chapter)
        
        row = [debit, credit, account_id, cost_center, notes]
        
        data.append(row)
    
    return data


def get_voucher_data(
    filepath: Path, 
    chapter: Literal['1', '2', '3'] = '1', 
    sheet_name: str = 'voucher'
) -> list[list[str]]:
    """
    read voucher data from salaries/partial `voucher` file
    """
    wb = src_utils.get_salaries_workbook(filepath)
    ws: Sheet = wb.sheets[sheet_name]
    
    lr = ws.range('A1').end('down').row
    rg = ws.range(f'A2:E{lr}').value
    
    data: list[list[str]] = []
    
    for r in rg:

        debit, credit, account_id, faculty, notes = r
        
        debit = str(int(debit or 0))
        credit = str(int(credit or 0))
        account_id = str(int(account_id or 15322))
        
        cost_center = _get_cost_center(faculty, account_id, chapter)
        
        row = [debit, credit, account_id, cost_center, notes]
        
        data.append(row)
    
    return data


def _navigate_to_add_new_voucher(page: Page) -> Page:
    """
    navigate to add new voucher playwright
    """
    page.goto('http://edu/RAS/?sc=500#/_FIN/ACT/vouchers.php?id=JOV')
    page.wait_for_selector('#addVoucher')
    page.click('#addVoucher')
    
    return page


def _fill_field(
    page: Page, field: dict, type_: Literal['select', 'input'] = 'input'
) -> None:
    """
    fill field
    """
    if field['value'] == '':
        return
  
    page.fill(f'#{field["id"]}', str(field['value']))
    if type_ == 'select':
        page.wait_for_timeout(3_000)
        page.press('body', 'ArrowDown')
        page.press('body', 'Enter')


def _fill_row(
  page: Page,
  debit: dict,
  credit: dict,
  account: dict,
  cost_center: dict,
  notes: dict,
) -> None:
    """
    fill voucher row
    """
    _fill_field(page, debit)
    _fill_field(page, credit)
    _fill_field(page, account, type_='select')
    _fill_field(page, cost_center, type_='select')
    _fill_field(page, notes)


def _parse_ids(
        parser: HTMLParser, 
        id_start_with: str, 
        type_: Literal['input', 'textarea'] = 'input',
    ) -> list[str]:
    """
    parse all ids from range of fields
    """
    ids = parser.css(f'{type_}[id^="{id_start_with}"]')
    ids = [el.attributes.get('id') for el in ids][1:]
    
    return ids


def _parse_additional_data(parser: HTMLParser) -> list[list[Any]]:
    """
    parse all ids from all fields
    """
    data: list = []
    
    debits = _parse_ids(parser, 'sumDebitId_show')
    credits = _parse_ids(parser, 'sumCreditId_show')
    accounts = _parse_ids(parser, 'accountId__label')
    cost_centers = _parse_ids(parser, 'costCenterId__label')
    notes = _parse_ids(parser, 'detailNote_', type_='textarea')
    
    for idx in range(len(debits)):
        row = [
            debits[idx], 
            credits[idx], 
            accounts[idx], 
            cost_centers[idx], 
            notes[idx]
        ]
        data.append(row)
        
    return data


def _merge_two_lists(list_of_ids, list_of_data) -> list[dict]:

    if len(list_of_ids) != len(list_of_data):
        raise Exception('two lists must be the same length')
    
    data: list[dict] = []
    
    for idx in range(len(list_of_ids)):
      
        keys = ['debit', 'credit', 'account', 'cost_center', 'notes']

        row = {
          el[0]:{'value': el[1], 'id': el[2]} 
          for el in zip(keys, list_of_data[idx], list_of_ids[idx])
        }
        data.append(row)
    
    return data


def add_voucher(
    timeout: int, 
    data: list[list[str]], 
):
    
    with sync_playwright() as p:
        
        page = src_utils.get_authenticated_page(p)
        
        page.wait_for_timeout(timeout)
        
        page = _navigate_to_add_new_voucher(page)
        
        page.wait_for_timeout(timeout)
        
        for _ in range(len(data) - 1):
            page.press('body', 'Shift+N')
        
        timeout_factor = math.ceil(len(data) / 10)
        
        page.wait_for_timeout(timeout * timeout_factor)
        
        parser = HTMLParser(page.content())
        
        additional_data = _parse_additional_data(parser)
        
        data = _merge_two_lists(additional_data, data)
        
        total = len(data)
        
        for row in track(data, total=total):
            _fill_row(page, **row)
            
        input('Press any key to close ... ')