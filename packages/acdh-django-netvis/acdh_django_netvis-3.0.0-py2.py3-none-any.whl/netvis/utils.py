import random

from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


def model_to_dict(instance):
    """
    serializes a model.object to dict, including non editable fields as well as
    ManyToManyField fields
    """
    field_dicts = []
    for x in instance._meta.get_fields():
        f_type = "{}".format(type(x))
        field_dict = {
            "name": x.name,
            "help_text": getattr(x, 'help_text', ''),
        }
        try:
            field_dict['extra_fields'] = x.extra
        except AttributeError:
            field_dict['extra_fields'] = None
        if 'reverse_related' in f_type:
            values = getattr(instance, x.name, None)
            if values is not None:
                field_dict['value'] = values.all()
            else:
                field_dict['value'] = []
            if getattr(x, 'related_name', None) is not None:
                field_dict['verbose_name'] = getattr(x, 'related_name', x.name)
            else:
                field_dict['verbose_name'] = getattr(x, 'verbose_name', x.name)
            field_dict['f_type'] = 'REVRESE_RELATION'
        elif 'related.ForeignKey' in f_type:
            field_dict['verbose_name'] = getattr(x, 'verbose_name', x.name)
            field_dict['value'] = getattr(instance, x.name, '')
            field_dict['f_type'] = 'FK'
        elif 'TreeForeignKey' in f_type:
            field_dict['verbose_name'] = getattr(x, 'verbose_name', x.name)
            field_dict['value'] = getattr(instance, x.name, '')
            field_dict['f_type'] = 'FK'
        elif 'related.ManyToManyField' in f_type:
            values = getattr(instance, x.name, None)
            if values is not None:
                field_dict['value'] = values.all()
            else:
                field_dict['value'] = []
            field_dict['verbose_name'] = getattr(x, 'verbose_name', x.name)
            field_dict['f_type'] = 'M2M'
        elif 'fields.DateTimeField' in f_type:
            field_value = getattr(instance, x.name, '')
            field_dict['verbose_name'] = getattr(x, 'verbose_name', x.name)
            field_dict['f_type'] = 'DateTime'
            if field_value:
                field_dict['value'] = (field_value.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            field_dict['verbose_name'] = getattr(x, 'verbose_name', x.name)
            field_dict['value'] = f"{getattr(instance, x.name, '')}"
            field_dict['f_type'] = 'SIMPLE'
        field_dicts.append(field_dict)
    return field_dicts


def color_generator(number_of_colors=5):
    """ generats some random Hex Color Codes
        taken from https://stackoverflow.com/questions/28999287/generate-random-colors-rgb
        :param number_of_colors: The number colors to generate
        :return: A list of Hex COlor Codes
    """

    number_of_colors = number_of_colors
    color = [
        "#" + ''.join(
            [random.choice('0123456789ABCDEF') for j in range(6)]
        ) for i in range(number_of_colors)
    ]
    return color


def as_node(instance):
    """ serializes an object as netvis-nodes
        :param instance: An instance of a django model class
        :return: A dict with keys 'type', 'label' and 'id'
    """
    app_name = instance._meta.app_label.lower()
    model_name = instance.__class__.__name__.lower()
    node = {}
    node["type"] = f"{app_name}__{model_name}"
    node["label"] = f"{instance.__str__()}"
    node["id"] = f"{node['type'].lower()}__{instance.id}"
    try:
        node['detail_view_url'] = f"{instance.get_absolute_url()}"
    except AttributeError:
        node['detail_view_url'] = "asdf/asdf/asdf/no-get-absolute-url-defined"
    node['as_graph'] = reverse(
        'netvis:graph',
        kwargs={
            "app_name": app_name,
            "model_name": model_name,
            "pk": instance.id
        }
    )
    return node


def add_node_types(base_graph):
    """ takes a base graph (nodes and edges) and adds node and edge type arrays
        :param base_grape: A dict with node and edges arrays
        :return: A dict according to netvis graph data model
    """
    graph = base_graph
    graph['types'] = {
        'nodes': [],
        'edges': []
    }
    nodes = [x['type'] for x in graph['nodes']]
    colors_dict = dict(zip(set(nodes), color_generator(len(set(nodes)))))
    for x in set(nodes):
        app_label, model = x.split('__')[:2]
        ct = ContentType.objects.get(
            app_label=app_label, model=model
        ).model_class()._meta.verbose_name
        graph['types']['nodes'].append(
            {
                'id': f"{x}",
                'label': f"{ct}",
                'color': f"{colors_dict[x]}"
            }
        )
    return graph


def as_graph(instance):
    """ serializes an object and its related (FK, M2M) objects as netvis-graph
        :param instance: An instance of a django model class
        :return: A dict with keys 'nodes' and 'edges'
    """
    obj_dict = model_to_dict(instance)
    graph = {
        'nodes': [as_node(instance)],
        'edges': []
    }

    for x in obj_dict:
        if x['f_type'] == 'FK' and x['value'] is not None:
            graph['nodes'].append(as_node(x['value']))
            graph['edges'].append(
                {
                    'id': f"{as_node(instance)['id']}__{as_node(x['value'])['id']}",
                    'source': as_node(instance)['id'],
                    'target': as_node(x['value'])['id'],
                    'label': x['verbose_name']
                }
            )
        elif x['f_type'] == 'M2M' and len(x['value']) > 0:
            for y in x['value']:
                graph['nodes'].append(as_node(y))
                graph['edges'].append(
                    {
                        'id': f"{as_node(instance)['id']}__{as_node(y)['id']}",
                        'source': as_node(instance)['id'],
                        'target': as_node(y)['id'],
                        'label': x['verbose_name']
                    }
                )
        elif x['f_type'] == 'REVRESE_RELATION' and len(x['value']) > 0:
            for y in x['value']:
                graph['nodes'].append(as_node(y))
                graph['edges'].append(
                    {
                        'id': f"{as_node(instance)['id']}__{as_node(y)['id']}",
                        'source': as_node(instance)['id'],
                        'target': as_node(y)['id'],
                        'label': x['verbose_name']
                    }
                )
    new_graph = add_node_types(graph)
    return new_graph


def qs_as_graph(qs, limit=100):
    """ serializes a django queryset as netvis-graph
        :param qs: A django queryset
        :param limit: A integer to limit the number of objects
        :return: A netvis graph
    """

    graphs = [as_graph(x) for x in qs[:limit]]
    graph = {
        'edges': []
    }
    nodes = []
    for x in graphs:
        for node in x['nodes']:
            nodes.append(node)
        for edge in x['edges']:
            graph['edges'].append(edge)
    graph['nodes'] = list({v['id']: v for v in nodes}.values())
    graph['types'] = graphs[0]['types']
    return graph
