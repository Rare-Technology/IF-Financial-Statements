from ourfish.models import (
    AuthUser, FishdataBuyer, FishdataFishsales,
    FishdataCatch, FishdataExpense, FishdataSupplypurchases
)
from django.contrib.auth.models import User
from django.utils.translation import get_language, activate, gettext as _
import pandas as pd
import numpy as np
from datetime import datetime
import json
from babel.numbers import format_currency
from babel.core import get_global

"""
notes

Expense types:
0 - Cash payment from fisher
1 - Cash payment or loan to fisher
2 - Ice
3 - Fuel
4 - Custom supply

Expense table flags:
ispayment - Buyer is paying for fish using e.g. fuel
isdonation - Buyer is donating supplies to fisher. Not part of income or cashflow
"""

def fish_profit(buyer):
    """Calculate profit from fish transactions.

    fish profit = fish revenue - fish cost
    fish revenue = fish sold
    fish cost = fish bought or received as payment (these are essentially fish paid with a loan given to the fisher)

    Using transaction data from FishdataFishinventory.

    Arguments:
    buyer -- FishdataBuyer object

    Returns:
    fish_income -- DataFrame containing revenue, costs, and profit
    """
    fish_catch = FishdataCatch.objects.filter(buyer = buyer)
    fish_sales = FishdataFishsales.objects.filter(buyer = buyer)

    if len(fish_sales) == 0:
        revenue = []
        revenue_date = []
    else:
        revenue = [obj.total_price for obj in fish_sales]
        revenue_date = [obj.date for obj in fish_sales]
    if len(fish_catch) == 0:
        expenses = []
        expenses_date = []
    else:
        expenses = [json.loads(obj.data)['total_price'] for obj in fish_catch]
        expenses_date = [obj.date for obj in fish_catch]

    revenue_transactions = {
        'Revenue': revenue,
        'date': revenue_date
    }
    expenses_transactions = {
        'Expenses': expenses,
        'date': expenses_date
    }
    revenue_transactions = pd.DataFrame(data = revenue_transactions)
    expenses_transactions = pd.DataFrame(data = expenses_transactions)

    revenue_transactions['date'] = revenue_transactions['date'].apply(lambda x: x.date().replace(day = 1))
    expenses_transactions['date'] = expenses_transactions['date'].apply(lambda x: x.date().replace(day = 1))

    fish_revenue = revenue_transactions.groupby(by = 'date').sum()
    fish_expenses = expenses_transactions.groupby(by = 'date').sum()

    fish_income = fish_revenue.join(fish_expenses, how = 'outer').fillna(0)
    fish_income['Profit'] = fish_income['Revenue'] - fish_income['Expenses']

    return fish_income

def supplies_profit(buyer):
    """Calculate profit from supply transactions

    supply profit = supply revenue - supply cost

    Where supply revenue is pulled from FishdataExpense costs are pulled from
    FishdataSupplypurchases.

    Arguments:
    buyer -- FishdataBuyer object

    Returns:
    supplies_income -- DataFrame containing revenue, costs, and profit
    """
    fishdata_expenses = FishdataExpense.objects.filter(
        buyer = buyer,
        expense_type__in = [2, 3, 4],
        isdonation = False,
        ispayment = False
    )
    supply_purchases = FishdataSupplypurchases.objects.filter(
        buyer = buyer,
        type_of_supply__in = [0, 1, 2]
    )

    if len(fishdata_expenses) == 0:
        revenue = []
        revenue_date = []
    else:
        revenue = [obj.total_price for obj in fishdata_expenses]
        revenue_date = [obj.date for obj in fishdata_expenses]
    if len(supply_purchases) == 0:
        expenses = []
        expenses_date = []
    else:
        expenses = [obj.total_paid_amount for obj in supply_purchases]
        expenses_date = [obj.purchase_date for obj in supply_purchases]

    revenue_transactions = {
        'date': revenue_date,
        'Revenue': revenue
    }
    expenses_transactions = {
        'date': expenses_date,
        'Expenses': expenses
    }
    revenue_transactions = pd.DataFrame(data = revenue_transactions)
    expenses_transactions = pd.DataFrame(data = expenses_transactions)

    revenue_transactions['date'] = revenue_transactions['date'].apply(lambda x: x.date().replace(day = 1))
    expenses_transactions['date'] = expenses_transactions['date'].apply(lambda x: x.date().replace(day = 1))

    supply_revenue = revenue_transactions.groupby(by = 'date').sum()
    supply_expenses = expenses_transactions.groupby(by = 'date').sum()
    supply_expenses['Expenses'] = -supply_expenses['Expenses']

    supplies_income = supply_revenue.join(supply_expenses, how='outer').fillna(0)
    supplies_income['Profit'] = supplies_income['Revenue'] - supplies_income['Expenses']

    return supplies_income

