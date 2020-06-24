class elements_2(object):
    """"Arrays of basic elements of lattice 
    
    nodes[]: array of nodes
    beams[]: array of beams
    periods[]: array of periodicity vectors
    profiles[]: array of profiles : section type and material
    Mode: actual mode 
    P1_acquired: point 1 node for mode ADD BEAM P1
    P1_acquired_bool: True if a Point 1 node is yet acquired 

    draw(dc,view): draw all objects : nodes, beams, periodicity vectors
    IndexNode(node): return the index of an node based on identifier value

    """
    def __init__(self,parent):
        self.parent=parent
        self.nodes=[]
        self.beams=[]
        self.periods=[]
        self.profiles=[]
