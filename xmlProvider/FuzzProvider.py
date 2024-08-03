# -*- coding: utf-8 -*-
TroubleMaker=True
Wh1tcTest= False
BaseMode = False
# False

#TroubleMaker=False
interestingIntegers=[                 
    -4096, -1024, -256, -128, -1, 0,-0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 64,
    127, 128, 129,                             
    255, 256, 257,                          
    512, 1000, 1024, 4096]
#interestingFloats = [-1e-15, -1e12, -1e9, -1e6, -1e3, -5.0, -4.0, -3.0, -2.0, -1.0 -0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 1e3, 1e6, 1e9, 1e12, 1e-15]
interestingFloats = [7.549789E-08,-5.0962E-06,-4.071E-05,-5.0, -4.0, -3.0, -2.0, -1.0,-0.3,-0.5, -0.0, 0.0,0.3, 0.5,1.0, 2.0, 3.0, 4.0, 5.0]
import random


def genInt():
    if(BaseMode):
        return str(random.randint(20,100))
    percent=random.randint(0,199)

    if(percent<194):
        fuzzint=str(random.randint(20,200))
    elif(percent<199):
        index_int=random.randint(0,len(interestingIntegers)-1)
        fuzzint=str(interestingIntegers[index_int])
    else:
        index_float=random.randint(0,len(interestingFloats)-1)
        fuzzint=str(interestingFloats[index_float])
    return fuzzint



def genpairInt():
    return genInt()+","+genInt()

def gensomepairInt(nums):
    temp = ""
    for i in range(nums):
        temp+=genInt()+","+genInt()+" "
    return temp

def genoneInt():
    return genInt()


def getpercent(givenint):
    return givenint>random.randint(0,99)


def genfourint():
    return genInt()+","+genInt()+","+genInt()+","+genInt()



#interestingString=["これは、縦書きの日本語テキスト が","Copyright &#xa9; 2006 QualityLogic, Inc.","中文测试","A"*4096]

interestingString=[u"これは、縦書きの日本語テキスト が","Copyright &#xa9; 2006 QualityLogic, Inc.",u"中文测试"]

def genonestring():
    return interestingString[random.randint(0,len(interestingString)-1)]



#color:
def randomcolor(num):
    colorArr = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(num):
        color += colorArr[random.randint(0,15)]
    return "#"+color

def randomfloat():
    return str(random.random())

def getfloat10():
    return str(random.uniform(0,10))

def getint10():
    return str(random.randint(0,10))

def getfloatorint():
    if(getpercent(50)):
        return getfloat10()
    else:
        return getint10()

def getcolorfloat():
    if(getpercent(90)):
        return randomfloat()
    else:
        return str(random.randint(0,1))


def gencolor():
    case = random.randint(0,5)
    if(case==0):#sRGB w/o alpha
        return (randomcolor(6))
    if(case==1):#sRGB with alpha
        return (randomcolor(6))
    if(case==2):#scRGB w/o alpha
        code="sc#"
        for i in range(3-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)
    if(case==3):#scRGB with alpha
        code="sc#"
        for i in range(4-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)
    if(case==4): #CMYK
        code="ContextColor /Resources/"+cmykcolor[random.randint(0,len(cmykcolor)-1)]+" "
        for i in range(5-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)
    if(case==5): #RGB
        code="ContextColor /Resources/RGBprofile.icc "
        for i in range(4-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)

cmykcolor=["SWOP2006_Coated3v2.icc","JapanColor2011Coated.icc","swopcmykprofile.icc"]
InterestingDash=["Flat","Round","Square","Triangle"]
InterestingLineJoin=["Miter","Bevel","Round"]

def genDash():
    return (InterestingDash[random.randint(0,len(InterestingDash)-1)])

def genLineJoin():
    return (InterestingLineJoin[random.randint(0,len(InterestingLineJoin)-1)])

def genTileMode():
    TileMode=["None", "Tile", "FlipX", "FlipY", "FlipXY"]
    return TileMode[random.randint(0,len(TileMode)-1)]

def genTag_percent():
    case = random.randint(0,100)
    if(case<3):# 0 1 2
        return 0
    elif (case<99):
        return 1
    else: #99 100
        return random.randint(2,5)

def genAttrNum_percent():
    case = random.randint(0,100)
    if(case<3):# 0 1 2
        return 0
    elif (case<99):
        return 1
    else: #99 100
        return random.randint(2,5)

