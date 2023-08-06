# -*- coding: utf-8 -*-
#
# co_co_all_variables_defined.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.
from pynestml.cocos.co_co import CoCo
from pynestml.meta_model.ast_declaration import ASTDeclaration
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.meta_model.ast_node import ASTNode
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.variable_symbol import BlockType
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor


class CoCoAllVariablesDefined(CoCo):
    """
    This class represents a constraint condition which ensures that all elements as used in expressions have been
    previously defined.
    Not allowed:
        state:
            V_m mV = V_m + 10mV # <- recursive definition
            V_m mV = V_n # <- not defined reference
        end
    """

    @classmethod
    def check_co_co(cls, node: ASTNode, after_ast_rewrite: bool):
        """
        Checks if this coco applies for the handed over neuron. Models which use not defined elements are not
        correct.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        # for each variable in all expressions, check if the variable has been defined previously
        expression_collector_visitor = ASTExpressionCollectorVisitor()
        node.accept(expression_collector_visitor)
        expressions = expression_collector_visitor.ret
        for expr in expressions:
            for var in expr.get_variables():
                symbol = var.get_scope().resolve_to_symbol(var.get_complete_name(), SymbolKind.VARIABLE)
                # this part is required to check that we handle invariants differently
                expr_par = node.get_parent(expr)

                if symbol is None:
                    # check if this symbol is actually a type, e.g. "mV" in the expression "(1 + 2) * mV"
                    symbol = var.get_scope().resolve_to_symbol(var.get_complete_name(), SymbolKind.TYPE)
                    if symbol is None:
                        # symbol has not been defined; neither as a variable name nor as a type symbol
                        code, message = Messages.get_variable_not_defined(var.get_name())
                        Logger.log_message(node=node, code=code, message=message, log_level=LoggingLevel.ERROR,
                                           error_position=var.get_source_position())
                # first check if it is part of an invariant
                # if it is the case, there is no "recursive" declaration
                # so check if the parent is a declaration and the expression the invariant
                elif isinstance(expr_par, ASTDeclaration) and expr_par.get_invariant() == expr:
                    # in this case its ok if it is recursive or defined later on
                    continue

                # now check if it has been defined before usage, except for predefined symbols, buffers and variables added by the AST transformation functions
                elif (not symbol.is_predefined) \
                        and symbol.block_type != BlockType.INPUT \
                        and not symbol.get_referenced_object().get_source_position().is_added_source_position():
                    # except for parameters, those can be defined after
                    if ((not symbol.get_referenced_object().get_source_position().before(var.get_source_position()))
                            and (not symbol.block_type in [BlockType.PARAMETERS, BlockType.INTERNALS])):
                        code, message = Messages.get_variable_used_before_declaration(var.get_name())
                        Logger.log_message(node=node, message=message, error_position=var.get_source_position(),
                                           code=code, log_level=LoggingLevel.ERROR)
                        # now check that they are now defined recursively, e.g. V_m mV = V_m + 1
                    # todo: we should not check this for invariants
                    if (symbol.get_referenced_object().get_source_position().encloses(var.get_source_position())
                            and not symbol.get_referenced_object().get_source_position().is_added_source_position()):
                        code, message = Messages.get_variable_defined_recursively(var.get_name())
                        Logger.log_message(code=code, message=message, error_position=symbol.get_referenced_object().
                                           get_source_position(), log_level=LoggingLevel.ERROR, node=node)

        # now check for each assignment whether the left hand side variable is defined
        vis = ASTAssignedVariableDefinedVisitor(node, after_ast_rewrite)
        node.accept(vis)


class ASTAssignedVariableDefinedVisitor(ASTVisitor):
    def __init__(self, neuron: ASTNeuron, after_ast_rewrite: bool = False):
        super(ASTAssignedVariableDefinedVisitor, self).__init__()
        self.neuron = neuron
        self.after_ast_rewrite = after_ast_rewrite

    def visit_assignment(self, node):
        symbol = node.get_scope().resolve_to_symbol(node.get_variable().get_complete_name(),
                                                    SymbolKind.VARIABLE)
        if symbol is None:
            if self.after_ast_rewrite:   # after ODE-toolbox transformations, convolutions are replaced by state variables, so cannot perform this check properly
                symbol = node.get_scope().resolve_to_symbol(node.get_variable().get_name(), SymbolKind.VARIABLE)
                if symbol is not None:
                    # an inline expression defining this variable name (ignoring differential order) exists
                    if "__X__" in str(symbol):	 # if this variable was the result of a convolution...
                        return
            else:
                # for kernels, also allow derivatives of that kernel to appear
                if self.neuron.get_equations_block() is not None:
                    for inline_expr in self.neuron.get_equations_block().get_inline_expressions():
                        if node.get_variable().get_name() == inline_expr.variable_name:
                            from pynestml.utils.ast_utils import ASTUtils
                            if ASTUtils.inline_aliases_convolution(inline_expr):
                                symbol = node.get_scope().resolve_to_symbol(node.get_variable().get_name(), SymbolKind.VARIABLE)
                                if symbol is not None:
                                    # actually, no problem detected, skip error
                                    # XXX: TODO: check that differential order is less than or equal to that of the kernel
                                    return

            code, message = Messages.get_variable_not_defined(node.get_variable().get_complete_name())
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(),
                               log_level=LoggingLevel.ERROR, node=self.neuron)


class ASTExpressionCollectorVisitor(ASTVisitor):

    def __init__(self):
        super(ASTExpressionCollectorVisitor, self).__init__()
        self.ret = list()

    def visit_expression(self, node):
        self.ret.append(node)

    def traverse_expression(self, node):
        # we deactivate traversal in order to get only the root of the expression
        pass

    def visit_simple_expression(self, node):
        self.ret.append(node)

    def traverse_simple_expression(self, node):
        # we deactivate traversal in order to get only the root of the expression
        pass
