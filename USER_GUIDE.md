- [User Guide](#user-guide)
  - [Setup](#setup)
  - [Sample code](#sample-code)
  - [AWS Sigv4 Request Signer Sample Code](#aws-sigv4-request-signer-sample-code)
# User Guide

This user guide specifies how to include and use the dsl-py client in your application.

## Setup

To add the client to your project, install it using [pip](https://pip.pypa.io/):

```bash
pip install opensearch-dsl
```

Then import it like any other module:

```python
from opensearchpy import OpenSearch
    from opensearch_dsl import Search
```

If you prefer to add the client manually or just want to examine the source code, see [opensearch-dsl-py on GitHub](https://github.com/opensearch-project/opensearch-dsl-py).


## Sample code

```python
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
```

## AWS Sigv4 Request Signer Sample Code
```
from opensearch_dsl import Search
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import botocore
import boto3
import os

# cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
host = os.getenv('host')
region = 'us-west-2' # e.g. us-west-1

# create credential from access_key and secret_key
credentials = botocore.credentials.Credentials(
    access_key=os.getenv('access_key'),
    secret_key=os.getenv('secret_key')
)

auth = AWSV4SignerAuth(credentials, region)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
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
```