def genAttrValue_percent():
    if(getpercent(99)):
        return 1
    else:
        return 0

def genOutputpercent():
    if(getpercent(99)):
        return 1
    else:
        return 0

def genspecial():
    return ""

def genWidthandHeight():
    if(getpercent(98)):
        return str(random.randint(500,2000))
    else:
        return genInt()

def genContentInt1():
    if(getpercent(98)):
        fuzzint=str(random.randint(0,20))
    else:
        fuzzint=genInt()
    return fuzzint

def genContentInt2():
    if(getpercent(98)):
        fuzzint=str(random.randint(0,500))
    else:
        fuzzint=genInt()
    return fuzzint

def genBleedInt1():
    if(getpercent(98)):
        fuzzint=str(random.randint(-20,0))
    else:
        fuzzint=genInt()
    return fuzzint

def genBleedInt2():
    if(getpercent(98)):
        fuzzint=str(random.randint(2000,2500))
    else:
        fuzzint=genInt()
    return fuzzint

def genContent():
    return genContentInt1()+","+genContentInt1()+","+genContentInt2()+","+genContentInt2()

def genBleed():
    return genBleedInt1()+","+genBleedInt1()+","+genBleedInt2()+","+genBleedInt2()

def ZeroOrOne():
    if(getpercent(50)):
        return str(0)
    else:
        return str(1)

def genAbbreviatedData():
    code = " "
    if(getpercent(20)):
        code+=" F "+ZeroOrOne()
    if(getpercent(90)):
        code+=" M "+genInt()+","+genInt()

    for i in range(random.randint(0,20)):
        case  = random.randint(0,8)
        if(case==0):
            if(getpercent(1)):
                code+=" F "+ZeroOrOne()
        if(case==1):
            if(getpercent(50)):
                code+=" L "+genInt()+","+genInt()
            else:
                code+=" l "+genInt()+","+genInt()
        if(case==2):
            if(getpercent(50)):
                code+=" H "+genInt()
            else:
                code+=" h "+genInt()
        if(case==3):
            if(getpercent(50)):
                code+=" V "+genInt()
            else:
                code+=" v "+genInt()
        if(case==4):
            if(getpercent(50)):
                code+=" C "+genInt()+","+genInt()+" "+genInt()+","+genInt()+" "+genInt()+","+genInt()
            else:
                code+=" c "+genInt()+","+genInt()+" "+genInt()+","+genInt()+" "+genInt()+","+genInt()
        if(case==5):
            if(getpercent(50)):
                code+=" Q "+genInt()+","+genInt()+" "+genInt()+","+genInt()
            else:
                code+=" q "+genInt()+","+genInt()+" "+genInt()+","+genInt()
        if(case==6):
            if(getpercent(50)):
                code+=" S "+genInt()+","+genInt()+" "+genInt()+","+genInt()
            else:
                code+=" s "+genInt()+","+genInt()+" "+genInt()+","+genInt()
        if(case==7):
            if(getpercent(50)):
                code+=" A "+genInt()+","+genInt()+" "+genInt()+" "+ZeroOrOne()+" "+ZeroOrOne()+" "+genInt()+","+genInt()+""
            else:
                code+=" a "+genInt()+","+genInt()+" "+genInt()+" "+ZeroOrOne()+" "+ZeroOrOne()+" "+genInt()+","+genInt()+""
        if(case==8):
            if(getpercent(1)):
                if(getpercent(50)):
                    code+=" M "+genInt()+","+genInt()
                else:
                    code+=" m "+genInt()+","+genInt()
        
    if(getpercent(50)):
        code+=" Z "
    else:
        code+=" z "
    return code


def genRenderTransform():
    return genInt()+","+genInt()+","+genInt()+","+genInt()+","+genInt()+","+genInt()


def genOpacity():
    if(getpercent(95)):
        return (str(round(random.random(),2)))
    else:
        return genInt()

def gencolor():
    case = random.randint(0,5)
    if(case==0):#sRGB w/o alpha
        return (randomcolor(6))
    if(case==1):#sRGB with alpha
        return (randomcolor(6))
    if(case==2):#scRGB w/o alpha
        code="sc#"
        for i in range(3-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)
    if(case==3):#scRGB with alpha
        code="sc#"
        for i in range(4-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)
    if(case==4): #CMYK
        code="ContextColor /Resources/"+cmykcolor[random.randint(0,len(cmykcolor)-1)]+" "
        for i in range(5-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)
    if(case==5): #RGB
        code="ContextColor /Resources/RGBprofile.icc "
        for i in range(4-1):
            code+=getcolorfloat()
            code+=","
        code+=getcolorfloat()
        return (code)

