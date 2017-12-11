class thingy:

    def __init__(self,indict):
        self.stuff = indict

    def __getattr__(self,which):
        return self.stuff.get(which,None)