def predict(model):

    future = (
        model.make_future_dataframe(
            periods=30
        )
    )

    forecast = model.predict(
        future
    )

    return forecast[
        ["ds","yhat"]
    ].tail(30)