def genST_EdgeMode():
    return "Aliased" 

def genUri():
    return "/Resources/resources.dict"

def genMatrix():
    return genInt()+","+genInt()+","+genInt()+","+genInt()+","+genInt()+","+genInt()

def genFillRule():
    temp_list=["EvenOdd","NonZero"]
    return temp_list[random.randint(0,len(temp_list)-1)]

def genST_CaretStops():
    if(getpercent(98)):
        return randomcolor(4)[1:]
    else:
        return randomcolor(random.randint(1,200))[1:]

def genBoolean():
    temp_list=["true","false"]
    return temp_list[random.randint(0,len(temp_list)-1)]

def genPointM():
        if(getpercent(98)):
            return gensomepairInt(random.randint(2,10))
        else:
            return gensomepairInt(random.randint(0,100))

def genST_EvenArrayPos():
    if getpercent(98):
        return getfloatorint()+" "+getfloatorint()
    else:
        for i in range(1,100):
            return getfloatorint()+" "
    
def genDouble():
    if(getpercent(60)):
        return str(round(random.uniform(1, 100),2))
    else:
        return genInt()

def genViewBox():
    return genfourint()

def genST_ViewUnits():
    return "Absolute"

FontUri=["msgothic.ttf","mshei.ttf","gulimche.ttf","courier.ttf","times.ttf","arial.ttf"]

def genST_UriFont():
    return "/Resources/"+FontUri[random.randint(0,len(FontUri)-1)]
ImageSource=["QL_logo_color.tif","img103.png","mammoth.jpg","not_kitty.jxr",
"logluv-3c-16b.tif","minisblack-1c-8b.tif","minisblack-1c-16b.tif","minisblack-2c-8b-alpha.tif","miniswhite-1c-1b.tif",
"palette-1c-1b.tif","palette-1c-4b.tif","palette-1c-8b.tif","quad-tile.tif","rgb-3c-8b.tif","rgb-3c-16b.tif"]
def genImageSource():
    return "/Resources/"+ImageSource[random.randint(0,len(ImageSource)-1)]


def genST_ClrIntMode():
    temp_list=["ScRgbLinearInterpolation","SRgbLinearInterpolation"]
    return temp_list[random.randint(0,len(temp_list)-1)]

def genST_SpreadMethod():
    temp_list=["Pad","Reflect","Repeat"]
    return temp_list[random.randint(0,len(temp_list)-1)]

def genST_StyleSimulations():
    temp_list=["ItalicSimulation","BoldSimulation","BoldItalicSimulation","None"]
    return temp_list[random.randint(0,len(temp_list)-1)]

def genST_SweepDirection():
    temp_list=["Clockwise","Counterclockwise"]
    return temp_list[random.randint(0,len(temp_list)-1)]

colorArr = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
def genUnicode():
    if(getpercent(60)):
        return genonestring()

    nums = 4
    if(getpercent(20)): 
        nums = random.randint(1,100)
    if(BaseMode):
        nums = 4
    unicode = ""
    
    for i in range(nums):
        unicode += "&#x"
        for j in range(3):
            unicode += colorArr[random.randint(0,15)]
        unicode += ";"
    return unicode
    

def randomManytoMany():
    return "("+genInt()+":"+genInt()+")"

Indices=["(2:3)94;76;88;(2:1)162", "153;106,,,16;(1:2)124;198;4","94;76;88;162"]

ManytoMany=["(1:2)","(1:2)","(1:2)","(1:2)","(1:2)","(1:3)","(1:4)","(2:1)","(2:1)","(2:1)","(2:1)","(2:1)","(3:1)","(4:1)"]

def genIndices():

    nums = 4
    if(getpercent(20)): 
        nums = random.randint(1,100)
    if(BaseMode):
        nums = 4

    if(BaseMode):
        return Indices[random.randint(0,len(Indices)-1)]


    if(getpercent(50)):
        return Indices[random.randint(0,len(Indices)-1)]
    else:
        indice=""
        for i in range(nums):
            if(getpercent(20)):
                if(getpercent(10)): #2%
                    indice += randomManytoMany()
                else:                #18%
                    indice += ManytoMany[random.randint(0,len(ManytoMany)-1)]
            indice+=genInt()
            if(i!=nums-1):
                indice+=";"
        return indice