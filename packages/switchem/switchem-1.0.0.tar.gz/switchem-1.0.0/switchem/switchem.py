import onetrick

@onetrick
class switch(Exception):
    __value:object
    __fall = False

    def __init__(self, value:object):
        self.__value = value

    def __enter__(self):
        return self
    
    def __exit__(self, _, exc, __):
        if exc is self:
            return True
        
        return False

    def __call__(self, value, *values) -> bool:
        if self.__fall:
            return True
        
        if (self.__value == value) or (self.__value in values):
            self.__fall = True
            return True
        
        return False

if __name__ == "__main__":
    MONKEY = 1
    ELEPHANT = 2
    GIRAFFE = 3
    HORSE = 4
    SQUIRREL = 5
    SQUID = 6
    COW = 7
    SARCASTIC_FRINGEHEAD = 8

    with switch(HORSE) as case:
        if case(MONKEY):
            print("It is a monkey")
            raise case
        
        if case(ELEPHANT, GIRAFFE, HORSE):
            print("It is not a monkey for sure")
        
        if case(SQUIRREL):
            print("It could be a squirrel")
            raise case
        
        print("It is definitely not a monkey, elephant, giraffe, horse, or squirrel")