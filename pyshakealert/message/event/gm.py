"""
..  codeauthor:: Charles Blais
"""
from typing import Union, List, Dict

from pyshakealert.message.event.gmcontour import GroundMotionContours
from pyshakealert.message.event.gmmap import GroundMotionMap


class GroundMotion(dict):
    """Event message gm_info element"""
    @property
    def contours(self) -> GroundMotionContours:
        """Get contour

        Contours are found in the "contour" index of gemcontour_pred section.

        In order to keep xmltodict structure, we extract information and save
        information in the same format.
        """
        value = self.get('gmcontour_pred', {}).get(
            "contour", GroundMotionContours())
        # if there is only one contour, it won't be list
        if not isinstance(value, list):
            value = [value]
        # optional field so force convert if requested
        return GroundMotionContours(*value) \
            if not isinstance(value, GroundMotionContours) \
            else value

    @contours.setter
    def contours(self, value: Union[Dict, List[Dict]]) -> None:
        """Set contour"""
        conv = [value] if isinstance(value, dict) else value
        # Create the gmcontour_pred dictionary if it does not exist
        self.setdefault('gmcontour_pred', {})
        self['gmcontour_pred']['contour'] = GroundMotionContours(*conv)
        # update the update attribute found in the xml document
        self['gmcontour_pred']["@number"] = len(conv)

    @property
    def map(self) -> GroundMotionMap:
        """Get map"""
        value = self.get('gmmap_pred', GroundMotionMap())
        # optional field so force convert if requested
        return GroundMotionMap(**value) \
            if not isinstance(value, GroundMotionMap) \
            else value

    @map.setter
    def map(self, value: GroundMotionMap) -> None:
        """Set map"""
        self['gmmap_pred'] = GroundMotionMap(**value)
