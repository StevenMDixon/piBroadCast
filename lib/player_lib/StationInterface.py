from abc import ABC, abstractmethod

class IStation(ABC):
        @abstractmethod
        def data_changed(self) -> bool:
            pass

        @abstractmethod
        def set_station_config(self, arg1) -> None:
            pass

        @abstractmethod
        def setup_playlist_data(self) -> None:
             pass