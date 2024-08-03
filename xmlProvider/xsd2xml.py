#!/usr/bin/python3
import re
from argparse import ArgumentParser
import configparser
import xmlschema
from xmlschema.validators import (
    XsdElement,
    XsdAnyElement,
    XsdComplexType,
    XsdAtomicBuiltin,
    XsdSimpleType,
    XsdList,
    XsdUnion,
    XsdGroup,
)
from FuzzProvider import *
import random
# default tag value
UKN_VALUE = 'UNKNOWN'

f = open("1.fpage", "wb")
def mywrite(str1):
    f.write(str1.encode('utf-8'))
    f.write("\n".encode('utf-8'))
    
DEFAULT_SCHEMAS = {
    'xml:lang':"en-US",
    '':"http://schemas.microsoft.com/xps/2005/06"
 #   '': 'http://www.iata.org/IATA/2015/00/2020.2/{0}',
 #   'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
 #   'xsi:schemaLocation': "http://www.iata.org/IATA/2015/00/2020.2/{0} ../{0}.xsd"
}

# sample data is hardcoded
def valsmap(v):
    v['ST_Width'] = genWidthandHeight
    v['ST_GEOne'] = genInt
    v['ST_Name'] = genonestring
    v['ST_BleedBox'] = genBleed
    v['ST_ContentBox'] = genContent
    v['ST_RscRefAbbrGeomF'] = genAbbreviatedData
    v['ST_RscRefMatrix'] = genRenderTransform
    v['ST_ZeroOne'] = genOpacity
    v['ST_RscRefColor'] = gencolor
    v['ST_Color'] = gencolor
    v['ST_RscRef'] = genspecial
    v['ST_EdgeMode'] = genST_EdgeMode
    v['anyURI'] = genUri
    v['string'] = genonestring
    v['ST_AbbrGeom'] = genAbbreviatedData
    v['ST_Matrix'] = genMatrix
    v['ST_FillRule'] = genFillRule
    v['ST_CaretStops'] = genST_CaretStops
    v['ST_Boolean'] = genBoolean
    v['ST_Point'] = genpairInt
    v['ST_PointGE0'] = genpairInt
    v['ST_Points'] = genPointM
    v['ST_PointsM2'] = genPointM
    v['ST_PointsM3'] = genPointM
    v['ST_UnicodeString'] = genonestring
    v['ST_GEZero'] = genInt
    v['ST_EvenArrayPos'] = genST_EvenArrayPos
    v['ST_Double'] = genDouble
    v['ST_ViewBox'] = genViewBox
    v['ST_TileMode'] = genTileMode
    v['ST_ViewUnits'] = genST_ViewUnits
    v['ST_UriCtxBmp'] = genImageSource
    v['ST_DashCap'] = genDash
    v['ST_LineCap'] = genDash
    v['ST_LineJoin'] = genLineJoin
    v['ST_ClrIntMode'] = genST_ClrIntMode
    v['ST_SpreadMethod'] = genST_SpreadMethod
    v['ST_MappingMode'] = genST_ViewUnits
    v['ST_Indices'] = genIndices
    v['ST_StyleSimulations'] =genST_StyleSimulations
    v['ST_UriFont'] = genST_UriFont
    v['ST_SweepDirection'] = genST_SweepDirection

