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


Installation
------------

    pip install opensearch-dsl


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
