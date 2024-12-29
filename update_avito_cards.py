from business_logic import card_creation
from data import accounts

def update_avito_cards():       
    for account in accounts:
        card_creation(account)