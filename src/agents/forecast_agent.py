from forecasting.data_loader import load_demand
from forecasting.preprocessing import preprocess
from forecasting.trainer import train
from forecasting.predictor import predict
from database.forecast_repository import save_forecast


class ForecastAgent:

    def run(self):

        data = load_demand()

        clean = preprocess(data)

        model = train(clean)

        forecast = predict(model)

        save_forecast(forecast)

        return forecast