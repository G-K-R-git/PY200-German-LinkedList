from typing import Sequence, Optional
from abc import ABC, abstractmethod
import pickle
import json
import os
from linked_list import DoubleLinkedList


class IStructureDriver(ABC):
    @abstractmethod
    def read(self) -> Sequence:
        """
        Считывает информацию из драйвера и возвращает её для объекта, использующего этот драйвер
        :return Последовательность элементов, считанная драйвером, для объекта
        """
        pass

    @abstractmethod
    def write(self, data: Sequence) -> None:
        """
        Получает информацию из объекта, использующего этот драйвер, и записывает её в драйвер
        :param data Последовательность элементов, полученная от объекта, для записи драйвером
        """
        pass


class JsonFileDriver(IStructureDriver):
    def __init__(self, filename):
        self._filename = filename

    def read(self) -> Sequence:
        with open(self._filename) as file:
            return json.load(file)

    def write(self, data: Sequence) -> None:
        with open(self._filename, "w") as file:
            json.dump(data, file)


class PickleFileDriver(IStructureDriver):
    def __init__(self, filename):
        self._filename = filename

    def read(self) -> Sequence:
        with open(self._filename, "rb") as file:
            return pickle.load(file)

    def write(self, data: Sequence) -> None:
        with open(self._filename, "wb") as file:
            pickle.dump(data, file)


class DoubleLinkedListWithDriver(DoubleLinkedList):
    def __init__(self, driver: Optional[IStructureDriver] = None):
        super().__init__()
        self._driver = driver

    @property
    def driver(self):
        if self._driver is None:
            self._driver = DriverFabric.get_driver()
        return self._driver

    @driver.setter
    def driver(self, new_driver: IStructureDriver):
        if not isinstance(new_driver, IStructureDriver):
            raise TypeError
        else:
            self._driver = new_driver
    
    def read(self):
        self.clear()
        for item in self.driver.read():
            self.append(item)

    def write(self):
        data_as_list = [item for item in self]
        self.driver.write(data_as_list)


class DriverBuilder(ABC):
    @abstractmethod
    def build(self):
        ...


class JsonFileBuilder(DriverBuilder):
    DEFAULT_NAME = 'untitled.json'

    @classmethod
    def build(cls) -> IStructureDriver:
        filename = input('Введите название json файла: (.json)').strip()
        filename = filename or cls.DEFAULT_NAME
        if not filename.endswith('.json'):
            filename = f'{filename}.json'

        return JsonFileDriver(filename)


class PickleFileBuilder(DriverBuilder):
    DEFAULT_NAME = 'untitled.bin'

    @classmethod
    def build(cls) -> IStructureDriver:
        filename = input('Введите название для файла: (.bin): ').strip()
        filename = filename or cls.DEFAULT_NAME
        if not filename.endswith('.bin'):
            filename = f'{filename}.bin'

        return PickleFileDriver(filename)


class DriverFabric:
    DRIVER_BUILDER = {
        'json': JsonFileBuilder,
        'pickle': PickleFileBuilder
    }
    DEFAULT_DRIVER = 'json_file'

    @classmethod
    def get_driver(cls):
        driver_name = input("Введите название драйвера: ")
        driver_name = driver_name or cls.DEFAULT_DRIVER

        driver_builder = cls.DRIVER_BUILDER[driver_name]
        return driver_builder.build()


def main():
    directory_path = os.path.dirname(__file__)  # Подразумевается, что фал будет лежать в каталоге проекта
    filename_json = os.path.join(directory_path, "TestFile.json")
    filename_pickle = os.path.join(directory_path, "TestFile.bin")

    driver: IStructureDriver = JsonFileDriver(filename_json)
    data = [1, 1, 1]

    driver.write(data)
    print(driver.read())

    driver2: IStructureDriver = PickleFileDriver(filename_pickle)

    driver2.write(data)
    print(driver2.read())

    dll = DoubleLinkedListWithDriver()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    dll.append(4)
    print(dll)
    dll.write()
    print(dll)
    dll.read()
    print(dll)


if __name__ == '__main__':
    main()
