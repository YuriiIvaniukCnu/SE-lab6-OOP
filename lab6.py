from abc import ABC, abstractmethod

ESV = 1760


class Employee(ABC):
    def __init__(self, code, surname):
        self.code = code
        self.surname = surname

    @abstractmethod
    def salary(self):
        pass

    @abstractmethod
    def tax(self):
        pass


class HourlyEmployee(Employee):
    def __init__(self, code, surname, rate):
        super().__init__(code, surname)
        self.rate = rate

    def salary(self):
        return 20.8 * 8 * self.rate

    def tax(self):
        return self.salary() * (0.18 + 0.015)


class FixedEmployee(Employee):
    def __init__(self, code, surname, monthly):
        super().__init__(code, surname)
        self.monthly = monthly

    def salary(self):
        return self.monthly

    def tax(self):
        return self.salary() * (0.18 + 0.015)


class FOPEmployee(HourlyEmployee):
    def __init__(self, code, surname, rate, group):
        super().__init__(code, surname, rate)
        self.group = group

    def salary(self):
        return super().salary() * 1.1

    def tax(self):
        return self.salary() * 0.05 + ESV


class SelfEmployed(Employee):
    def __init__(self, code, surname, line_price, lines):
        super().__init__(code, surname)
        self.line_price = line_price
        self.lines = lines

    def salary(self):
        return self.line_price * self.lines

    def tax(self):
        return self.salary() * (0.18 + 0.015) + ESV
