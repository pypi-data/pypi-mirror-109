#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Distributed under terms of the MIT license.


import itertools
from collections import deque
from typing import *

from django.apps import apps
from django.db import models

from .exceptions import DAGCircleError


def get_model(model, app_label):
    if isinstance(model, str):
        model_cls = apps.get_model(app_label=app_label, model_name=model)
    else:
        model_cls = model

    return model_cls


class Node(models.Model):
    class Meta:
        abstract = True


def with_dag_edge(node_model):
    class DAGEdge(models.Model):
        class Meta:
            abstract = True

        prev_node = models.ForeignKey(node_model, related_name="edges", on_delete=models.CASCADE)
        next_node = models.ForeignKey(node_model, related_name="+", on_delete=models.CASCADE)

        def __str__(self):
            return f"{self.prev_node} -> {self.next_node}"

        def save(self, *args, **kwargs):
            if self.prev_node == self.next_node:
                raise DAGCircleError(f"self link is not allowed for {self}")

            if self.next_node in self.prev_node.all_upstreams:
                raise DAGCircleError(f"detect circle exists for {self}")
            super().save(*args, **kwargs)

    return DAGEdge


def with_dag_node(edge_model, dag_model, app_label=None):
    class DAGNode(Node):
        class Meta:
            abstract = True

        downstreams = models.ManyToManyField(
            'self',
            blank=True,
            symmetrical=False,
            through=edge_model,
            related_name='upstreams')

        dag = models.ForeignKey(dag_model, related_name='nodes', on_delete=models.CASCADE)

        def __str__(self):
            raise NotImplementedError

        @property
        def in_degree(self):
            return len(self.upstreams.all())

        @property
        def out_degree(self):
            return len(self.downstreams.all())

        @property
        def all_downstreams(self):
            nodes = [self]
            nodes_seen = set()
            i = 0

            while i < len(nodes):
                downstream_nodes = nodes[i].downstreams.all()
                for next_node in downstream_nodes:
                    if next_node not in nodes_seen:
                        nodes_seen.add(next_node)
                        nodes.append(next_node)
                i += 1

            return nodes_seen

        @property
        def all_upstreams(self):
            nodes = [self]
            nodes_seen = set()
            i = 0

            while i < len(nodes):
                upstream_nodes = nodes[i].upstreams.all()
                for next_node in upstream_nodes:
                    if next_node not in nodes_seen:
                        nodes_seen.add(next_node)
                        nodes.append(next_node)
                i += 1

            return nodes_seen

        def connect_to(self, node):
            app_label_name = app_label or self._meta.app_label
            model = get_model(edge_model, app_label_name)
            model.add_edge(self, node)

    return DAGNode


def with_dag(job_model, edge_model, app_label=None):
    class DAG(models.Model):
        class Meta:
            abstract = True

        job = models.OneToOneField(job_model, related_name='dag', on_delete=models.CASCADE, auto_created=True)

        @property
        def circles(self):
            def explore(edge, visited, exploring, find_circles):
                exploring.append(edge)
                visited.add(edge)
                for next_edge in edge.next_node.edges.all():
                    if next_edge not in visited or next_edge not in exploring:
                        explore(next_edge, visited, exploring, find_circles)
                    elif next_edge in exploring:
                        circle = [next_edge]
                        explored = exploring.copy()
                        explore_edge = explored.pop()
                        while explore_edge != next_edge:
                            circle.append(explore_edge)
                            explore_edge = explored.pop()
                        circle.reverse()
                        if circle not in find_circles:
                            find_circles.append(circle)

                exploring.remove(edge)

            graph_circles = []
            visited = set()
            exploring = []

            for node in self.nodes.all():
                for edge in node.edges.all():
                    if edge not in visited:
                        explore(edge, visited, exploring, graph_circles)

            return graph_circles

        def add_edge(self, from_node, to_node):
            app_label_name = app_label or self._meta.app_label
            model = get_model(edge_model, app_label_name)
            model.objects.create(prev_node=from_node, next_node=to_node)

        def add_edges(self, from_node, to_node, *to_nodes):
            for next_node in itertools.chain((to_node,), to_nodes):
                self.add_edge(from_node, next_node)

        def add_edges_from(self, edges: List[Tuple[Node, Node]]):
            for edge in edges:
                self.add_edge(*edge)

        def get_zero_in_degree_nodes(self):
            for node in self.nodes.all():
                if node.in_degree == 0:
                    yield node

        def get_zero_out_degree_nodes(self):
            for node in self.nodes.all():
                if node.out_degree == 0:
                    yield node

        def get_task_flows_display(self):
            flows = []
            node_out_degrees = {}

            for node in self.nodes.all():
                node_out_degrees[node] = node.out_degree

            visted = set()
            while len(visted) != len(node_out_degrees):
                flow = []
                for node, out_degree in node_out_degrees.items():
                    if out_degree == 0 and node not in visted:
                        flow.append(node)
                        visted.add(node)
                for node in flow:
                    for upstream_node in node.upstreams.all():
                        node_out_degrees[upstream_node] -= 1
                flows.append(flow)
            return flows

        def is_directed_acyclic_graph(self):
            try:
                self.topological_sort()
            except DAGCircleError:
                return False
            return True

        def topological_sort(self):
            ret = []
            queue = deque()
            node_in_degrees = {}
            dag_size = 0
            for node in self.nodes.all():
                node_in_degrees[node] = node.in_degree
                dag_size += 1

            for node in self.nodes.all():
                if node.in_degree == 0:
                    queue.appendleft(node)

            while queue:
                node = queue.pop()
                ret.append(node)
                for downstream_node in node.downstreams.all():
                    node_in_degrees[downstream_node] -= 1
                    if node_in_degrees[downstream_node] == 0:
                        queue.appendleft(downstream_node)

            if len(ret) != dag_size:
                raise DAGCircleError(message=f"circle exists: {self.circles}")

            return ret

    return DAG
