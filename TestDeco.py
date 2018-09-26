import DecoDebug as dd
import inspect

class TestDeco():

    @dd.Debug(1)
    def testFunc(self, thing):
        print("My level is 1!")
    @dd.Debug(3)
    def testFunc2(self, thing):
        print("My level is 3")
        return thing

@dd.Debug(2)
def test1(more):
    print("My level is 2")

@dd.Debug(4)
def test2(more, fizz="bang"):
    print("My level is 4")
    printName()
    return more

@dd.Debug()
def printName():
    print(inspect.stack()[1])

@dd.DecoDebugMain
def execute():
    test = TestDeco()
    test.testFunc("stuff")
    test2("merp")
    test.testFunc2("Jon")
    test1("Me")
    test.testFunc("again")
    test1("me again!")
    test2("huh", fizz="pop")
    printName()

if __name__ == "__main__":
    execute()
