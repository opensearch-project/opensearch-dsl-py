- [Compatibility with OpenSearch](#compatibility-with-opensearch)
- [Upgrading](#upgrading)

## Compatibility with OpenSearch

The below matrix shows the compatibility of the [`opensearch-dsl-py-client`](https://pypi.org/project/opensearch-dsl/) with versions of [`OpenSearch`](https://opensearch.org/downloads.html#opensearch).

| OpenSearch Version | Client Version |
| --- | --- |
| 1.0.0 | 1.0.0 |
| 1.0.1 | 1.0.0 |
| 1.1.0 | 1.0.0 |
| 1.2.0 | 1.0.0 |
| 1.2.1 | 1.0.0 |
| 1.2.2 | 1.0.0 |
| 1.2.3 | 1.0.0 |
| 1.2.4 | 1.0.0 |
| 1.3.0 | 1.0.0 |
| 1.3.1 | 1.0.0 |
| 1.3.2 | 1.0.0 |
| 1.3.3 | 1.0.0 |
| 2.0.0 | 2.0.1 |
| 2.0.1 | 2.0.1 |

## Upgrading

Major versions of OpenSearch introduce breaking changes that require careful upgrades of the client. While `opensearch-dsl-py-client` 2.0.1 works against the latest OpenSearch 1.x, certain deprecated features removed in OpenSearch 2.0 have also been removed from the client. Please refer to the [OpenSearch documentation](https://opensearch.org/docs/latest/clients/index/) for more information.