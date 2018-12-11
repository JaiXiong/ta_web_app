import abc


class ILab:

    @abc.abstractmethod
    def course(self) -> str:
        pass

    @abc.abstractmethod
    def course(self, n: str):
        pass

    @abc.abstractmethod
    def section(self) -> str:
        pass

    @abc.abstractmethod
    def section(self, s: str):
        pass

    @abc.abstractmethod
    def days_of_week(self) -> [str]:
        pass

    @abc.abstractmethod
    def days_of_week(self, d: [str]):
        pass

    @abc.abstractmethod
    def start_time(self) -> str:
        pass

    @abc.abstractmethod
    def start_time(self, s: str):
        pass

    @abc.abstractmethod
    def end_time(self) -> str:
        pass

    @abc.abstractmethod
    def end_time(self, e: str):
        pass

    @abc.abstractmethod
    def ta(self) -> str:
        pass

    @abc.abstractmethod
    def ta(self, ts: str):
        pass
