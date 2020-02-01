def visitor(visitor_class: object):
    def visited(self, obj: object):
        # save idx where the expr was visited
        visit_idx = obj.__getattribute__("visit_idx")
        setattr(self, "visit_idx", visit_idx)
        setattr(obj, "visit_idx", visit_idx + 1)

        # call visitor
        obj.__getattribute__("visited_" + visitor_class.__name__)(self)
    setattr(visitor_class, "visit", visited)
    setattr(visitor_class, "visit_idx", -1)
    return visitor_class