def supplies_inventory(buyer):
    """Keep track of supplies

    supply inventory = supplies in - supplies out
    supplies in = supplies bought (equivelent to expenses from supplies_profit)
    supplies out = supplies sold + supplies used as payment + supplies donated

    Arguments:
    buyer -- FishdataBuyer object

    Returns:
    supply_inventory -- Dataframe containing supply inventory
    """
    supply_purchases = FishdataSupplypurchases.objects.filter(
        buyer = buyer,
        type_of_supply__in = [0, 1, 2]
    )
    fishdata_expenses = FishdataExpense.objects.filter(
        buyer = buyer,
        expense_type__in = [2, 3, 4],
    ) # includes supplies sold, used as payment (ispayment = True), and donated (isdonation = True)

    supplies_in = []
    supplies_in_date = []
    if len(supply_purchases) > 0:
        supplies_in = [obj.total_paid_amount for obj in supply_purchases]
        supplies_in_date = [obj.purchase_date for obj in supply_purchases]

    supplies_out = []
    supplies_out_date = []
    if len(fishdata_expenses) > 0:
        supplies_out = [obj.total_price for obj in fishdata_expenses]
        supplies_out_date = [obj.date for obj in fishdata_expenses]

    supplies_in_transactions = {
        'date': supplies_in_date,
        'Supplies in': supplies_in
    }
    supplies_out_transactions = {
        'date': supplies_out_date,
        'Supplies out': supplies_out
    }
    supplies_in_transactions = pd.DataFrame(data = supplies_in_transactions)
    supplies_out_transactions = pd.DataFrame(data = supplies_out_transactions)

    supplies_in_transactions['date'] = supplies_in_transactions['date'].apply(lambda x: x.date().replace(day = 1))
    supplies_out_transactions['date'] = supplies_out_transactions['date'].apply(lambda x: x.date().replace(day = 1))

    supplies_in = supplies_in_transactions.groupby(by = 'date').sum()
    supplies_out = supplies_out_transactions.groupby(by = 'date').sum()
    supplies_in['Supplies in'] = -supplies_in['Supplies in']

    supplies = supplies_in.join(supplies_out, how='outer').fillna(0)
    supplies['Supply inventory'] = supplies['Supplies in'] - supplies['Supplies out']

    return supplies['Supply inventory']

