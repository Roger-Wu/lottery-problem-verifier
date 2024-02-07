from typing import List, Tuple, Dict, Set, Union
from int_set.native_int_set import NativeIntSet
# from int_set.numpy_int_set import NumpyIntSet

TicketType = Tuple[int, ...]
TicketComboType = Tuple[int, ...]
TicketIndexType = int
TicketIndexListType = List[TicketIndexType]
TicketIndexSetType = Set[TicketIndexType]
TicketComboListType = List[TicketComboType]
TicketComboSetType = Set[TicketComboType]
DrawType = Tuple[int, ...]
DrawComboType = Tuple[int, ...]
DrawIndexType = int
# DrawSetType = Union[NativeIntSet, NumpyIntSet]
DrawSetType = NativeIntSet
