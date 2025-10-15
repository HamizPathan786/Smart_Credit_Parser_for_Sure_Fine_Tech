
from .hdfc_parser import HDFCParser
from .sbi_parser import SBIParser
from .icici_parser import ICICIParser
from .axis_parser import AxisParser
from .citi_parser import CitiParser

__all__ = ["HDFCParser", "SBIParser", "ICICIParser", "AxisParser", "CitiParser"]

PARSERS = {
    "hdfc": HDFCParser,
    "sbi": SBIParser,
    "icici": ICICIParser,
    "axis": AxisParser,
    "citi": CitiParser
}

