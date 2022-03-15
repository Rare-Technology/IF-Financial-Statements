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

def fish_profit(buyer):
    """Calculate profit from fish transactions.

    fish profit = fish revenue - fish cost

    Using transaction data from FishdataFishinventory.

    Arguments:
    buyer -- FishdataBuyer object

    Returns:
    fish_income -- DataFrame containing revenue, costs, and profit
    """
    fish_catch = FishdataCatch.objects.filter(buyer = buyer)
    fish_sales = FishdataFishsales.objects.filter(buyer = buyer)

    if len(fish_catch) == 0:
        revenue = []
        revenue_date = []
    else:
        revenue = [obj.total_price for obj in fish_sales]
        revenue_date = [obj.date for obj in fish_sales]
    if len(fish_sales) == 0:
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
    fish_expenses['Expenses'] = fish_expenses['Expenses']

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
    supplies_income -- Dictionary containing revenue, costs, and profit
    """
    fishdata_expenses = FishdataExpense.objects.filter(
        buyer = buyer,
        expense_type__in = [3, 4]
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

def generate_income_statement(buyer):
    """ Use fish_profit and supplies_profit to produce a dictionary of figures """
    fish_income = fish_profit(buyer)
    supplies_income = supplies_profit(buyer)

    income = fish_income.join(supplies_income, how='outer', lsuffix='_Fish', rsuffix='_Supplies').fillna(0)
    income['Revenue_Total'] = income['Revenue_Fish'] + income['Revenue_Supplies']
    income['Expenses_Total'] = income['Expenses_Fish'] + income['Expenses_Supplies']
    income['Profit_Total'] = income['Profit_Fish'] + income['Profit_Supplies']
    income = income.rename({
        'Revenue_Fish': _('Revenue_Fish'),
        'Revenue_Suplies': _('Revenue_Supplies'),
        'Revenue_Total': _('Revenue_Total'),
        'Expenses_Fish': _('Expenses_Fish'),
        'Expenses_Supplies': _('Expenses_Supplies'),
        'Expenses_Total': _('Expenses_Total'),
        'Profit_Fish': _('Profit (Loss)_Fish'),
        'Profit_Supplies': _('Profit (Loss)_Supplies'),
        'Profit_Total': _('Net income_Total')
    }, axis = 1)

    income.index = income.index.map(lambda x: x.strftime('%b %Y'))

    return income

def accounts_receivable_summary(buyer):
    owed_data = FishdataExpense.objects.filter(
        buyer = buyer,
        expense_type = 1, # cash for fish and loans
    )
    received_data = FishdataExpense.objects.filter(
        buyer = buyer,
        expense_type = 0,
        ispayment = True # payments made by fisher
    )

    if len(owed_data) == 0: # TODO write this better... can probably initiate these lists as [] then append data
        owed = []
        owed_dates = []
    else:
        loan_terms = ['loan', 'prestamo', 'pinjaman']
        # keep only the rows that are related to loans i.e. have 'loan' or translations in the `note` field
        owed_data_filter = []
        # this is not very elegant but can't have these conditionals in one line when notes
        # is None since .lower() cannot be used on None
        for obj in owed_data:
            if obj.notes is not None:
                if any(term for term in loan_terms if term in obj.notes.lower()):
                    owed_data_filter.append(obj)
        owed = [obj.total_price for obj in owed_data_filter]
        owed_dates = [obj.date for obj in owed_data_filter]
    if len(received_data) == 0:
        received = []
        receieved_dates = []
    else:
        received = [obj.total_price for obj in received_data]
        received_dates = [obj.date for obj in received_data]

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
    summary['Accounts Receivable'] = summary['Owed'] - summary['Received']

    return summary

def accounts_payable_summary(buyer):
    debt_data = FishdataCatch.objects.filter(buyer = buyer)
    paid_data = FishdataExpense.objects.filter(
        buyer = buyer,
        expense_type = 1 # cash for fish and loans
    )

    if len(paid_data) == 0:
        paid = []
        paid_dates = []
    else:
        loan_terms = ['loan', 'prestamo', 'pinjaman']
        # remove rows which represent issuing loans
        paid_data_filter = []
        for obj in paid_data:
            if obj.notes is None:
                paid_data_filter.append(obj)
            else:
                if not any(term for term in loan_terms if term in obj.notes.lower()):
                    paid_data_filter.append(obj)
        paid = [obj.total_price for obj in paid_data_filter]
        paid_dates = [obj.date for obj in paid_data_filter]
    if len(debt_data) == 0:
        debt = []
        debt_dates = []
    else:
        debt = [json.loads(obj.data)['total_price'] for obj in debt_data]
        debt_dates = [obj.date for obj in debt_data]

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

def generate_cashflow_statement(buyer, income):
    """ Calculate accounts receivable/payable and produce dictionary of figures """
    accounts_receivable = accounts_receivable_summary(buyer)
    accounts_payable = accounts_payable_summary(buyer)

    cashflow = accounts_payable.join(accounts_receivable, how='outer').fillna(0)
    cashflow.index = cashflow.index.map(lambda x: x.strftime('%b %Y'))
    cashflow = cashflow.join(income, how = 'outer').fillna(0)
    cashflow['Total Cash'] = cashflow['Net income_Total'] - cashflow['Accounts Receivable'] + cashflow['Accounts Payable']
    cashflow = cashflow[['Net income_Total', 'Accounts Receivable', 'Accounts Payable', 'Total Cash']]
    cashflow = cashflow.rename({
        'Net income_Total': _('Net income'),
        'Accounts Receivable': _('Accounts receivable'),
        'Accounts Payable': _('Accounts payable'),
        'Total Cash': _('Total cash')
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
    out = format_currency(data, '', locale = buyer_locale)
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
