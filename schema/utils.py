from builtins import property

class SchemaException(Exception):
    pass

class Schema(object):
    TYPE_TABLE = 'table'
    TYPE_TEXT = 'text'
    TYPE_NUMBER = 'number'
    TYPE_BOOLEAN = 'boolean'
    def __init__(self, schema, data=[]):
        self.schema = schema
        self.data = data
    def get_variables_of_type(self, TYPE):
        try:
            return [v for v in self.schema['order'] if self.schema['properties'][v]['type'] == TYPE]
        except:
            raise SchemaException('Poorly formed schema')
    @property
    def table_variables(self):
        return self.get_variables_of_type(Schema.TYPE_TABLE)
    def variable_title(self, variable):
        title =self.schema['properties'][variable].get('title', None)
        return title if title is not None else variable

def schema_to_filters(schema):
    filters = {}
    for v, definition in schema['properties'].items():
        if definition['type'] == 'table' and 'schema' in definition:
            table, table_definition = v, definition
            for v, definition in table_definition['schema']['properties'].items():
                v = '{}__{}'.format(table, v)
                if definition['type'] == 'string':
                    filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}__contains'.format(v)}]}
                    if definition.get('enum'):
                        filters[v]['enum'] = definition.get('enum')
                elif definition['type'] == 'number':
                    filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}__contains'.format(v)}]}
        elif definition['type'] == 'string':
            filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}'.format(v)}, {'label': 'contains', 'filter': 'submission_data__{}__icontains'.format(v)}]}
            if definition.get('enum'):
                filters[v]['enum'] = definition.get('enum')
        elif definition['type'] == 'number':
            filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}'.format(v)}, {'label': '>', 'filter': 'submission_data__{}__gt'.format(v)}, {'label': '<', 'filter': 'submission_data__{}__lt'.format(v)}]}
        elif definition['type'] == 'boolean':
            filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}__boolean'.format(v)}], 'enum': ['True', 'False']}
    return filters

def submission_type_schema_filters(submission_type):
    return schema_to_filters(submission_type.submission_schema)

def all_submission_type_filters(lab):
    filters = []
    filters.append({'name': 'ALL', 'id': 'ALL', 'filters': schema_to_filters(lab.submission_variables)})
    for t in lab.submission_types.all():
        type_filters = submission_type_schema_filters(t)
        filters.append({'name': t.name, 'id': t.id, 'filters': type_filters})
    return filters

# Take a coreomics style schema, and convert it to a standard jsonschema, replacing 'table' type with 'array' type where necessary
def convert_to_jsonschema(coreomics_schema):
    import copy
    schema = copy.deepcopy(coreomics_schema)
    schema['type'] = 'object'
    # Make changes to schema
    if 'properties' in schema:
        for prop in schema['properties'].keys():
            if 'table' == schema['properties'].get(prop,{}).get('type', '').lower():
                list_prop = {'type': 'array', 'items': schema['properties'][prop].pop('schema')}
                schema['properties'][prop] = list_prop
                schema['properties'][prop]['items']['type'] = 'object'
    return schema
GROUP_DISPLAY_OPTIONS = ['box', 'header']

def normalize_layout(schema):
    """
    Normalize the optional field grouping keys of a submission schema.

    `layout_order` lists ungrouped field names and group ids in display order.
    `groups` maps group ids to {title, fields, ...}, where `fields` lists the
    group's field names in display order.  `order` remains the flat list of all
    fields and is rebuilt from `layout_order` so both agree.

    Problems only a grouping-aware client can cause (duplicates, id collisions,
    malformed groups) raise SchemaException.  Stale data left by clients that
    don't know about groups (deleted or added fields) is repaired silently.
    Schemas without `groups` or `layout_order` are returned unchanged.
    """
    if not isinstance(schema, dict) or ('groups' not in schema and 'layout_order' not in schema):
        return schema
    import copy
    schema = copy.deepcopy(schema)
    properties = schema.get('properties') or {}
    order = schema.get('order') or []
    groups = schema.get('groups')
    groups = {} if groups is None else groups
    layout_order = schema.get('layout_order')
    layout_order = [] if layout_order is None else layout_order
    if not isinstance(groups, dict):
        raise SchemaException('"groups" must be an object')
    if not isinstance(layout_order, list):
        raise SchemaException('"layout_order" must be a list')
    for group_id, group in groups.items():
        if not group_id:
            raise SchemaException('Group ids must not be empty')
        if group_id in properties:
            raise SchemaException('Group id "{}" is also a field name'.format(group_id))
        if not isinstance(group, dict):
            raise SchemaException('Group "{}" must be an object'.format(group_id))
        if not isinstance(group.get('title'), str) or not group['title'].strip():
            raise SchemaException('Group "{}" requires a title'.format(group_id))
        if not isinstance(group.get('fields', []), list):
            raise SchemaException('Group "{}" fields must be a list'.format(group_id))
        if group.get('display', 'box') not in GROUP_DISPLAY_OPTIONS:
            raise SchemaException('Group "{}" display must be one of: {}'.format(group_id, ', '.join(GROUP_DISPLAY_OPTIONS)))
    seen = set()
    def check_duplicate(id):
        if id in seen:
            raise SchemaException('"{}" appears more than once in the layout'.format(id))
        seen.add(id)
    # Drop ids that no longer exist, and reject duplicates among the rest
    new_layout_order = []
    for id in layout_order:
        if id in properties or id in groups:
            check_duplicate(id)
            new_layout_order.append(id)
    for group_id, group in groups.items():
        fields = []
        for field in group.get('fields', []):
            if field in groups:
                raise SchemaException('Group "{}" cannot contain group "{}"'.format(group_id, field))
            if field in properties:
                check_duplicate(field)
                fields.append(field)
        group['fields'] = fields
    # Append fields and groups that aren't placed anywhere yet
    for field in order + [f for f in properties if f not in order]:
        if field in properties and field not in seen:
            seen.add(field)
            new_layout_order.append(field)
    for group_id in groups:
        if group_id not in seen:
            seen.add(group_id)
            new_layout_order.append(group_id)
    schema['groups'] = groups
    schema['layout_order'] = new_layout_order
    schema['order'] = [field for id in new_layout_order for field in (groups[id]['fields'] if id in groups else [id])]
    return schema
