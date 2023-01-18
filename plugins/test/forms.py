form = {
    'private': {
        "order": [
          "secret",
          "url"
        ],
        "required": [
          "secret",
          "url"
        ],
        "layout": {},
        "properties": {
          "secret": {
            "type": "string",
            "title": "Something secret",
            "description": "This is stored on the server, and not available to the client except when configuring this plugin.  It is used behind the scene for making API calls, etc.",
            "pattern": "^.+$"
#             "error_message": "Please enter a URL starting with 'https://'",
#             "validators": [
#               {
#                 "id": "regex",
#                 "options": {
#                   "regex": "testregex"
#                 }
#               }
#             ]
          },
          "url": {
            "type": "string",
            "title": "API URL",
            "description": "For example, you may want to configure an API url if this differs at the lab level",
            "pattern": "^https://.+$"
#             "error_message": "Please enter a URL starting with 'https://'",
#             "validators": [
#               {
#                 "id": "regex",
#                 "options": {
#                   "regex": "testregex"
#                 }
#               }
#             ]
          }
        }
        },
    'public': {
        "order": [
          "test",
        ],
        "required": [
          "test",
        ],
        "layout": {},
        "properties": {
          "test": {
            "type": "string",
            "title": "Test input",
            "validators": [],
            "description": "Please enter anything.  This will be available to the frontend via an API call when rendering the plugin.",
            "pattern": "^.+$"
#             "error_message": "Please enter a URL starting with 'https://'",
#             "validators": [
#               {
#                 "id": "regex",
#                 "options": {
#                   "regex": "testregex"
#                 }
#               }
#             ]
          }
        }
      }
    }