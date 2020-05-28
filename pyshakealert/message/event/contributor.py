"""
..  codeauthor:: Charles Blais
"""
from typing import SupportsInt


class Contributor(dict):
    """Event message contributor element"""
    def __init__(self, *args, **kwargs):
        super(Contributor, self).__init__(*args, **kwargs)
        # Create the default required objects
        # attributes
        self.algorithm_name = self.algorithm_name
        self.algorithm_version = self.algorithm_version
        self.algorithm_instance = self.algorithm_instance
        self.category = self.category
        self.event_id = self.event_id
        self.version = self.version

    @property
    def algorithm_name(self) -> str:
        """Get algorithm name"""
        return self.get('@alg_name', '-')

    @algorithm_name.setter
    def algorithm_name(self, value: str) -> None:
        """Set algorithm name"""
        self['@alg_name'] = value

    @property
    def algorithm_version(self) -> str:
        """Get algorithm version"""
        return self.get('@alg_version', '-')

    @algorithm_version.setter
    def algorithm_version(self, value: str) -> None:
        """Set algorithm version"""
        self['@alg_version'] = value

    @property
    def algorithm_instance(self) -> str:
        """Get algorithm instance"""
        return self.get('@alg_instance', '-')

    @algorithm_instance.setter
    def algorithm_instance(self, value: str) -> None:
        """Set algorithm instance"""
        self['@alg_instance'] = value

    @property
    def category(self) -> str:
        """Get category"""
        return self.get('@category', '-')

    @category.setter
    def category(self, value: str) -> None:
        """Set category"""
        self['@category'] = value

    @property
    def event_id(self) -> str:
        """Get event id"""
        return self.get('@event_id', '-')

    @event_id.setter
    def event_id(self, value: str) -> None:
        """Set event id"""
        self['@event_id'] = value

    @property
    def version(self) -> int:
        """Get version"""
        return self.get('@version', 0)

    @version.setter
    def version(self, value: SupportsInt) -> None:
        """Set version"""
        self['@version'] = int(value)


class Contributors(list):
    """Event message contributors"""
    def __init__(self, *args, **kwargs):
        # Convert all args to contributor object
        contribs = [Contributor(**arg) for arg in args]
        if not contribs:
            contribs = [Contributor()]
        super(Contributors, self).__init__(contribs, **kwargs)
