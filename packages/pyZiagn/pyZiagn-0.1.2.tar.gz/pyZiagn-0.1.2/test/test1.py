import pyZiagn
print("Test of package")
Test1 = pyZiagn.uniaxialTensileTest()
Test1.Title = "Test1"
Test1.loadExample()
Test1.changeUnits()
Test1.plotForceDisp()