from endpoints.classes import Resource

from .post import DOC as post_doc
from .post import post

DATA_ACQUISITION = [
    Resource(
        "POST",
        "/data_acquisition",
        post,
        "Send a Data Acquisition Query",
        "Query For Data",
        post_doc,
    )
]
