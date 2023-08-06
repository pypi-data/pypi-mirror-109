# Claudio Perez
# 2021
"""
Parse a CSMIP Volume 2 strong motion data file.
"""
import re
import zipfile
from pathlib import Path
from collections import defaultdict

import numpy as np

from .core import (
    GroundMotionEvent,
    GroundMotionRecord,
    GroundMotionSeries,
    # RealNumber
)
from .utils.parseutils import (
    parse_sequential_fields,
    open_quake
)

# Module constants
NUM_COLUMNS = 8
HEADER_END_LINE = 45

# Regular expression for extracting decimal number
RE_DECIMAL = "[-]?[0-9]*[.][0-9]*"
# Regular expression for extracting units
RE_UNITS = "[a-z,/,*,0-9]*"

# fmt: off
HEADER_FIELDS = {
    ("record.station_no", "record.azimuth"): ((str, str),
        re.compile(
            rf"Station No\. *([0-9]*) *({RE_DECIMAL}[NSEW]*, *{RE_DECIMAL}[NSEW]*)"
        )
    ),
    ("record.instr_period", ".units"): ((float, str),
        re.compile(
            rf"Instr Period = ({RE_DECIMAL}) ({RE_UNITS}),"
        )
    ),
    ("record.peak_accel", ".units", ".time"): ((float, str, float),
        re.compile(
            rf"Peak *acceleration *= *({RE_DECIMAL}) *({RE_UNITS}) *at *({RE_DECIMAL})"
        )
    ),
    ("record.peak_veloc", ".units", ".time"): ((float, str, float),
        re.compile(
            rf"Peak *velocity *= *({RE_DECIMAL}) *({RE_UNITS}) *at *({RE_DECIMAL})"
        )
    ),
    ("record.peak_displ", ".units", ".time"): ((float, str, float),
        re.compile(
            rf"Peak *displacement *= *({RE_DECIMAL}) *({RE_UNITS}) *at *({RE_DECIMAL})"
        )
    ),
    ("record.init_veloc", ".units"): ((float, str),
        re.compile(rf"Initial velocity *= *({RE_DECIMAL}) *({RE_UNITS});"),
    ),
    ("accel.shape", "accel.time_step"): ((int, float),
        re.compile(f"([0-9]*) *points of accel data equally spaced at *({RE_DECIMAL})")
    ),
    ("veloc.shape", "accel.time_step"): ((int, float),
        re.compile(f"([0-9]*) *points of veloc data equally spaced at *({RE_DECIMAL})")
    ),
    ("displ.shape", "accel.time_step"): ((int, float),
        re.compile(f"([0-9]*) *points of displ data equally spaced at *({RE_DECIMAL})")
    ),
}
# fmt: on


def read_event(read_file, **kwds):
    """
    Take the name of a CSMIP zip file and extract record data for the event.
    """
    zippath = Path(read_file)
    archive = zipfile.ZipFile(zippath)
    records = []
    for file in archive.namelist():
        if file.endswith(".v2"):
            records.append(read_record_v2(file, archive))
    metadata = {}
    return GroundMotionEvent("file_name", *records, **metadata)


def read_record_v2(
    read_file, archive: zipfile.ZipFile = None, summarize=False, **kwds
) -> GroundMotionRecord:
    """
    Read a ground motion record using the CSMIP Volume 2 format
    """
    filename = Path(read_file)
    # Parse header fields
    with open_quake(read_file, "r", archive) as f:
        header_data = parse_sequential_fields(f, HEADER_FIELDS)
    parse_options = dict(
        delimiter=10,  # fields are 10 chars wide
    )
    # Reopen and parse out data; Note, only the first call
    # provides a skip_header argument as successive reads
    # pick up where the previous left off.
    if not summarize:
        with open_quake(read_file, "r", archive) as f:
            accel = np.genfromtxt(
                f,
                skip_header=HEADER_END_LINE + 1,
                max_rows=header_data["accel.shape"] // NUM_COLUMNS,
                **parse_options,
            ).flatten()
            next(f)
            veloc = np.genfromtxt(
                f, max_rows=header_data["veloc.shape"] // NUM_COLUMNS, **parse_options
            ).flatten()
            next(f)
            displ = np.genfromtxt(
                f, max_rows=header_data["displ.shape"] // NUM_COLUMNS, **parse_options
            ).flatten()
    else:
        accel, veloc, displ = None, None, None

    # Separate out metadata
    record_data = {}
    series_data = defaultdict(dict)
    for key, val in header_data.items():
        typ, k = key.split(".", 1)
        if typ == "record":
            record_data.update({k: val})
        elif typ in ["accel", "veloc", "displ"]:
            series_data[typ].update({k: val})

    record_data["file_name"] = filename.name
    return GroundMotionRecord(
        GroundMotionSeries(accel, series_data["accel"]),
        GroundMotionSeries(veloc, series_data["veloc"]),
        GroundMotionSeries(displ, series_data["displ"]),
        meta=record_data,
    )


FILE_TYPES = {
    "csmip.v1": {"type": GroundMotionRecord, "read": read_record_v2},
    "csmip.v2": {"type": GroundMotionRecord, "read": read_record_v2},
    "csmip.v3": {"type": GroundMotionRecord, "read": read_record_v2, "spec": ""},
    "csmip.zip": {"type": GroundMotionEvent, "read": read_event},
}


def read_record(read_file, *args):
    file = Path(read_file)
    if file.suffix == ".v2":
        return read_record_v2(file)


def read(read_file, input_format=None):
    # file_type = get_file_type(file,file_type,"csmip")
    # if isinstance(
    pass
