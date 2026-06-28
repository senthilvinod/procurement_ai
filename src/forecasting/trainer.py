from prophet import Prophet


def train(df):

    train_df = df.rename(
        columns={
            "demand_date":"ds",
            "shipped_quantity":"y"
        }
    )

    model = Prophet()

    model.fit(train_df)

    return model