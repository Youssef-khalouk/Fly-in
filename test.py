
def power_validator(min_power: int) -> callable:
    pass

def decorator(min_power) -> callable:

    def wrapper():
        func()

    return wrapper


@decorator
def funnction():
    print("hello")


    dicorator = @power_validator(10)
    @dicorator
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"