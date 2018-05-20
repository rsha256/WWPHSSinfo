from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from info import models


@login_required
def graph_post(request):
    if request.method == "POST":
        post_dict = dict(request.POST)

        graph = models.Graph()
        graph.title = str(post_dict['title'][0])
        graph.save()

        graph_data = []
        names = post_dict["names[]"]
        values = post_dict["values[]"]
        colors = post_dict["colors[]"]

        for i in range(0, len(names)):
            if names[i] is not '':
                graph_data.append({"order": i, "name": names[i], "value": values[i], "color": colors[i]})

        for d in graph_data:
            entry = models.GraphEntry()
            entry.graph = graph
            entry.name = d['name']
            entry.value = float(d['value'])
            entry.color = str(d['color'])
            entry.save()

    return redirect("/staff")


@login_required
def graph_delete(request):
    if request.method == "POST":
        models.Graph.objects.all().delete()

    return redirect("/staff")


def graph_get():
    graph = models.Graph.objects.all()
    entries = []

    if graph:
        graph = graph[0]
        entries = models.GraphEntry.objects.filter(graph=graph)

    return {
        "graph": graph,
        "entries": entries,
    }

