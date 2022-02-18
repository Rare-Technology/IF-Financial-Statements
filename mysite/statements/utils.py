from ourfish.models import (
    AuthUser, FishdataFishsales, FishdataFishinventory,
    FishdataCatch, FishdataExpense, FishdataSupplypurchases
)

def fish_profit(user, start_date, end_date):
    """Calculate profit from fish transactions.

    fish profit = fish revenue - fish cost

    Where fish revenue is pulled from FishdataFishsales/FishdataFishinventory and
    costs are pulled from FishdataCatch

    Arguments:
    user -- User object
    start_date -- Date
    end_date -- Date

    Returns:
    fish_numbers -- Dictionary containing revenue, costs, and profit
    """
    pass

def supplies_profit(user, start_date, end_date):
    """Calculate profit from supply transactions

    supply profit = supply revenue - supply cost

    Where supply revenue is pulled from FishdataExpense costs are pulled from
    FishdataSupplypurchases.

    Arguments:
    user -- User object
    start_date -- Date
    end_date -- Date

    Returns:
    supply_numbers -- Dictionary containing revenue, costs, and profit
    """
    pass

def generate_income_statement(user, start_date, end_date):
    """ Use fish_profit and supplies_profit to produce a dictionary of figures """
     pass

def generate_cashflow_statement(user, start_date, end_date, income_statement):
    """ Calculate accounts recievable/payable and produce dictionary of figures """
    pass
