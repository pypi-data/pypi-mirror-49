from .generator import Generator, PortType, PortDirection, BlockEdgeType, \
    always, verilog, signed, CombinationalCodeBlock, SequentialCodeBlock

from .passes import Attribute

# directly import from the underlying C++ binding
from _kratos.util import is_valid_verilog
from _kratos.exception import VarException, StmtException
from _kratos.passes import IRVisitor as IRVisitor
from _kratos import SwitchStmt, PackedStruct, Port, Var, IfStmt, AssignmentType
from _kratos import AssignStmt

__all__ = ["Generator", "PortType", "PortDirection", "BlockEdgeType", "always",
           "verilog", "signed", "is_valid_verilog", "VarException",
           "StmtException", "IRVisitor"]

# code blocks
__all__ += ["CombinationalCodeBlock", "SequentialCodeBlock", "SwitchStmt",
            "PackedStruct", "Port", "Var", "IfStmt", "AssignmentType",
            "AssignStmt"]