def fish_inventory(buyer):
    """Keep track of fish inventory

    supply inventory = fish in - fish out
    fish in = fish bought or received as payment
    fish out = fish sold

    Arguments:
    buyer -- FishdataBuyer object

    Returns:
    fish -- Dataframe containing supply inventory
    """
    fish_catch = FishdataCatch.objects.filter(buyer = buyer)
    fish_sales = FishdataFishsales.objects.filter(buyer = buyer)

    supplies_in = []
    supplies_in_date = []
    if len(supply_purchases) > 0:
        supplies_in = [obj.total_paid_amount for obj in supply_purchases]
        supplies_in_date = [obj.purchase_date for obj in supply_purchases]

    supplies_out = []
    supplies_out_date = []
    if len(fishdata_expenses) > 0:
        supplies_out = [obj.total_price for obj in fishdata_expenses]
        supplies_out_date = [obj.date for obj in fishdata_expenses]

    supplies_in_transactions = {
        'date': supplies_in_date,
        'Supplies in': supplies_in
    }
    supplies_out_transactions = {
        'date': supplies_out_date,
        'Supplies out': supplies_out
    }
    supplies_in_transactions = pd.DataFrame(data = supplies_in_transactions)
    supplies_out_transactions = pd.DataFrame(data = supplies_out_transactions)

    supplies_in_transactions['date'] = supplies_in_transactions['date'].apply(lambda x: x.date().replace(day = 1))
    supplies_out_transactions['date'] = supplies_out_transactions['date'].apply(lambda x: x.date().replace(day = 1))

    supplies_in = supplies_in_transactions.groupby(by = 'date').sum()
    supplies_out = supplies_out_transactions.groupby(by = 'date').sum()
    supplies_in['Supplies in'] = -supplies_in['Supplies in']

    supplies = supplies_in.join(supplies_out, how='outer').fillna(0)
    supplies['Supply inventory'] = supplies['Supplies in'] - supplies['Supplies out']

    return supplies['Supply inventory']


def generate_income_statement(buyer):
    """ Use fish_profit and supplies_profit to produce a dictionary of figures """
    fish_income = fish_profit(buyer)
    supplies_income = supplies_profit(buyer)

    income = fish_income.join(supplies_income, how='outer', lsuffix='_Fish', rsuffix='_Supplies').fillna(0)
    income['Revenue_Total'] = income['Revenue_Fish'] + income['Revenue_Supplies']
    income['Expenses_Total'] = income['Expenses_Fish'] + income['Expenses_Supplies']
    income['Profit_Total'] = income['Profit_Fish'] + income['Profit_Supplies']

    income = income.rename({
        'Profit_Fish': 'Profit (Loss)_Fish',
        'Profit_Supplies': 'Profit (Loss)_Supplies',
        'Profit_Total': 'Net income_Total',
    }, axis = 1)

    return income

def accounts_receivable_summary(buyer):
    owed_data = FishdataExpense.objects.filter( # loans and supply sales
        buyer = buyer,
        expense_type__in = [1, 2, 3, 4],
        isdonation = False,
        ispayment = False
    )
    cash_payment_data = FishdataExpense.objects.filter( # cash payments from fisher
        buyer = buyer,
        expense_type = 0,
        isdonation = False
    )
    fish_payment_data = FishdataCatch.objects.filter( # fish payments from fisher
        buyer = buyer
    )

    owed = []
    owed_dates = []
    loan_terms = ['loan', 'prestamo', 'pinjaman']
    # Among the objects with expense_type = 1 (cash payments/loans issued), keep only the
    # objects that are related to loans i.e. have 'loan' or translations in the `note` field
    owed_data_filter = []
    # this is not very elegant but can't have these conditionals in one line when notes
    # is None since .lower() cannot be used on None
    for obj in owed_data:
        if obj.expense_type == 1 and obj.notes is not None:
            if any(term for term in loan_terms if term in obj.notes.lower()):
                owed_data_filter.append(obj)
        elif obj.expense_type != 1:
            owed_data_filter.append(obj)
    if len(owed_data) > 0:
        owed = [obj.total_price for obj in owed_data_filter]
        owed_dates = [obj.date for obj in owed_data_filter]

    received = []
    received_dates = []
    if len(cash_payment_data) > 0:
        received += [obj.total_price for obj in cash_payment_data]
        received_dates += [obj.date for obj in cash_payment_data]
    if len(fish_payment_data) > 0:
        # We are interested in the catch transactions where the fisher uses the fish as cash payment.
        # This is denoted by the 'isPayment' flag in a FishdataCatch object's `data` column
        # However, that flag was not introduced until July 2021, so we will filter the catch data to only
        # those transactions which include an isPayment flag, and from there filter to only the ones with
        # `isPayment` = True
        fish_payment_data_isPayment = [obj for obj in fish_payment_data if 'isPayment' in json.loads(obj.data).keys()]
        json_data = [json.loads(obj.data) for obj in fish_payment_data_isPayment]
        received += [jdata['total_price'] for jdata in json_data if jdata['isPayment'] == True]
        received_dates += [obj.date for obj in fish_payment_data_isPayment if json.loads(obj.data)['isPayment'] == True]


    owed_transactions = pd.DataFrame(data = {
        'Owed': owed,
        'date': owed_dates
    })
    received_transactions = pd.DataFrame(data = {
        'Received': received,
        'date': received_dates
    })

    owed_transactions['date'] = owed_transactions['date'].apply(lambda x: x.date().replace(day = 1))
    received_transactions['date'] = received_transactions['date'].apply(lambda x: x.date().replace(day = 1))

    owed_summary = owed_transactions.groupby(by = 'date').sum()
    received_summary = received_transactions.groupby(by = 'date').sum()

    summary = owed_summary.join(received_summary, how = 'outer').fillna(0)
    summary['Accounts Receivable'] =  summary['Owed'] - summary['Received']

    return summary

