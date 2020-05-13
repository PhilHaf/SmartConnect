import hou
import nodegraph

def getRunning():
    return hou.session.scRunning
def setRunning(input):
    hou.session.scRunning = input

def getLast():
    return hou.session.scLastNode
def setLast(node):
    hou.session.scLastNode = node
    
def getCurrent():
    return hou.session.scCurrentNode
def setCurrent(node):
    hou.session.scCurrentNode = node
    
def initVariables():
    hou.ui.removeAllSelectionCallbacks()
    hou.session.scRunning = None
    hou.session.scCurrentNode = None
    hou.session.scLastNode = None
    hou.ui.addSelectionCallback(selectionCallback)
    setRunning(1)
    
def selectionCallback(selection):

    try:
        if (len(selection)>0):
            
            #print(selection)
            #print("length ", len(selection))
            #print("lastNode", getLast())
            
            if (getCurrent()!=None):
                
                setLast(getCurrent())
            setCurrent(selection)
        
    except:

        print("An Selection exception occurred")
        
def connectByHeight(node1, node2):
    #print("connectByHeight")
    if sameParents(node1, node2) == True:
        
        if (node1.position()[1]>node2.position()[1]):
            setCurrent([node2])
            setLast([node1])
        else:
            setCurrent([node1])
            setLast([node2])
        connectByLastSelection()
    
def sameParents(node1, node2):
    if node1.parent().name()==node2.parent().name():
        return True
    else:
        return False
    
    
def connectByLastSelection():
    #print("connectByLastSelection")
    last = getLast()[0]
    current = getCurrent()[0]
    
    if (last!=None and current!=None):
        if sameParents(last, current) == True:
            if ( len(last.outputConnectors())>0 and len(current.inputConnectors())>0):
                
                pos = switchInput(current, last)
                current.setInput(pos, last, 0)
    
    
def switchInput(current, last):
    #print("switchInput")
    found=-1
            
    for ele in current.inputConnections():

        if (ele.inputNode().name() == last.name()):
            found = ele.inputIndex()

            current.setInput(found, None, 0)
            #print("already connected")
            if len(current.inputConnectors())>=found+2:
                found += 1
            else:
                found = 0
            break
    
    if found<0:
        found = 0
    return found
    
if kwargs['ctrlclick'] or kwargs['cmdclick']:
    #RESET
    initVariables()
    #print("reset")
else:
    try:
        if getRunning():
    
            #CALLBACK is running
            
            if len(getCurrent())>1:
                connectByHeight(getCurrent()[0], getCurrent()[1])
            else:
                connectByLastSelection()
        else:
            #print("start")
            #START CALLBACK
            
            initVariables()
    except:
        initVariables()