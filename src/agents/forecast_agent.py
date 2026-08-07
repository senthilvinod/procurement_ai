from src.forecasting.data_loader import load_demand
from src.forecasting.preprocessing import preprocess
from src.forecasting.trainer import train
from src.forecasting.predictor import predict

from src.database.forecast_repository import save_forecast

from src.forecasting.bom_loader import load_bom
from src.forecasting.bom_explosion import explode_bom
from src.forecasting.product_demand import (
    calculate_product_statistics,
)
from src.forecasting.daily_product_demand_update import (
    save_product_demand_forecast,
)

print("Forecast Agent Loaded")

class ForecastAgent:

    def run(self):

        # --------------------------------------------------
        # Load historical demand
        # --------------------------------------------------

        data = load_demand()
        print("\n========== HISTORICAL DEMAND ==========")
        print(data)

        # --------------------------------------------------
        # Preprocess
        # --------------------------------------------------

        clean = preprocess(data)
        print("\n========== CLEANED DATA ==========")
        print(clean)

        # --------------------------------------------------
        # Train Forecast Model
        # --------------------------------------------------

        model = train(clean)
        print("\n========== MODEL TRAINED ==========")
        print(model)

        # --------------------------------------------------
        # Predict next 30 days
        # --------------------------------------------------

        forecast = predict(model)

        forecast["yhat"] = forecast["yhat"].astype(int)

        forecast = forecast.rename(
            columns={
                "ds": "forecast_date",
                "yhat": "predicted_demand",
            }
        )

        print("\n========== VEHICLE FORECAST ==========")
        print(forecast)

        # --------------------------------------------------
        # Save vehicle forecast
        # --------------------------------------------------

        save_forecast(forecast)
        print("\nVehicle forecast saved.")

        # --------------------------------------------------
        # Load BOM
        # --------------------------------------------------

        bom = load_bom()

        print("\n========== BOM ==========")
        print(bom)

        # --------------------------------------------------
        # BOM Explosion
        # --------------------------------------------------

        daily_product_demand = explode_bom(
            forecast_df=forecast,
            bom_df=bom,
        )

        print("\n========== PRODUCT DEMAND ==========")
        print(daily_product_demand)

        # --------------------------------------------------
        # Calculate Product Statistics
        # --------------------------------------------------

        product_statistics = calculate_product_statistics(
            daily_product_demand
        )

        print("\n========== PRODUCT DEMAND SUMMARY ==========")
        print(product_statistics)

        # --------------------------------------------------
        # Save Product Demand Forecast
        # --------------------------------------------------

        save_product_demand_forecast(product_statistics)

        print("\nProduct demand forecast saved.")

        return {
            "vehicle_forecast": forecast,
            "product_forecast": product_statistics,
        }

def run_forecast_agent():

    agent = ForecastAgent()

    result = agent.run()

    return result

if __name__ == "__main__":
    ForecastAgent().run()