class GenXML:


    def __init__(self, xsd, elem, template, use_default_schemas, enable_choice, print_comments):
        self.xsd = xmlschema.XMLSchema(xsd)
        self.elem = elem
        self.template = template
        self.use_default_schemas = use_default_schemas
        self.enable_choice = enable_choice
        self.print_comments = print_comments
        self.root = True
        self.vals = {}

    # read template text values for tags
    def read_template(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(self.template)
        if config.has_section(self.elem):
            for key in config[self.elem]:
                self.vals[key] = config[self.elem].get(key)

    # shorten the namespace
    def short_ns(self, ns):
        for k, v in self.xsd.namespaces.items():
            if v == ns:
                return k
        return ''

    # if name is using long namespace,
    # lets replace it with the short one
    def use_short_ns(self, name):
        if name[0] == '{':
            x = name.find('}')
            ns = name[1:x]
            short_ns = self.short_ns(ns)
            return short_ns + ":" + name[x + 1:] if short_ns != '' else name[x + 1:]
        return name

    # remove the namespace in name
    def remove_ns(self, name):
        if name[0] == '{':
            x = name.find('}')
            return name[x + 1:]
        return name

    # header of xml doc
    def print_header(self):
        mywrite("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")

    # put all defined namespaces as a string
    def ns_map_str(self):
        ns_all = ''
        s = self.xsd.namespaces if self.use_default_schemas else DEFAULT_SCHEMAS
        for k, v in s.items():
            if ns_all.find(v) == -1:
                prefix = k
                if prefix.find(':') == -1 or prefix == '':
                    prefix = 'xmlns' + (':' + prefix if prefix != '' else '')
                ns_all += prefix + '=\"' + v.format(self.elem) + '\"' + ' '
        return ns_all.strip()

    # start a tag with name
    def start_tag(self, name, attrs=''):
        x = '<' + name
        if self.root:
            self.root = False
            x += ' ' + self.ns_map_str()
        if attrs:
            x += ' ' + attrs
        x += '>'
        return x
    
    # end a tag with name
    def end_tag(self, name):
        return '</' + name + '>'

    # make a sample data for primitive types
    def genval(self, name):

        name = self.remove_ns(name)
        

        if name in self.vals:
            return self.vals[name]()

        return UKN_VALUE



    def genMany(self):
        return 1
        case = random.randint(0,100)
        if(case<1):
            return random.randint(2,3)
        else:
            return 1
    
    # make attributes string
    def gen_attrs(self, attributes,attrs_list):
        a_all = ''
        requese_list=["Width","Height","Color","Offset","Viewbox","Viewport","ViewboxUnits",
        "ViewportUnits","MappingMode","Color","ImageSource","StartPoint","EndPoint","IsLargeArc"
        "Center","GradientOrigin","RadiusX","RadiusY","Points","Size","RotationAngle","OriginX","OriginY"
        "IsLargeArc","SweepDirection","FontRenderingEmSize","FontUri","Matrix","UnicodeString",]

        for attr in attributes:
            if(attr in requese_list  or getpercent(50)):
                tp = attributes[attr].type.name
                attrs_list.append(attributes[attr].name)
                if(tp):
                    a_all += attr + '="' + self.genval(tp) + '" '
        return a_all.strip()

    # print a group
    def group2xml(self, g,node,attrs_list):
        model = str(g.model)
        model = self.remove_ns(model)
        nextg = g._group
        y = len(nextg)
        if y == 0:
            self.print_comment('empty')
            return
    
        self.print_comment('START:[' + model + ']')
        if self.enable_choice and model == 'choice':
            self.print_comment('next item is from a [choice] group with size=' + str(y) + '')
        else:
            self.print_comment('next ' + str(y) + ' items are in a [' + model + '] group')
            
        choice=random.randint(0,y-1)
        times=0
        n = self.use_short_ns(node.name)
        for ng in nextg:
            if(re.search("Transform",str(ng.name)) and getpercent(95)):
                continue
            if(n=="Path"):
                if("Data" in attrs_list and ng.name=="Path.Data"):
                    continue
                elif(("RenderTransform" in attrs_list or getpercent(50))and ng.name=="Path.RenderTransform"):
                    continue
                elif("Clip" in attrs_list and ng.name=="Path.Clip"):
                    continue
                elif("Stroke" in attrs_list and ng.name=="Path.Stroke"):
                    continue
                elif("Fill" in attrs_list and ng.name=="Path.Fill"):
                    continue

            if(n=="Glyphs"):
                if(("RenderTransform" in attrs_list or getpercent(50))and ng.name=="Glyphs.RenderTransform"):
                    continue
                elif("Clip" in attrs_list and ng.name=="Glyphs.Clip"):
                    continue
                elif("Fill" in attrs_list and ng.name=="Glyphs.Fill"):
                    continue

            if(n=="Canvas"):
                if(("RenderTransform" in attrs_list or getpercent(50)) and ng.name=="Canvas.RenderTransform"):
                    continue
                elif("Clip" in attrs_list and ng.name=="Canvas.Clip"):
                    continue

            if(n=="PathGeometry"):
                if("Figures" in attrs_list and ng.name =="PathFigure"):
                    continue

            if(n=="FixedPage" or ng.name=="Path.Data" or getpercent(99)):
                if self.enable_choice and model == 'choice':
                    if times!=choice:
                        times+=1
                        continue

                for i in range(self.genMany()):
                    if isinstance(ng, XsdElement):
                        self.node2xml(ng)
                        if(n=="FixedPage" and isinstance(ng,XsdElement) and getpercent(0)):
                            self.node2xml(ng)
                        if(ng.name=="GradientStop" or ng.name =="PathFigure"):
                            for i in range(1,5):
                                self.node2xml(ng)
                    elif isinstance(ng, XsdAnyElement):
                        self.node2xml(ng)
                    else:
                        self.group2xml(ng,node,[])
            

                if self.enable_choice and model == 'choice':
                    #if(n=="FixedPage" and isinstance(ng,XsdElement)):
                    #    continue
                    #else:
                    break

        self.print_comment('END:[' + model + ']')
    
    # print a node
    def node2xml(self, node):
        if int(node.min_occurs or 1) == 0:
            self.print_comment('next 1 item is optional (minOccurs = 0)')
        if int(node.max_occurs or 1) > 1:
            self.print_comment('next 1 item is multiple (maxOccurs > 1)')
        if isinstance(node, XsdAnyElement):
            mywrite('<_ANY_/>')
            return

        if isinstance(node.type, XsdComplexType):
            n = self.use_short_ns(node.name)
            if node.type.is_simple():
                self.print_comment('simple content')
                tp = str(node.type.content)
                mywrite(self.start_tag(n) + self.genval(tp) + self.end_tag(n))
            elif not isinstance(node.type.content, XsdGroup):
                self.print_comment('complex content')
                attrs = self.gen_attrs(node.attributes)
                tp = node.type.content.name
                mywrite(self.start_tag(n, attrs) + self.genval(tp) + self.end_tag(n))
            else:
                self.print_comment('complex content')
                attrs_list=[]
                attrs = self.gen_attrs(node.attributes,attrs_list)
                if(attrs):
                    mywrite(self.start_tag(n,attrs))
                    self.group2xml(node.type.content,node,attrs_list)
                else:
                    mywrite(self.start_tag(n))
                    self.group2xml(node.type.content,node,attrs_list)
                mywrite(self.end_tag(n))

        elif isinstance(node.type, XsdAtomicBuiltin):
            n = self.use_short_ns(node.name)
            tp = str(node.type.name)
            mywrite(self.start_tag(n) + self.genval(tp) + self.end_tag(n))

        elif isinstance(node.type, XsdSimpleType):
            n = self.use_short_ns(node.name)
            if isinstance(node.type, XsdList):
                self.print_comment('simpletype: list')
                tp = str(node.type.item_type.name)
                mywrite(self.start_tag(n) + self.genval(tp) + self.end_tag(n))
            elif isinstance(node.type, XsdUnion):
                self.print_comment('simpletype: union.')
                self.print_comment('default: using the 1st type')
                tp = str(node.type.member_types[0].base_type.name)
                mywrite(self.start_tag(n) + self.genval(tp) + self.end_tag(n))
            else:
                tp = node.type.base_type.name
                value = self.genval(n)
                if value == UKN_VALUE:
                    value = self.genval(tp)
                mywrite(self.start_tag(n) + value + self.end_tag(n))
        else:
            mywrite('ERROR: unknown type: ' + node.type)
    
    def print_comment(self, comment):
        if self.print_comments:
            mywrite('<!--' + comment + '-->')

    # setup and print everything
    def run(self):
        valsmap(self.vals)
        if self.template:
            self.read_template()
        #self.print_header()
        self.node2xml(self.xsd.elements[self.elem])

def main():
    parser = ArgumentParser()
    parser.add_argument("-s", "--schema", dest="xsdfile", required=True, 
                        help="select the xsd used to generate xml")
    parser.add_argument("-e", "--element", dest="element", required=True,
                        help="select an element to dump xml")
    parser.add_argument("-t", "--template", dest="template",
                        help="template for tag content")
    parser.add_argument("-d", "--default_namespaces", dest="use_default_namespaces", default=False, action="store_true",
                        help="use default namespaces for xml generation")
    parser.add_argument("-c", "--choice",
                        action="store_true", dest="enable_choice", default=False,
                        help="enable the <choice> mode")
    parser.add_argument("-p", "--print_comments", dest="print_comments", default=False,
                        help="print comments to result xml")
    args = parser.parse_args()

    generator = GenXML(args.xsdfile, args.element, args.template, args.use_default_namespaces, args.enable_choice, args.print_comments)
    generator.run()

if __name__ == "__main__":
    main()