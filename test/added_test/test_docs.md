## Content

* <a href='#Donate_Blood'>1. Donate_Blood</a>
* <a href='#Catastrophic_Delete'>2. Catastrophic_Delete</a>
* <a href='#Period_Change_1'>3. Period_Change_1</a>
* <a href='#Period_change_2'>4. Period_change_2</a>
* <a href='#Worst_DRed'>5. Worst_DRed</a>

<span id='Donate_Blood'/>

#### 1. Donate_Blood

    data = [
        "Donated(a)@-365",
        "Vaccinated(a)@-20",
        "Ill(a)@[-10,-5]",

        "Vaccinated(b)@-250",
        "Vaccinated(b)@-170",
        "Vaccinated(b)@-130",
        "Vaccinated(b)@-90",
        "Vaccinated(b)@-55",
        "Vaccinated(b)@-20",
        "Ill(b)@[-200,-180]",
        "Ill(b)@[-130,-105]",
        "Ill(b)@[-80,-60]",
        "Ill(b)@[-30,-5]",
    ]
    program = [
               "NoDonate(X):-SOMETIME[-182,0]Donated(X)",
                "NoDonate(X):-SOMETIME[-30,0]Vaccinated(X)",
                "NoDonate(X):-Ill(X)@0",
    ]
    fact = "NoDonate(a)@0"
可以对b添加任意条件以增加运算量，不影响最终结果

<span id='Catastrophic_Delete'/>

#### 2. Catastrophic_Delete

    data = [
        "A(x)@0",
        "B(x)@0",
        "C(x)@0"
    ]
    program = [
        "D(X):-ALWAYS[-1,-1] A(X)",
        "D(X):-ALWAYS[-1,-1] B(X)",
        "E(X):-ALWAYS[-1,-1] B(X)",
        "E(X):-ALWAYS[-1,-1] C(X)",
    
        "A(X):-ALWAYS[-1,-1] D(X)",
        "B(X):-ALWAYS[-1,-1] D(X)",
        "B(X):-ALWAYS[-1,-1] E(X)",
        "C(X):-ALWAYS[-1,-1] E(X)",
    ]
    fact = "A(x)@4"
示意图：

![img_1.png](img_1.png)
去除data中的"B(x)@0"，不会影响执行结果，但是Dred会删除Time>=1的所有fact，然后再重新推出fact。

<span id='Period_Change_1'/>

#### 3. Period_Change_1

    data = [
        "Step_five(a)@[0,1]",
        "Step_seven(a)@[0,1]",
    ]
    program = ["ALWAYS[0,1] Step_five(X):- ALWAYS[-5,-4] Step_five(X)",
                "ALWAYS[0,1] Step_seven(X):- ALWAYS[-7,-6] Step_seven(X)"
    ]
    fact = "Step_five(a)@35"
去除Step_seven(a)@[0,1]可使周期长度由35改变到5；

<span id='Period_Change_2'/>

#### 4. Period_Change_2

    data = [
        "Step_three(a)@0",
        "Step_three(a)@1",
        "Step_three(a)@2",
    ]
    program = ["Step_three(X):- ALWAYS[-3,-3]Step_three(X)"]
    fact = "Step_five(a)@5"
去除Step_three(a)@2可使周期长度由1改变到3；

<span id='Worst_DRed'/>

#### 5. Worst_DRed

    data = [
        "Step_five(a)@0",#A
        "Step_oneA(a)@0",#B
        #"Step_fifty(b)@0"
    ]
    program = ["Step_five(X):- ALWAYS[-5,-5]Step_five(X)",
               "Step_oneB(X):- ALWAYS[-1,-1]Step_oneA(X)",
               "Step_oneC(X):- ALWAYS[-1,-1]Step_oneB(X)",
               "Step_oneD(X):- ALWAYS[-1,-1]Step_oneC(X)",
               "Step_oneE(X):- ALWAYS[-1,-1]Step_oneD(X)",
               "Step_one(X):- ALWAYS[-1,-1]Step_oneE(X)",
               #"Step_fifty(X):- ALWAYS[-50,-50]Step_fifty(X)"
    ]
    fact = "Step_five(a)@25"

示意图：

![img.png](img.png)

在单个周期内，若给出A、B两个数据，则可在5步内推出所有事实；但去掉事实A后，首先要花费5步回溯，再花费4步重新推出事实；对结果无影响。

data和program中关于Step_fifty的代码本意为设置周期长度足够大，但加入会导致程序不终止（挠头




