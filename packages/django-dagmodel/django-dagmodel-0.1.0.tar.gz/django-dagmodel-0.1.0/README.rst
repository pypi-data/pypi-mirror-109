===============
django-dagmodel
===============


.. image:: https://img.shields.io/pypi/v/dag.svg
        :target: https://pypi.python.org/pypi/django-dagmodel

DAG in django


* Free software: MIT license
* Documentation: https://dag.readthedocs.io.


Installation
---------------

.. code-block:: sh

   $ pip install django-dagmodel

or

.. code-block:: sh

   $ python setup install

Usage
----------------

.. code-block:: python

   from dag import with_dag_node, with_dag_edge, with_dag


   class MyJob(model.Model):
       name = models.CharField(max_length=20)


   class MyNode(with_dag_node('MyEdge', 'MyDag')):
       name = models.CharField(max_length=10, unique=True)

       def __str__(self):
           return self.name


   class MyEdge(with_dag_edge(MyNode)):
       def __str__(self):
           return f"{self.prev_node} -> {self.next_node}"

       def __repr__(self):
           return f"{self.prev_node} -> {self.next_node}"


   class MyDag(with_dag(MyJob, 'MyEdge')): ...

   >>> job = TestJob.objects.create(name='myjob')
   >>> dag = MyDag.objects.create(job=job)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
