import pyZiagn
import matplotlib.pyplot as plt

TestData = "1-5.txt"
Area0 = 21.35
length0 = 33
dispCutOff = 1.75
TestName = TestData
Test4 = pyZiagn.uniaxialTensileTest(length0, Area0=Area0, Title=TestName[:-4])
Test4.importTestData("data/"+TestData)
Test4.changeUnits()
Test4.cutData("disp", dispCutOff)
Test4.smoothForce()
Test4.calcStressEng()
Test4.calcStrainEng()
Test4.calcStressTrue()
Test4.calcStrainTrue()
Test4.calcStressUltimate()
Test4.calcLength()
Test4.calcArea()
Test4.calcElasticModulus(strain0=0.0001, strain1=0.0005)
Test4.calcRP02()
Test4.calcLinearLimit()
Test4.zeroStrain()
Test4.calcToughnessModulus()
Test4.approxRambergOsgood()
Test4.approxHockettSherby()
Test4.approxGhosh()
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 5))
plt.plot(Test4.strainTrue, Test4.stressTrue, label="True stress-strain")
plt.plot(Test4.strainEng, Test4.stressEng, label="Engineering stress-strain")
plt.plot(Test4.strainRambergOsgood, Test4.stressRambergOsgood,
         label="Ramsberg-Osgood")
plt.plot(Test4.strainHockettSherby+Test4.strainTrueLinLimit,
         Test4.stressHockettSherby, label="Hockett-Sherby")
plt.plot(Test4.strainGhosh+Test4.strainTrueLinLimit,
         Test4.stressGhosh, label="Ghosh")
plt.plot(Test4.strainTrueLinLimit, Test4.stressTrueLinLimit, 'o',
         label='Linear limit in true stress and strain')
plt.plot(Test4.strainRP02, Test4.stressRP02, 'o', label="$R_{P0.2}$")
plt.legend()
plt.show()