def accounts_payable_summary(buyer):
    # Add payments made w/ supplies
    debt_data = FishdataCatch.objects.filter(buyer = buyer)
    paid_data = FishdataExpense.objects.filter(
        buyer = buyer,
        expense_type__in = [1, 2, 3, 4] # cash for fish and loans
    )

    paid = []
    paid_dates = []
    if len(paid_data) > 0:
        loan_terms = ['loan', 'prestamo', 'pinjaman']
        # remove rows which represent issuing loans
        paid_data_filter = []
        for obj in paid_data:
            if obj.expense_type == 1 and obj.notes is not None: # cash payments w/ a memo
                if not any(term for term in loan_terms if term in obj.notes.lower()):
                    paid_data_filter.append(obj)
            elif obj.expense_type == 1: # cash payments w/ no memo
                paid_data_filter.append(obj)
            elif obj.ispayment == True: # supply payments
                paid_data_filter.append(obj)
        paid += [obj.total_price for obj in paid_data_filter]
        paid_dates += [obj.date for obj in paid_data_filter]
    debt = []
    debt_dates = []
    if len(debt_data) > 0:
        # Similar to what was done in the accounts receivable summary func, we first
        # filter to only catch tranactions that include a `isPayment` flag, then we
        # filter to only those that have `isPayment` = False
        debt_data_isPayment = [obj for obj in debt_data if 'isPayment' in json.loads(obj.data).keys()]
        json_data = [json.loads(obj.data) for obj in debt_data_isPayment]
        debt += [jdata['total_price'] for jdata in json_data if jdata['isPayment'] == False]
        debt_dates += [obj.date for obj in debt_data_isPayment if json.loads(obj.data)['isPayment'] == False]

    paid_transactions = pd.DataFrame(data = {
        'Paid': paid,
        'date': paid_dates
    })
    debt_transactions = pd.DataFrame(data = {
        'Debt': debt,
        'date': debt_dates
    })

    paid_transactions['date'] = paid_transactions['date'].apply(lambda x: x.date().replace(day = 1))
    debt_transactions['date'] = debt_transactions['date'].apply(lambda x: x.date().replace(day = 1))

    paid_summary = paid_transactions.groupby(by = 'date').sum()
    debt_summary = debt_transactions.groupby(by = 'date').sum()

    summary = paid_summary.join(debt_summary, how = 'outer').fillna(0)
    summary['Accounts Payable'] = summary['Debt'] - summary['Paid']

    return summary

