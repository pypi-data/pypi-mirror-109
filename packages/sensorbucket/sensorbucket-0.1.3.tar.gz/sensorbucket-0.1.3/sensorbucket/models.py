from dataclasses import dataclass, field
from typing import Optional
from dataclasses_json import dataclass_json
from datetime import datetime
from marshmallow import fields


@dataclass_json
@dataclass
class Location:
    """Represents a static measurement location of an organisation

    Attributes
    ----------
    id : int
        The location id of the measurements
    name : str
        ID or name of the measurement type
    ownerId : int
        The start time of the time window
    description : str
        The end time of the time windows
    coordinates : dict
        ID or name of the measurement type
    address : Optional[str]
        The start time of the time window
    city : Optional[str]
        The end time of the time windows
    """
    id: int
    name: str
    ownerId: int
    description: str
    coordinates: dict
    address: Optional[str] = None
    city:  Optional[str] = None


@dataclass_json
@dataclass
class MeasurementType:
    """Represents the type of a measurement, this also contains a the unit.
    These types are defined by the system

    Attributes
    ----------
    id : int
        The identifier for measurement type
    name : str
        The name of the measurement type
    description : str
        A short description of this measurement type
    unit : str
        The unit in which the values of this measurement type is stored
    """
    id: int
    name: str
    description: str
    unit: str


@dataclass_json
@dataclass
class Measurement:
    """Represents a measurement with all metadata. Note that properties contain 
    the value at the moment of the measurement. To filter, use the `Id` properties


    Attributes
    ----------
    id : int
        The identifier for this measurement
    timestamp : datetime
        The date and time on which the measurement was performed / stored
    latitude : float
        The latitude of the coordinates where the measurement was performed
    longitude : float
        The longitude of the coordinates where the measurement was performed
    value : float
        The value of the measurement
    deviceId : int
        The ID of the device that performed the measurement
    deviceDescription : str
        The description of the device that performed the measurement
    deviceTypeId : str
        The ID of the type of the device that performed the measurement
    deviceTypeDescription : str
        The description of the type of the device that performed the measurement
    deviceTypeMobile : bool
        Whether the device is mobile
    measurementTypeId : int
        The ID of the type of measurement that was performed
    measurementTypeName : str
        The name of the type of measurement that was performed
    measurementTypeDescription : str
        The description of the type of measurement that was performed
    measurementTypeUnit : str
        The unit of the type of measurement that was performed
    orgnisationId : int
        The organisation which this measurement belongs to
    orgnaisationName : str
        The name of the organisation which this measurement belongs to
    organisationAddress : str
        The address of the organisation which this measurement belongs to
    organisationZipcode : str
        The Zipcode of the organisation which this measurement belongs to
    organisationCity : str
        The city of the organisation which this measurement belongs to
    locationId : int
        The ID of the location where the measurement was performed. Only available
        if the device is not mobile.
    locationName : str
        The name of the location where the measurement was performed. Only available
        if the device is not mobile.
    locationAddress : str
        (Almost always None)
        The address of the location where the measurement was performed. Only available
        if the device is not mobile.
    locationCity : str
        (Almost always None)
        The city of the location where the measurement was performed. Only available
        if the device is not mobile.
    """
    id: int
    # Timestamp is defined with a custom encoder/decoder to encode/decode from
    # ISO8601 which the API returns/expects
    timestamp: datetime = field(
        metadata={'dataclasses_json': {
            'encoder': datetime.isoformat,
            'decoder': datetime.fromisoformat,
            'mm_field': fields.DateTime(format='iso')
        }}
    )
    latitude: float
    longitude: float
    value: float
    deviceId: int
    deviceDescription: str
    deviceTypeId: str
    deviceTypeDescription: str
    deviceTypeMobile: bool
    measurementTypeId: int
    measurementTypeName: str
    measurementTypeDescription: str
    measurementTypeUnit: str
    orgnisationId: int
    orgnaisationName: str
    organisationAddress: str
    organisationZipcode: str
    organisationCity: str
    locationId: int
    locationName: str
    locationAddress: str
    locationCity: str
