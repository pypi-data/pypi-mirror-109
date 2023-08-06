import requests as r
from datetime import datetime, timedelta
from typing import List, Union

from .errors import MeasurementTypeNotFound
from .models import MeasurementType, Measurement, Location
from .jsonwebtoken import get_expiry_date


class Facade:
    """Facade is a class which simplifies your interaction with the SensorBucket API."""
    __token_refresh_window = timedelta(minutes=5)

    def __init__(self, url: str, username: str, password: str):
        """This class acts as a Facade for the SensorBucket API

        Parameters
        ----------
        url : str
            The base url for the SensorBucket API
        username : str
            Your username
        password : str
            Your password
        """
        self.url = url
        self.username = username
        self.password = password
        self.token = ""
        self.token_expire = None

    def __authenticate(self):
        """Used to reauthenticate to the api and fetch a new token
        """
        res = r.post(f"{self.url}/auth/login", json={
            "email": self.username,
            "password": self.password
        })
        res.raise_for_status()
        self.token = res.json()["data"]
        self.token_expire = get_expiry_date(self.token)

    def __get_authentication_token(self) -> str:
        """
        Returns the currently active authentication token and will automatically
        refresh the token if it is about to expire

        Returns
        -------
        str
            The authentication token
        """
        if self.token_expire == None or self.token_expire < datetime.now() - self.__token_refresh_window:
            self.__authenticate()
        return self.token

    def __measurement_type_for_name(self, name: str) -> MeasurementType:
        """Find the first MeasurementType that corresponds to the given name
        """
        types = self.get_measurement_types()
        for t in types:
            if t.name == name:
                return t
        return None

    def get_locations(self) -> List[Location]:
        """Fetches all the available locations for the authenticated user

        Returns
        -------
        List[Location]
            The locations
        """
        res = r.get(f"{self.url}/api/v1/locations", headers={
            "authorization": f"bearer {self.__get_authentication_token()}"
        })
        res.raise_for_status()
        return Location.schema().load(res.json()["data"], many=True)

    def get_measurement_types(self) -> List[MeasurementType]:
        """Fetches all available measurement types in the system

        Returns
        -------
        List[MeasurementType]
            A list of MeasurementTypes in the system
        """
        res = r.get(f"{self.url}/api/v1/measurement-types", headers={
            "authorization": f"bearer {self.__get_authentication_token()}"
        })
        res.raise_for_status()
        return MeasurementType.schema().load(res.json()["data"], many=True)

    def get_measurements(self, location_id: int, measurement_type: Union[int, str], start: Union[datetime, str], end: Union[datetime, str]) -> List[Measurement]:
        """Fetches a list of measurements from a given location in a given time window

        Parameters
        ----------
        location_id : int
            The location id of the measurements
        measurement_type : Union[int, str]
            ID or name of the measurement type
        start : Union[datetime, str]
            The start time of the time window
        end : Union[datetime, str]
            The end time of the time windows

        Returns
        -------
        List[Measurement]
            A list of measurements

        Raises
        ------
        MeasurementTypeNotFound
            Thrown if measurement_type could not be found
        """

        # `measurement_type` can be a string, so find the corresponding
        # MeasuremenType and assign the id
        if type(measurement_type) == str:
            found_type = self.__measurement_type_for_name(
                measurement_type
            )
            if found_type == None:
                raise MeasurementTypeNotFound()
            measurement_type = found_type.id

        # Start and End parameters can be datetime objects, but the API expects
        # ISO8601 strings, so convert them
        if type(start) == datetime:
            start = start.isoformat()
        if type(end) == datetime:
            end = end.isoformat()

        # Perform request to API
        query = {
            "location": location_id,
            "measurement": measurement_type,
            "start": start,
            "end": end
        }
        res = r.get(f"{self.url}/api/v1/measurements", params=query, headers={
            "authorization": f"bearer {self.__get_authentication_token()}"
        })
        res.raise_for_status()
        return Measurement.schema().load(res.json()["data"], many=True)
