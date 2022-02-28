from ourfish.models import (
    AuthUser, FishdataBuyer, FishdataFishsales,
    FishdataCatch, FishdataExpense, FishdataSupplypurchases
)
from django.contrib.auth.models import User
import pandas as pd
import numpy as np
from datetime import datetime
import json

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

def generate_income_statement(user):
    """ Use fish_profit and supplies_profit to produce a dictionary of figures """
    of_user = AuthUser.objects.get(username = user.username)
    buyer = FishdataBuyer.objects.get(user = of_user)

    fish_income = fish_profit(buyer)
    supplies_income = supplies_profit(buyer)

    income = fish_income.join(supplies_income, how='outer', lsuffix='_Fish', rsuffix='_Supplies').fillna(0)
    income['Revenue_Total'] = income['Revenue_Fish'] + income['Revenue_Supplies']
    income['Expenses_Total'] = income['Expenses_Fish'] + income['Expenses_Supplies']
    income['Profit_Total'] = income['Profit_Fish'] + income['Profit_Supplies']

    income.index = income.index.map(lambda x: x.strftime('%b %Y'))

    return income

def generate_cashflow_statement(user, income_statement):
    """ Calculate accounts recievable/payable and produce dictionary of figures """
    pass
