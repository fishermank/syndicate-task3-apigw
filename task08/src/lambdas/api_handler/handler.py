import json

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


import asyncio

from open_meteo import OpenMeteo
from open_meteo.models import DailyParameters, HourlyParameters


class MeteoForecast:

    @staticmethod
    async def _main():
        """Show example on using the Open-Meteo API client."""
        async with OpenMeteo() as open_meteo:
            forecast = await open_meteo.forecast(
                latitude=52.52,
                longitude=13.41,
                current_weather=True,
                hourly=[
                    HourlyParameters.TEMPERATURE_2M,
                    HourlyParameters.RELATIVE_HUMIDITY_2M,
                    HourlyParameters.WIND_SPEED_10M,
                ],
            )
            result = json.loads(forecast.json())

        print(result)
        return result

    def get_weather_forecast(self):
        return asyncio.run(self._main())


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        if 'rawPath' in event:
            print(f'rawPath: {event["rawPath"]}')
        mf = MeteoForecast()
        forecast = mf.get_weather_forecast()

        return forecast


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
