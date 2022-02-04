import pandas as pd
from statements.models import Catches

def main():
    df = pd.read_csv("./static/ourfish_sample.csv")

    samples = [
        Catches(
            id = row['id'],
            buyer_id = row['buyer_id'],
            buyer_name = row['buyer_name'],
            fisher_id = row['fisher_id'],
            date = row['date'],
            total_price = row['total_price']
        )

        for idx, row in df.iterrows()
    ]

    Catches.objects.bulk_create(samples)
