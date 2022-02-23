from ourfish.models import (
    AuthUser, FishdataBuyer, FishdataFishsales, FishdataFishinventory,
    FishdataCatch, FishdataExpense, FishdataSupplypurchases
)
from django.contrib.auth.models import User
import pandas as pd
import numpy as np
from datetime import date

def fish_profit(buyer, start_date, end_date):
    """Calculate profit from fish transactions.

    fish profit = fish revenue - fish cost

    Using transaction data from FishdataFishinventory.

    Arguments:
    buyer -- FishdataBuyer object
    start_date -- datetime.date
    end_date -- datetime.date

    Returns:
    fish_income -- DataFrame containing revenue, costs, and profit
    """
    fish_inventory = FishdataFishinventory.objects.filter(
        buyer = buyer,
        delivery_date__range = (start_date, end_date)
    )

    cash_in = [obj.total_received_amount for obj in fish_inventory]
    cash_out = [obj.total_paid_amount for obj in fish_inventory]

    revenue = np.sum(cash_in) # at some point figure out how to do this month-to-month
    cost = np.sum(cash_out)
    profit = revenue - cost

    fish_income = {
        'revenue': [revenue],
        'cost': [cost],
        'profit': [profit]
    }
    fish_income = pd.DataFrame(data = fish_income)

    return fish_income

def supplies_profit(buyer, start_date, end_date):
    """Calculate profit from supply transactions

    supply profit = supply revenue - supply cost

    Where supply revenue is pulled from FishdataExpense costs are pulled from
    FishdataSupplypurchases.

    Arguments:
    buyer -- FishdataBuyer object
    start_date -- datetime.date
    end_date -- datetime.date

    Returns:
    supplies_income -- Dictionary containing revenue, costs, and profit
    """
    expenses = FishdataExpense.objects.filter(
        buyer = buyer,
        date__range = (start_date, end_date),
        expense_type__in = [3, 4] # might be missing some here
    )
    supply_purchases = FishdataSupplypurchases.objects.filter(
        buyer = buyer,
        purchase_date__range = (start_date, end_date),
        type_of_supply__in = [0, 1, 2]
    )

    cash_in = [obj.total_price for obj in expenses]
    cash_out = [obj.total_paid_amount for obj in supply_purchases]

    revenue = np.sum(cash_in)
    cost = np.sum(cash_out)
    profit = revenue - cost

    supplies_income = {
        'revenue': [revenue],
        'cost': [cost],
        'profit': [profit]
    }
    supplies_income = pd.DataFrame(supplies_income)

    return supplies_income

def generate_income_statement(user, start_date, end_date):
    """ Use fish_profit and supplies_profit to produce a dictionary of figures """
    of_user = AuthUser.objects.get(username = user.username)
    buyer = FishdataBuyer.objects.get(user = of_user)

    fish_income = fish_profit(buyer, start_date, end_date)
    supplies_income = supplies_profit(buyer, start_date, end_date)

    income = pd.concat([fish_income, supplies_income], keys = ['Fish', 'Supplies'])
    print(income)
    return income

def generate_cashflow_statement(user, start_date, end_date, income_statement):
    """ Calculate accounts recievable/payable and produce dictionary of figures """
    pass
