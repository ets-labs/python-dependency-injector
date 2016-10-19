"""Dependency injection example, Cars & Engines."""

import example.cars
import example.engines


if __name__ == '__main__':
    gasoline_car = example.cars.Car(example.engines.GasolineEngine())
    diesel_car = example.cars.Car(example.engines.DieselEngine())
    electro_car = example.cars.Car(example.engines.ElectroEngine())
