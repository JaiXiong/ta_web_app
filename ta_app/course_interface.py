import abc


class ICourse(abc.ABC):

    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def name(self, n: str):
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
    def instructor(self) -> str:
        pass

    @abc.abstractmethod
    def instructor(self, i: str):
        pass

    @abc.abstractmethod
    def tas(self) -> [str]:
        pass

    @abc.abstractmethod
    def tas(self, ts: [str]):
        pass

    @abc.abstractmethod
    def lab(self) -> str:
        pass

    @abc.abstractmethod
    def lab(self, l: str):
        pass

    @abc.abstractmethod
    def lab_sections(self) -> [str]:
        pass

    @abc.abstractmethod
    def lab_sections(self, ls: [str]):
        pass

