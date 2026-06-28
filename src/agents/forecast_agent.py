from src.forecasting.data_loader import load_demand
from src.forecasting.preprocessing import preprocess
from src.forecasting.trainer import train
from src.forecasting.predictor import predict
from src.database.forecast_repository import save_forecast


class ForecastAgent:

    def run(self):

        data = load_demand()
        print("DATA RETRIVAL\n")
        print(data)

        clean = preprocess(data)
        print("CLEANED DATA\n")
        print(clean)

        model = train(clean)
        print("MODEL\n")
        print(model)

        forecast = predict(model)
        print("FORECAST\n")
        print(forecast)
        forecast['yhat'] = forecast['yhat'].astype(int)
        forecast = forecast.rename(
            columns={
                "ds": "forecast_date",
                "yhat": "predicted_demand"
            }
        )

        save_forecast(forecast)
        print("FORECAST SAVED")

        return forecast