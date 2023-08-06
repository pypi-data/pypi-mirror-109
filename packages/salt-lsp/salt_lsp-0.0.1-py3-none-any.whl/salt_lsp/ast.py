from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union, overload

from pygls.lsp import types

from salt_lsp.utils import get_last_element_of_iterator


@dataclass(init=False)
class Position:
    line: int
    column: int

    @overload
    def __init__(self, line: int, column: int) -> None:
        ...

    @overload
    def __init__(self, params: types.CompletionParams) -> None:
        ...

    @overload
    def __init__(self, yaml_node: Any) -> None:
        ...

    def __init__(self, *args, **kwargs) -> None:
        if len(args) + len(kwargs) == 2:
            # we are constructing from the (line, column) overload
            self.line = args[0] if len(args) > 0 else kwargs["line"]
            self.column = args[1] if len(args) > 1 else kwargs["column"]
        else:
            if len(args) + len(kwargs) != 1:
                raise ValueError(
                    "Got an invalid number of arguments, expected one, "
                    f"but got {len(args) + len(kwargs)}"
                )
            param = (
                args[0]
                if len(args) == 1
                else get_last_element_of_iterator(kwargs.values())
            )

            if hasattr(param, "position"):
                self.line = param.position.line
                self.column = param.position.character
            elif hasattr(param, "lc"):
                self.line = param.lc.line
                self.column = param.lc.col
            else:
                raise ValueError(
                    "Received an invalid parameter to the Position "
                    f"constructor: {param}"
                )


class NodeType(Enum):
    STATE_ID = auto()
    STATE = auto()
    JINJA = auto()
    STATE_ARGUMENT = auto()


@dataclass
class AstNode:
    entry: str
    children: Optional[Union[AstNode, List[AstNode], Dict[str, AstNode]]]
    node_type: NodeType
    position: Position
