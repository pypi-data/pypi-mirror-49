from ..igvtools_2_0 import IgvTools_2_0
from .base import IgvToolsIndexBase


class IgvToolsIndex_2_0(IgvTools_2_0, IgvToolsIndexBase):
    pass


if __name__ == "__main__":
    print(IgvToolsIndex_2_0().help())
