from src.TableauxBuilder.BaseTableauxBuilder import BaseTableauxBuilder


def curry(function, *c_args, **c_kwargs):
    def curried(*args, **kwargs):
        return function(*c_args, *args, **c_kwargs, **kwargs)

    return curried


class DrawingCalculator:
    def __init__(self, tableau: BaseTableauxBuilder,
                 painter, manual, intuitionisitc, margin,
                 x=375, parent_processed: (list, list, list)=None):
        self.tableau = tableau
        self.painter = painter
        self.x = x
        self.margin = margin
        self.parent_processed = ([], [], []) if parent_processed is None else parent_processed
        processed_exprs = tableau.get_processed_exprs()
        l = [x for x in processed_exprs[0] if x not in self.parent_processed[0]]
        r = [x for x in processed_exprs[1] if x not in self.parent_processed[1]]
        cf = [x for x in processed_exprs[2] if x not in self.parent_processed[2]]
        self.processed_exprs = (l, r, cf)

        self.closed = tableau.is_closed()
        self.done = tableau.is_done()

        self.manual = manual
        self.intuitionistic = intuitionisitc

    def get_child(self, child_idx, new_x):
        parent_processed = (self.parent_processed[0] + self.processed_exprs[0],
                            self.parent_processed[1] + self.processed_exprs[1],
                            self.parent_processed[2] + self.processed_exprs[2],)
        
        child = self.tableau.children[child_idx]
        return type(self)(
            child, self.painter, self.manual, self.intuitionistic,
            self.margin, new_x, parent_processed,
        )

    def get_child_clears_false(self, tableau=None):
        if tableau is None:
            tableau = self.tableau
        child_clears_false = len(tableau.children) > 0 and not all([not child.clears_false_exprs for child in tableau.children])
        if len(self.tableau.children) > 0:
            if any([child.clears_false_exprs for child in tableau.children]):
                return True
            return any([self.get_child_clears_false(c) for c in tableau.children])
        return False

    def calc_expr_positions(self, draw_btn_fun):
        child_clears_false = self.get_child_clears_false()

        # a close tableau does not need to draw unprocessed exprs
        not_include_unprocessed = self.closed
        if self.intuitionistic:
            not_include_unprocessed = not child_clears_false
            if len(self.tableau.children) == 0:
                not_include_unprocessed = not self.manual
        else:
            not_include_unprocessed = self.closed
        unprocessed_exprs = ([], [], []) if not_include_unprocessed else self.tableau.get_unprocessed_exprs(self.manual)
        atom_exprs = self.tableau.get_atom_exprs()
        partially_exprs = self.tableau.get_partially_processed_exprs(self.manual)

        # calculate horizontal positions of expressions
        expr_pos = self.to_pos_list(self.processed_exprs, self.x, self.painter.draw_underlined)
        expr_pos.extend(self.to_pos_list(atom_exprs, self.x, self.painter.draw_normal, include_atoms=True))
        
        dotted_underlined = self.painter.draw_dotted_underlined
        normal = self.painter.draw_normal
        if self.manual and not self.closed and not self.done and not child_clears_false:
            dotted_underlined = draw_btn_fun(self.painter, self.tableau)
            normal = draw_btn_fun(self.painter, self.tableau)
        expr_pos.extend(self.to_pos_list(partially_exprs, self.x, dotted_underlined))
        expr_pos.extend(self.to_pos_list(unprocessed_exprs, self.x, normal, include_atoms=True))

        # sort by processing order
        expr_pos.sort(key=lambda x: x[1].visit_idx)

        # unvisited expressions have idx = -1
        # put those at the end of the list
        unvisited_exprs = [x for x in expr_pos if x[1].visit_idx == -1]
        expr_pos = expr_pos[len(unvisited_exprs):]
        expr_pos.extend(unvisited_exprs)

        return expr_pos

    def to_pos_list(self, exprs, x, draw_fun, include_atoms=False):
        """
        Converts a list of expressions to a list of tuples
        Tuples are added if include_atoms is True or the expr is not a atom
        (x-pos, expression, draw_function)
        """
        lst = [(
                    x - self.margin - self.painter.get_text_width(str(expr)),
                    expr,
                    curry(draw_fun, expr=(expr, None, None)),
                    str(expr),
                )
               for expr in exprs[0] if not expr.is_atom or include_atoms]
        lst.extend([(
                        x + self.margin,
                        expr,
                        curry(draw_fun, expr=(None, expr, None)),
                        str(expr)
                    )
                    for expr in exprs[1] if not expr.is_atom or include_atoms])
        lst.extend([(
                        x + self.margin,
                        expr,
                        curry(draw_fun, expr=(None, None, expr)),
                        '[' + str(expr) + ']',
                    )
                    for expr in exprs[2] if not expr.is_atom or include_atoms])

        return lst
