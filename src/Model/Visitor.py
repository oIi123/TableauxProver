def visitor(visitor_class: object):
    def visited(self, obj: object):
        obj.__getattribute__("visited_" + visitor_class.__name__)(self)
    setattr(visitor_class, "visit", visited)
    return visitor_class
