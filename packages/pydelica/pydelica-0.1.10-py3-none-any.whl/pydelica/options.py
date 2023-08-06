import collections.abc
import os
import enum
import defusedxml.ElementTree as ET

from pydelica.exception import UnknownOptionError

from typing import Any


class Solver(enum.Enum):
    DASSL = "dassl"
    EULER = "euler"
    RUNGE_KUTTA = "rungekutta"


class SimulationOptions(collections.abc.MutableMapping):
    def __init__(self, xml_model_file: str) -> None:
        self._model_xml = xml_model_file

        if not os.path.exists(xml_model_file):
            raise FileNotFoundError(
                "Could not extract simulation options, "
                f"no such file '{xml_model_file}"
            )

        with open(xml_model_file) as f:
            _xml_obj = ET.parse(xml_model_file)

        self._opts = list(_xml_obj.iterfind("DefaultExperiment"))[0].attrib

    def _write_opts(self):
        _xml_obj = ET.parse(self._model_xml)

        for opt in _xml_obj.findall("DefaultExperiment")[0].attrib:
            _xml_obj.findall("DefaultExperiment")[0].attrib[opt] = str(
                self._opts[opt]
            )

        _xml_obj.write(self._model_xml)

    def __setitem__(self, key: str, value: Any) -> None:
        self._opts[key] = value
        self._write_opts()

    def __getitem__(self, key: str) -> Any:
        return self._opts[key]

    def __delitem__(self, key: str) -> None:
        del self._opts[key]

    def set_option(self, option_name: str, value: Any) -> None:
        if option_name not in self._opts:
            raise UnknownOptionError(option_name)
        _opt = [
            i for i in self._opts.keys() if i.lower() == option_name.lower()
        ][0]
        self._opts[_opt] = value
        self._write_opts()

    def __len__(self):
        return len(self._opts)

    def __iter__(self):
        return iter(self._opts)
