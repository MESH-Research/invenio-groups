from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator
checker = FormatChecker()
f = checker.checks('isLowercase')(lambda x: x == x.lower())

validator = Draft4Validator({"format": "isLowercase"},
                            format_checker=checker)

# FIXME: how to serve this from "local://groups-metadata-v1.0.0.json"?
groups_metadata_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "id": "local://groups-metadata-v1.0.0.json",
    # "additionalProperties": False,
    "title": "Invenio Groups Metadata Schema v1.0.0",
    "type": "object",
    "properties": {
        "commons_group_id": {"type": "string",
                             "format": "isLowercase"},
        "group_name": {"type": "string"},
        "group_url": {"type": "string"},
        "group_privacy": {"type": "string"},
        "community_privacy": {"type": "string"},
        "group_description": {"type": "string"},
        "profile_image": {"type": "string"},
        "who_can_upload": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["members", "moderators", "administrators"]
            }
        },
        "who_can_accept": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["members", "moderators", "administrators"]
            }
        },
        "invenio_roles": {
            "type": "object",
            "properties": {
                "administrator": {"type": "string"},
                "moderator": {"type": "string"},
                "member": {"type": "string"}
            },
            "required": ["administrator", "moderator", "member"]
        },
        "has_community": {"type": "boolean"}
    },
    "required": ["commons_id", "group_name", "group_description",
                 "group_privacy", "who_can_upload",
                 "who_can_accept", "invenio_roles", "has_community"]
}