"""
..  codeauthor:: Charles Blais
"""
from typing import SupportsInt, SupportsFloat, Dict

from pyshakealert.message.event.magnitude import \
    Magnitude, MagnitudeUncertainty
from pyshakealert.message.event.coordinate import \
    Coordinate, CoordinateUncertainty
from pyshakealert.message.event.depth import \
    Depth, DepthUncertainty
from pyshakealert.message.event.origintime import \
    OriginTime, OriginTimeUncertainty


class Core(dict):
    """Event message core_info element"""
    def __init__(self, *args, **kwargs):
        super(Core, self).__init__(*args, **kwargs)
        # Create the default required objects
        # attributes
        self.id = self.id
        # elements
        self.magnitude = self.magnitude
        self.magnitude_uncertainty = self.magnitude_uncertainty
        self.latitude = self.latitude
        self.latitude_uncertainty = self.latitude_uncertainty
        self.longitude = self.longitude
        self.longitude_uncertainty = self.longitude_uncertainty
        self.depth = self.depth
        self.depth_uncertainty = self.depth_uncertainty
        self.origintime = self.origintime
        self.origintime_uncertainty = self.origintime_uncertainty
        self.likelihood = self.likelihood

    @property
    def id(self) -> str:
        """Get id"""
        return self.get('@id', '')

    @id.setter
    def id(self, value: str) -> None:
        """Set id"""
        self['@id'] = value

    @property
    def magnitude(self) -> Magnitude:
        """Get magnitude"""
        return self.get('mag', Magnitude())

    @magnitude.setter
    def magnitude(self, value: Dict) -> None:
        """Set magnitude"""
        self['mag'] = Magnitude(**value)

    @property
    def magnitude_uncertainty(self) -> MagnitudeUncertainty:
        """Get magnitude uncertainty"""
        return self.get('mag_uncer', MagnitudeUncertainty())

    @magnitude_uncertainty.setter
    def magnitude_uncertainty(self, value: Dict) -> None:
        """Set magnitude uncertainty"""
        self['mag_uncer'] = MagnitudeUncertainty(**value)

    @property
    def latitude(self) -> Coordinate:
        """Get latitude"""
        return self.get('lat', Coordinate())

    @latitude.setter
    def latitude(self, value: Dict) -> None:
        """Set latitude"""
        self['lat'] = Coordinate(**value)

    @property
    def latitude_uncertainty(self) -> CoordinateUncertainty:
        """Get latitude uncertainty"""
        return self.get('lat_uncer', CoordinateUncertainty())

    @latitude_uncertainty.setter
    def latitude_uncertainty(self, value: Dict) -> None:
        """Set latitude uncertainty"""
        self['lat_uncer'] = CoordinateUncertainty(**value)

    @property
    def longitude(self) -> Coordinate:
        """Get longitude"""
        return self.get('lon', Coordinate())

    @longitude.setter
    def longitude(self, value: Dict) -> None:
        """Set longitude"""
        self['lon'] = Coordinate(**value)

    @property
    def longitude_uncertainty(self) -> CoordinateUncertainty:
        """Get longitude uncertainty"""
        return self.get('lon_uncer', CoordinateUncertainty())

    @longitude_uncertainty.setter
    def longitude_uncertainty(self, value: Dict) -> None:
        """Set longitude uncertainty"""
        self['lon_uncer'] = CoordinateUncertainty(**value)

    @property
    def depth(self) -> Depth:
        """Get depth"""
        return self.get('depth', Depth())

    @depth.setter
    def depth(self, value: Dict) -> None:
        """Set depth"""
        self['depth'] = Depth(**value)

    @property
    def depth_uncertainty(self) -> DepthUncertainty:
        """Get depth uncertainty"""
        return self.get('depth_uncer', DepthUncertainty())

    @depth_uncertainty.setter
    def depth_uncertainty(self, value: Dict) -> None:
        """Set depth uncertainty"""
        self['depth_uncer'] = DepthUncertainty(**value)

    @property
    def origintime(self) -> OriginTime:
        """Get origin time"""
        return self.get('orig_time', OriginTime())

    @origintime.setter
    def origintime(self, value: Dict) -> None:
        """Set origin time"""
        self['orig_time'] = OriginTime(**value)

    @property
    def origintime_uncertainty(self) -> OriginTimeUncertainty:
        """Get origin time uncertainty"""
        return self.get('orig_time_uncer', OriginTimeUncertainty())

    @origintime_uncertainty.setter
    def origintime_uncertainty(self, value: Dict) -> None:
        """Set origin time uncertainty"""
        self['orig_time_uncer'] = OriginTimeUncertainty(**value)

    @property
    def likelihood(self) -> float:
        """Get likelihood"""
        return self.get('likelihood', 0.0)

    @likelihood.setter
    def likelihood(self, value: SupportsFloat) -> None:
        """Set likelihood"""
        self['likelihood'] = float(value)

    @property
    def stations(self) -> int:
        """Get number of stations"""
        value = self.get('num_stations', 0)
        # optional field so force convert if requested
        return int(value) if not isinstance(value, int) else value

    @stations.setter
    def stations(self, value: SupportsInt) -> None:
        """Set number of stations"""
        self['num_stations'] = int(value)
