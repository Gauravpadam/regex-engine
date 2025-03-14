from ASM import *

# Let's make a manual AST for the expression *(a|bc)d


alternation_node = Alternation(children=[
    MatchCharacter("a"),
    MatchString("bc")
])

group_node = Group(children=[alternation_node], index = 1, is_capturing = True)

quantifier = Quantifier(qtype = QuantifierType.ZERO_OR_MORE, is_lazy=False)

quant_expr_node = QuantifiedExpression(expression=group_node, quantifier = quantifier)

match_d_node = MatchCharacter("d")

implicit_group_node = ImplicitGroup(children=[quant_expr_node, match_d_node])

ast = AST(is_from_start_of_string=True, root=implicit_group_node)

print(ast)