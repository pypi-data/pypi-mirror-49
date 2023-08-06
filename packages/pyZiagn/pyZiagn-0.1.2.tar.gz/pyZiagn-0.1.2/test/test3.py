import pyZiagn

# 1: 0°, 2: 45°, 3: 90°
TestList = ["1-1.txt", "1-2.txt", "1-3.txt", "1-4.txt", "1-5.txt",
            "2-1.txt", "2-2.txt", "2-3.txt", "2-4.txt", "2-5.txt",
            "3-1.txt", "3-2.txt", "3-3.txt", "3-4.txt", "3-5.txt"]
Area0 = [26, 21.35, 21.35, 21.35, 20.79, 21.35,
         22.4475, 22.32, 23.18, 21.96, 21.35,
         22.57, 25.2, 24.57, 21.96, 22.32]
length0 = [33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]
dispCutOff = [2.15, 1.38, 1.38, 2.0, 1.75,
              1.95, 1.83, 1.97, 2.1, 2.07,
              3.8, 1.22, 1.95, 1.2, 1.55]
OnlyGood = False
if OnlyGood:
    NotAll = [     1,      3,  4,
                   6,           ]
    TestList = [TestList[i] for i in NotAll]
    Area0 = [Area0[i] for i in NotAll]
    length0 = [length0[i] for i in NotAll]
    dispCutOff = [dispCutOff[i] for i in NotAll]
TestName = TestList
Test = [[]]*len(TestList)
for i in range(len(TestList)):
    Test[i] = pyZiagn.uniaxialTensileTest(length0=length0[i], Area0=Area0[i],
                                          Title=TestName[i][:-4])
    Test[i].importTestData("data/"+TestList[i])
    Test[i].changeUnits()
    #Test[i].plotForceDisp()
    Test[i].cutData("disp", dispCutOff[i])
    Test[i].smoothForce()
    #Test[i].plotForceDispSmoothRaw()
    Test[i].calcStressEng()
    Test[i].calcStrainEng()
    Test[i].calcStressTrue()
    Test[i].calcStrainTrue()
    Test[i].calcStressUltimate()
    Test[i].calcArea()
    Test[i].calcElasticModulus(strain0=0.0001, strain1=0.0005)
    Test[i].calcRp02()
    Test[i].calcLinearLimit()
    Test[i].zeroStrain()
    Test[i].plotStressStrainEngAll()
pyZiagn.export2Excel(Test)
pyZiagn.plotMulti(Test, strainMax=0.08)