def negative_accounts(row):
    """
    After joining accounts payable and receivable, check for negative values.
    Convert negative values to positive to move to the opposite cashflow type.

    Example: Accounts payable on June 2021 is -100 while accounts receivable is 50.
    Then set accounts payable that month to 0 and accounts receivable to 150.

    This goes into .apply() on `cashflow`, so `row` is a row from `cashflow`
    """
    tmp_payable = 0
    tmp_receivable = 0

    if row['Accounts Payable'] < 0:
        tmp_payable = -row['Accounts Payable']
        row['Accounts Payable'] = 0

    if row['Accounts Receivable'] < 0:
        tmp_receivable = -row['Accounts Receivable']
        row['Accounts Receivable'] = 0

    row['Accounts Payable'] += tmp_receivable
    row['Accounts Receivable'] += tmp_payable

    return row



def generate_cashflow_statement(buyer, income):
    """ Calculate accounts receivable/payable and produce dictionary of figures """
    accounts_receivable = accounts_receivable_summary(buyer)
    accounts_payable = accounts_payable_summary(buyer)
    supplies = supplies_inventory(buyer)

    cashflow = accounts_payable.join(accounts_receivable, how='outer')
    cashflow = cashflow.apply(negative_accounts, axis = 1)
    cashflow = cashflow.join(income, how = 'outer').join(supplies, how = 'outer').fillna(0)
    cashflow['Total Cash'] = cashflow['Net income_Total'] - cashflow['Accounts Receivable'] + cashflow['Accounts Payable']
    cashflow = cashflow[['Net income_Total', 'Accounts Receivable', 'Accounts Payable', 'Total Cash', 'Supply inventory']]
    cashflow = cashflow.rename({
        'Net income_Total': 'Net income',
        'Accounts Receivable': 'Changes in accounts receivable',
        'Accounts Payable': 'Changes in accounts payable',
        'Total Cash': 'Total cash from fisheries operations',
        'Supply inventory': 'Changes in supply inventory'
    }, axis = 1)

    return cashflow

locale_dict = {
# Map the country from OF user data to locale strings that can be read by babel
# There should be a better way to do this, this is very manual and will have to
# be modified whenever country info from OF changes
    'United States of America': 'en_US',
    'Indonesia': 'id_ID'
}

currency_dict = {
    # similar to locale_dict; at some point write this in a more generalizable way.
    # Tried using babel.core.get_global('territory_currencies') but it returns a list
    # of historical currencies not necessarily in chronological order, so would
    # have to think of how to get the right currency every time
    'en_US': 'USD',
    'id_ID': 'IDR'
}

def format_data(buyer, data):
    try:
        buyer_locale = locale_dict[buyer.installation.country.name]
    except KeyError: # either missing country info in the data or country info is not in locale_dict
        buyer_locale = 'en_US'

    # Don't actually need currency symbol so it's left blank here, but format_currency
    # is used over format_decimal since it automatically truncates the decimal places
    # The `format` argument rounds values as integers
    out = format_currency(data, '', format = u'#,##0.', locale = buyer_locale)
    if out[0] == '-': # negative
        out = '(' + out[1:] + ')'

    return out

def get_currency(buyer):
        try:
            buyer_locale = locale_dict[buyer.installation.country.name]
        except KeyError: # either missing country info in the data or country info is not in locale_dict
            buyer_locale = 'en_US'

        try:
            return currency_dict[buyer_locale]
        except KeyError:
            return currency_dict['en_US']

month_translations = {
    'Jan': _('Jan'),
    'Feb': _('Feb'),
    'Mar': _('Mar'),
    'Apr': _('Apr'),
    'May': _('May'),
    'Jun': _('Jun'),
    'Jul': _('Jul'),
    'Aug': _('Aug'),
    'Sep': _('Sep'),
    'Oct': _('Oct'),
    'Nov': _('Nov'),
    'Dec': _('Dec')
}

def translate_date(month_year):
    month, year = [s for s in month_year.split(' ')]
    trans_month = month_translations[month]
    trans_month_year = ' '.join([trans_month, year])

    return trans_month_year
