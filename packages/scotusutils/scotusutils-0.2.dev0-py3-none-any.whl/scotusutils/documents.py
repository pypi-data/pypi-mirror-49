import datetime


class BaseAttrClass(object):
    _DATA_ATTRS_MAPPING = {}

    @classmethod
    def init_from_kwargs(cls, **kwargs):
        new_item = cls()
        data_dict = {}
        for key, value in kwargs.items():
            if key not in new_item._DATA_ATTRS_MAPPING:
                pass
            if not isinstance(value, new_item._DATA_ATTRS_MAPPING[key]["type"]):
                pass
            data_dict[key] = value
        new_item._data_dict = data_dict
        return new_item

    @property
    def dict(self):
        return {key: value for key, value in self._data_dict.items()}

    def __init__(self, **kwargs):
        self._data_dict = {
            name: self._DATA_ATTRS_MAPPING[name]["default_value"]
            for name in self._DATA_ATTRS_MAPPING
        }

    def __getattr__(self, attr):
        if attr in self._DATA_ATTRS_MAPPING:
            return self._data_dict[attr]
        else:
            err_msg = f"Attr '{attr}' is not a valid attribute name"
            raise ValueError(err_msg)


class Case(BaseAttrClass):
    _DATA_ATTRS_MAPPING = {
        "case_id": {"type": str, "default_value": None},
        "name": {"type": str, "default_value": None},
        "date": {"type": datetime.date, "default_value": None},
        "term": {"type": str, "default_value": None},
    }

    def __repr__(self):
        return "<Case(case_id='%s', name='%s', date='%s', term='%s')>" % (
            self.case_id,
            self.name,
            self.date,
            self.term,
        )


class OralArgTranscript(BaseAttrClass):
    """
    An Oral Arguments Transcript data object representation.

    Contains data relevant for oral arguments transcripts.

    """

    _DATA_ATTRS_MAPPING = {
        "case_id": {"type": str, "default_value": None},
        "name": {"type": str, "default_value": None},
        "date": {"type": datetime.date, "default_value": None},
        "file_url": {"type": str, "default_value": None},
        "file_path": {"type": str, "default_value": None},
        "transcript": {"type": bytes, "default_value": None},
    }

    @classmethod
    def init_from_oralarg(cls, oral_arg_web):
        data_dict = {
            name: getattr(oral_arg_web, name)
            for name in cls._DATA_ATTRS_MAPPING
            if name != "transcript"
        }
