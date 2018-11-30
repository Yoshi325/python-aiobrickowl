from typing import Dict
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiError:
    ''' An Error Response from the Api.'''
    error : Dict[str,str]

    '''
    example:
    --------
    {
        "error": {
            "status": "Store not found, you may need to set list_type=customer"
        }
    }
    '''

    @classmethod
    def from_dict(cls, source:Dict):
        if not isinstance(source, dict):
            return None
        error = source.get('error')
        if not error:
            return None
        else:
            return cls(error)
