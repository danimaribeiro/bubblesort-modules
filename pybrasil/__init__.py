#coding=utf-8
import xml.etree.ElementTree as ET

class DynamicXml(object):    
    def __getattr__(self, name):
        try:
            return object.__getattribute__(self,name)
        except:           
            self.__setattr__(name, None)
            return object.__getattribute__(self,name)
            
    def __setattr__(self, obj, val):
        if(obj=="value" or obj=="atributos"):
            object.__setattr__(self,obj, val)
        else:
            object.__setattr__(self,obj, DynamicXml(val))

    def __init__(self, value):
        self.value = value
        self.atributos={}
    def __str__(self):
        return str(self.value)
    def __call__(self, *args, **kw):
        if(len(kw)>0):
            self.atributos=kw
        if(len(args)>0):
            self.value= args[0]
        else:
            return self.value


def serialize_xml():
    def xml_recursive(xml, objeto):
        for attr, value in objeto.__dict__.items():
            if(attr!="value" and attr!="atributos"):            
                sub = ET.SubElement(xml,attr)
                if(str(value)!="None"):
                    sub.text = str(value)
                xml_recursive(sub, value)
            elif(attr=="atributos"):
                for atr, val in value.items():                
                    xml.set(atr.replace("__", ":"), str(val))

    print("Iniciando a geração do xml")
    root = ET.Element(str(t))
    xml_recursive(root, t)
    
    tree = ET.ElementTree(root)
    tree.write("/home/danimar/nfe.xml")
    

t = DynamicXml("NFe")
t(xmlns__id="NFe12038903283904823748923798")
t.pessoa.nome("Metodo")
t.pessoa.nome = "Propriedade"   
t.pessoa(id="123", cpf="019209012")

print(t.danimar.ribeiro.jaqueline.barp())

serialize_xml()

