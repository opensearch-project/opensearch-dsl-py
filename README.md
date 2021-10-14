[![CI](https://github.com/opensearch-project/opensearch-dsl-py/actions/workflows/ci.yml/badge.svg)](https://github.com/opensearch-project/opensearch-dsl-py/actions/workflows/ci.yml)
[![Integration](https://github.com/opensearch-project/opensearch-dsl-py/actions/workflows/integration.yml/badge.svg)](https://github.com/opensearch-project/opensearch-dsl-py/actions/workflows/integration.yml)
[![Chat](https://img.shields.io/badge/chat-on%20forums-blue)](https://discuss.opendistrocommunity.dev/c/clients/)
![PRs welcome!](https://img.shields.io/badge/PRs-welcome!-success)

![OpenSearch logo](OpenSearch.svg)

OpenSearch DSL Python Client

- [Welcome!](#welcome)
- [Project Resources](#project-resources)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Copyright](#copyright)

## Welcome!

**opensearch-dsl-py** is [a community-driven, open source fork](https://aws.amazon.com/blogs/opensource/introducing-opensearch/) of elasticsearch-dsl-py licensed under the [Apache v2.0 License](LICENSE.txt). For more information, see [opensearch.org](https://opensearch.org/).

OpenSearch DSL is a high-level library whose aim is to help with writing and
running queries against OpenSearch. It is built on top of the official
low-level client (`opensearch-py <https://github.com/opensearch-project/opensearch-py>`_).

It provides a more convenient and idiomatic way to write and manipulate
queries. It stays close to the OpenSearch JSON DSL, mirroring its
terminology and structure. It exposes the whole range of the DSL from Python
either directly using defined classes or a queryset-like expressions.

It also provides an optional wrapper for working with documents as Python
objects: defining mappings, retrieving and saving documents, wrapping the
document data in user-defined classes.

To use the other OpenSearch APIs (eg. cluster health) just use the
underlying client.

Installation
------------

pip install opensearch-dsl


Compatibility
-------------

The library is compatible with all OpenSearch versions since ``1.x`` but you
**have to use a matching major version**:

For **OpenSearch 1.0** and later, use the major version 1 (``1.x.y``) of the
library.


The recommended way to set your requirements in your `setup.py` or
`requirements.txt` is::

    # OpenSearch 1.x
    opensearch-dsl>=1.0.0,<2.0.0


The development is happening on ``master``, older branches only get bugfix releases


Sample Code
-----------
    from opensearchpy import OpenSearch
    from opensearch_dsl import Search

    host = 'localhost'
    port = 9200
    auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
    ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

    # Optional client certificates if you don't want to use HTTP basic authentication.
    # client_cert_path = '/full/path/to/client.pem'
    # client_key_path = '/full/path/to/client-key.pem'

    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        # client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl = True,
        verify_certs = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
        ca_certs = ca_certs_path
    )

    index_name = 'my-dsl-index'

    response = client.indices.create(index_name)
    print('\nCreating index:')
    print(response)

    # Add a document to the index.
    document = {
      'title': 'python',
      'description': 'beta',
      'category': 'search'
    }
    id = '1'

    response = client.index(
        index = index_name,
        body = document,
        id = id,
        refresh = True
    )

    print('\nAdding document:')
    print(response)

    # Search for the document.
    s = Search(using=client, index=index_name) \
        .filter("term", category="search") \
        .query("match", title="python")

    response = s.execute()

    print('\nSearch results:')
    for hit in response:
        print(hit.meta.score, hit.title)

    # Delete the document.
    print('\nDeleting document:')
    print(response)

    # Delete the index.
    response = client.indices.delete(
        index = index_name
    )

    print('\nDeleting index:')
    print(response)


Search Example
--------------

Let's have a typical search request written directly as a ``dict``:

.. code:: python

    from opensearchpy import OpenSearch
    client = OpenSearch()

    response = client.search(
        index="my-index",
        body={
          "query": {
            "bool": {
              "must": [{"match": {"title": "python"}}],
              "must_not": [{"match": {"description": "beta"}}],
              "filter": [{"term": {"category": "search"}}]
            }
          },
          "aggs" : {
            "per_tag": {
              "terms": {"field": "tags"},
              "aggs": {
                "max_lines": {"max": {"field": "lines"}}
              }
            }
          }
        }
    )

    for hit in response['hits']['hits']:
        print(hit['_score'], hit['_source']['title'])

    for tag in response['aggregations']['per_tag']['buckets']:
        print(tag['key'], tag['max_lines']['value'])



The problem with this approach is that it is very verbose, prone to syntax
mistakes like incorrect nesting, hard to modify (eg. adding another filter) and
definitely not fun to write.

Let's rewrite the example using the Python DSL:

.. code:: python

    from opensearchpy import OpenSearch
    from opensearch_dsl import Search

    client = OpenSearch()

    s = Search(using=client, index="my-index") \
        .filter("term", category="search") \
        .query("match", title="python")   \
        .exclude("match", description="beta")

    s.aggs.bucket('per_tag', 'terms', field='tags') \
        .metric('max_lines', 'max', field='lines')

    response = s.execute()

    for hit in response:
        print(hit.meta.score, hit.title)

    for tag in response.aggregations.per_tag.buckets:
        print(tag.key, tag.max_lines.value)

As you see, the library took care of:

  * creating appropriate ``Query`` objects by name (eq. "match")

  * composing queries into a compound ``bool`` query

  * putting the ``term`` query in a filter context of the ``bool`` query

  * providing a convenient access to response data

  * no curly or square brackets everywhere


Persistence Example
-------------------

Let's have a simple Python class representing an article in a blogging system:

.. code:: python

    from datetime import datetime
    from opensearch_dsl import Document, Date, Integer, Keyword, Text, connections

    # Define a default OpenSearch client
    connections.create_connection(hosts=['localhost'])

    class Article(Document):
        title = Text(analyzer='snowball', fields={'raw': Keyword()})
        body = Text(analyzer='snowball')
        tags = Keyword()
        published_from = Date()
        lines = Integer()

        class Index:
            name = 'blog'
            settings = {
              "number_of_shards": 2,
            }

        def save(self, ** kwargs):
            self.lines = len(self.body.split())
            return super(Article, self).save(** kwargs)

        def is_published(self):
            return datetime.now() > self.published_from

    # create the mappings in opensearch
    Article.init()

    # create and save and article
    article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
    article.body = ''' looong text '''
    article.published_from = datetime.now()
    article.save()

    article = Article.get(id=42)
    print(article.is_published())

    # Display cluster health
    print(connections.get_connection().cluster.health())


In this example you can see:

  * providing a default connection

  * defining fields with mapping configuration

  * setting index name

  * defining custom methods

  * overriding the built-in ``.save()`` method to hook into the persistence
    life cycle

  * retrieving and saving the object into OpenSearch

  * accessing the underlying client for other APIs

You can see more in the persistence chapter of the documentation.

Migration from ``opensearch-py``
-----------------------------------

You don't have to port your entire application to get the benefits of the
Python DSL, you can start gradually by creating a ``Search`` object from your
existing ``dict``, modifying it using the API and serializing it back to a
``dict``:

.. code:: python

    body = {...} # insert complicated query here

    # Convert to Search object
    s = Search.from_dict(body)

    # Add some filters, aggregations, queries, ...
    s.filter("term", tags="python")

    # Convert back to dict to plug back into existing code
    body = s.to_dict()

Development
-----------

Activate Virtual Environment (`virtualenvs <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_):

.. code:: bash

    $ virtualenv venv
    $ source venv/bin/activate

To install all of the dependencies necessary for development, run:

.. code:: bash

    $ pip install -e '.[develop]'

To run all of the tests for ``opensearch-dsl-py``, run:

.. code:: bash

    $ python setup.py test

Alternatively, it is possible to use the ``run_tests.py`` script in
``test_opensearch_dsl``, which wraps `pytest
<http://doc.pytest.org/en/latest/>`_, to run subsets of the test suite. Some
examples can be seen below:

.. code:: bash

    # Run all of the tests in `test_opensearch_dsl/test_analysis.py`
    $ ./run_tests.py test_analysis.py

    # Run only the `test_analyzer_serializes_as_name` test.
    $ ./run_tests.py test_analysis.py::test_analyzer_serializes_as_name

``pytest`` will skip tests from ``test_opensearch_dsl/test_integration``
unless there is an instance of OpenSearch on which a connection can occur.
By default, the test connection is attempted at ``localhost:9200``, based on
the defaults specified in the ``opensearch-py`` `Connection
<https://github.com/opensearch-project/opensearch-py/tree/main/opensearchpy
/connection/base.py#L29>`_ class. **Because running the integration
tests will cause destructive changes to the OpenSearch cluster, only run
them when the associated cluster is empty.** As such, if the
OpenSearch instance at ``localhost:9200`` does not meet these requirements,
it is possible to specify a different test OpenSearch server through the
``TEST_OPENSEARCH_SERVER`` environment variable.

.. code:: bash

    $ TEST_OPENSEARCH_SERVER=my-test-server:9201 ./run_tests

## Project Resources

* [Project Website](https://opensearch.org/)
* [Downloads](https://opensearch.org/downloads.html).
* [Documentation](https://opensearch.org/docs/)
* Need help? Try [Forums](https://discuss.opendistrocommunity.dev/)
* [Project Principles](https://opensearch.org/#principles)
* [Contributing to OpenSearch](CONTRIBUTING.md)
* [Maintainer Responsibilities](MAINTAINERS.md)
* [Release Management](RELEASING.md)
* [Admin Responsibilities](ADMINS.md)
* [Security](SECURITY.md)

## Code of Conduct

This project has adopted the [Amazon Open Source Code of Conduct](CODE_OF_CONDUCT.md). For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq), or contact [opensource-codeofconduct@amazon.com](mailto:opensource-codeofconduct@amazon.com) with any additional questions or comments.

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright 2020-2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
