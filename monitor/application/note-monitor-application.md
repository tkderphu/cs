# Monitor
Monitoring is the process of collecting, analyzing, and visualizing data to understand how a system (like an application, server, or network) is performing over time.

It's like installing sensors in your system that tell you:

- Is everything working?

- How fast is it?

- Are there errors?

- Is something unusual happening?

# Monitoring Components

## 1. Metrics

- Definition: Numerical data collected at intervals (time-series)

- Examples:

    - CPU usage: 75%

    - Response time: 300ms

    - Requests per second: 120

- Tools: Prometheus(common), Datadog, InfluxDB

## 2. Logs

- Definition: Text-based records of events that happen in your system

- Examples:

    - 2025-07-04 12:00:00 ERROR OrderService - NullPointerException

    - User 'john_doe' logged in

- Tools: Loki, ELK Stack (Elasticsearch + Logstash + Kibana), Graylog

## 3. Traces

- Definition: Step-by-step journey of a single request through your app (used in distributed systems)

- Example:

    - Trace of an HTTP request from API gateway → auth service → order service → payment service

- Tools: Zipkin, Jaeger, Tempo, OpenTelemetry
## 4. Dashboards

- Definition: Visual UI showing system health

- Use: Combine metrics, logs, and traces in real-time

- Tools: Grafana, Kibana, Datadog

## 5. Alerts

- Definition: Notifications triggered when things go wrong

- Examples:

    - Send Slack message when CPU > 90% for 5 minutes

    - Email when /checkout endpoint has > 5% errors

    - Tools: Grafana Alerting, Prometheus Alertmanager, Opsgenie, PagerDuty


# Observability
Observability is the ability to understand what is happening inside a system by looking at its outputs — such as logs, metrics, and traces.

It's not just about knowing that something is broken — it's about knowing why it's broken and where to look to fix it.

```
Observability = Monitoring + Debugging Insight
```
# The 3 Pillars of Observability

| Pillar      | Description                           | Example                                                   |
| ----------- | ------------------------------------- | --------------------------------------------------------- |
| **Metrics** | Numeric data over time                | CPU usage, request count, error rate                      |
| **Logs**    | Text records of events                | `2025-07-04 12:30:45 ERROR: NullPointerException`         |
| **Traces**  | A map of a request through the system | A trace showing how a request flows through microservices |

# Observability vs Monitoring

| Feature       | Monitoring                 | Observability                                     |
| ------------- | -------------------------- | ------------------------------------------------- |
| **Purpose**   | Tell if something is wrong | Help understand why it's wrong                    |
| **Data Used** | Mostly metrics             | Metrics + logs + traces                           |
| **Scope**     | Reactive (alerts)          | Proactive & investigative                         |
| **Example**   | “Error rate is 5%”         | “Why is the error rate high? Trace this request.” |

Monitoring tells you:
- "This service is slow."

Observability tells you:

- "Here’s the exact request causing the slowdown, and where it’s spending time."

# Prometheus

Prometheus is an open-source metrics-based monitoring and alerting toolkit originally developed at SoundCloud. It works by scraping metrics from configured endpoints and storing them in a time-series database.

# Core concept of prometheus

1. Metrics

2. Scraping

    - Prometheus fetches metrics by pulling(HTTP GET) from a <strong>/metrics</strong> endpoint

3. Target

    - A server or app exposing metrics in Prometheus format

4. Job

    - A group of targets(e.g., all instances of a service)

5. Alerting

    - Prometheus can evaluate rules and send alerts via Alertmanager

6. Querying

    - Uses PromQL to analyze data

7. Retention

    - Stores data in a local time-series DB

# Prometheus Architecture

```
        +--------------+
        |  Web UI      |
        |  API/PromQL  |
        +------+-------+
               |
               v
     +----------------------+
     |   Prometheus Server  |
     +----------+-----------+
                |
      +---------+---------+
      |                   |
+------------+   +----------------+
| /metrics   |   | /metrics       |
| Spring App |   | Node Exporter  |
+------------+   +----------------+
```

# Data storeed in Prometheus

# Grafana


Grafana is an open-source analytics and visualization platform that allows you to query, visualize, and understand data from various sources in real time. It’s commonly used for monitoring infrastructure, applications, and network systems by creating dynamic dashboards with charts, graphs, and alerts.

# Key Features of Grafana:

- Data Visualization

  - Create interactive and customizable dashboards with panels like graphs, tables, heatmaps, and more.

- Data Source Agnostic

  - Supports many backends: Prometheus, InfluxDB, Graphite, MySQL, PostgreSQL, Loki, Elasticsearch, AWS CloudWatch, and many others.

- Alerting

  - Set up alerts with thresholds, and get notified via email, Slack, PagerDuty, Microsoft Teams, etc.

- Templating

  - Use variables to make dashboards reusable and dynamic.

- Plugins and Extensions

  - Extend functionality using official and community-built plugins (e.g., panel types, new data sources).

- User Management

  - Role-based access control and authentication via LDAP, OAuth, etc.

- Dashboard Sharing

  - Share dashboards via links or snapshots (static or live).

# How grafana work

 1. Connect to Data Sources
    - Grafana supports many data sources like:

      - Time-series databases: Prometheus, InfluxDB, Graphite

      - SQL databases: MySQL, PostgreSQL, MSSQL

      - Cloud services: AWS CloudWatch, Google Cloud Monitoring

      - Log tools: Loki, Elasticsearch

    - You configure data sources through the Grafana UI. Grafana doesn’t store data itself—it queries the data live.

2. Query the Data
    
    - Once the data source is connected, you build queries to fetch the data you want.

    - Grafana provides query editors specific to each data source.

    - Queries can be written using PromQL (Prometheus), InfluxQL/Flux (InfluxDB), or SQL (for relational databases).

    - You can use filters, functions, and time ranges (e.g., “last 1 hour”).

3. Visualize with Dashboards
    -  Data is shown using panels—each panel is a visual element like:

      - Line chart

      - Gauge

      - Table

      - Bar chart

      - Heatmap

      - Logs viewer

      - Panels can be arranged into dashboards, which can be saved, reused, and shared.

4. Set Up Alerts (Optional)

    - Grafana lets you define alert rules based on your data:

        - For example: “Trigger alert if CPU usage > 90% for 5 minutes”

    - Alerts can be sent to:

      - Email

      - Slack

      - Microsoft Teams

      - PagerDuty

      - Webhooks

5. Extend with Plugins (Optional)

    - You can add:

      - New panel types

      - New data source integrations

      - App plugins (prepackaged dashboards + data sources)

## Example Use Case: Monitoring Servers with Prometheus

1. Install Prometheus to collect server metrics.

2. Set up Grafana and connect it to Prometheus.

3. Create a dashboard with a panel that queries CPU usage.

4. Visualize CPU over time as a line chart.

5. Set an alert if CPU > 80%.


# Grafana Loki

Grafana Loki is a log aggregation system inspired by Prometheus, developed by Grafana Labs. It’s designed for efficient, cost-effective logging, particularly in cloud-native environments like Kubernetes.

# Key Principles of Loki

| Feature                   | Description                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Index by Labels Only**  | Loki indexes logs using **labels** (e.g., `job`, `instance`, `pod`, `namespace`), rather than full-text search. This makes it **cheaper and faster** than systems like Elasticsearch. |
| **No Full-Text Indexing** | Instead of indexing log content, Loki stores it in chunks and **uses metadata labels** for querying.                                                                                  |
| **Works with Grafana**    | Tight integration with **Grafana** for powerful visualization and querying.                                                                                                           |
| **Cloud-Native Ready**    | Built for environments like **Kubernetes**, integrates with Prometheus labels, and works well with modern log shippers.                                                               |

# Core Components of Loki

1. Loki Server

    - The backend component that receives, stores, and serves logs.

    - Stores logs in chunks (usually in object storage like S3, GCS, etc.).

    - Indexes metadata like labels for fast retrieval.

2. Promtail (or alternatives like Fluent Bit)

    - Promtail is the default log shipper for Loki.

    - Installed as a DaemonSet in Kubernetes to collect logs from nodes/pods.

    - Parses logs and attaches labels based on the environment.

    - Alternatives: You can also use Fluent Bit, Fluentd, or Logstash to send logs to Loki.

3. Grafana
    - Loki is natively supported in Grafana.

    - Allows you to search logs using LogQL (a PromQL-inspired query language).

# LogQL – Loki’s Query Language

LogQL allows you to query logs using label selectors and filters.

## Examples

```
{job="nginx"}                                # Select logs from job "nginx"
{app="api"} |= "error"                       # Logs with "error" in them
{app="db"} |~ "timeout|failed"               # Regex match for multiple keywords
```

You can also compute metrics from logs:

```
rate({app="nginx"} |= "GET" [5m])            # Requests per second
count_over_time({level="error"}[1h])         # Count of errors in the past hour

```

# Loki Storage Architecture

| Layer            | Purpose                                                                |
| ---------------- | ---------------------------------------------------------------------- |
| **Ingester**     | Receives logs, buffers in memory, and writes chunks to storage.        |
| **Distributor**  | Accepts incoming logs, validates them, and sends them to the ingester. |
| **Querier**      | Handles queries from Grafana, fetches data from storage.               |
| **Index Store**  | Stores metadata (e.g., BoltDB, DynamoDB, Bigtable, or Cortex Index).   |
| **Object Store** | Stores actual log chunks (e.g., S3, GCS, Azure Blob).                  |

### Keyword

1. Buffer

A buffer is a temporary in-memory storage area where data is held before being processed or written to disk.
    
-  In Loki: When log data arrives at the ingester, it is not immediately written to storage. Instead, it is held in memory (RAM) in a buffer. This allows Loki to:

    - Collect more log lines to group together.

    - Reduce the number of small, inefficient writes to disk or cloud storage.

- Analogy:
Think of a buffer like a waiting room — logs come in and wait until there's enough of them to be processed together efficiently.

2. What is a Chunk?

A chunk is a block of log entries that have been collected and grouped together (from the buffer), and then stored as a unit.

- In Loki:
Logs in the buffer are grouped by stream (same set of labels).

- After a period of time (e.g., 2 minutes) or a size limit (e.g., 1MB), the buffered logs are cut into a "chunk".

- The chunk contains:

   -  All the log lines (with timestamps).

    - Metadata like the stream labels.

- The chunk is then compressed and written to object storage (like S3).

- Analogy:
A chunk is like a file folder full of related documents (log lines) that Loki archives together.


3. What is Compressed?

Compression reduces the size of data using algorithms (like Snappy, gzip, etc.), saving storage space and improving transfer speed.

- In Loki:
When a chunk is finalized, it is compressed before being saved to storage.

- This reduces:

    - The amount of disk or cloud storage used.

    - The network bandwidth required for retrieving logs during queries.

    - Loki supports efficient compression methods that balance speed and size.

- Analogy:
Think of compressing logs like vacuum-sealing food: it takes up less space but keeps the contents safe.


# How Loki Uses Object Storage 
### Write Flow:

1. Logs are ingested (via Promtail, Fluent Bit, etc.).

2. Logs are buffered in memory by the Ingester (per stream).

3. When the chunk size or time threshold is reached:

    - The ingester compresses the chunk.

    - The chunk is written to object storage (e.g., S3 bucket).

    - A reference to the chunk (along with label metadata and time range) is written to the index backend.

### Read Flow (Querying Logs):
1. A query is sent via Grafana or the Loki API.

2. Loki uses the index backend to find which chunks match the query.

3. Loki fetches the matching compressed chunks from object storage.

4. Chunks are decompressed, filtered, and returned.

```
Grafana (User Query)
     ↓
+--------------+
|   Querier    | ←────────────┐
+--------------+              │
     ↓                       │
 Index Store (e.g. BoltDB, DynamoDB)
     ↓
[chunk references + time ranges]
     ↓
Object Store (S3, GCS, etc.)
     ↓
[compressed chunks → decompressed]
     ↓
Querier filters results
     ↓
Grafana displays logs

```

## Example of What the Index Might Contain:

Imagine this metadata stored in the index:

```
| Stream Labels                  | Chunk ID       | Time Range      | Chunk Path                                |
| ------------------------------ | -------------- | --------------- | ----------------------------------------- |
| `{job="nginx"}`                | `chunk-abc123` | `10:00 → 10:05` | `s3://bucket/loki/chunks/01/abc123.chunk` |
| `{job="nginx", level="error"}` | `chunk-def456` | `10:03 → 10:08` | `s3://bucket/loki/chunks/01/def456.chunk` |

```

So when your query is {job="nginx"} from 10:02 to 10:06:

- Both chunks will be fetched and processed.


✅ 1. Time Series
The fundamental unit stored is a time series, which consists of:

A metric name (e.g. http_requests_total)

A set of labels (e.g. {method="GET", status="200"})

A series of timestamped values (i.e. samples)

Example of a time series stored:

text
Sao chép mã
metric name: http_requests_total
labels: {method="GET", status="200", instance="app1", job="spring-app"}
samples:
  [timestamp: 1657012345, value: 1234]
  [timestamp: 1657012400, value: 1250]
  ...
✅ 2. Sample Data
Each sample in a time series includes:

A float64 value (the actual metric value)

A timestamp in milliseconds (when the sample was scraped)

Prometheus does not store raw logs or trace data — only numerical samples over time.

✅ 3. Metadata (optional)
Prometheus also stores some metadata like:

Metric type (counter, gauge, histogram, summary)

HELP description (if provided by the exporter)

Unit (e.g., seconds, bytes)

Example:

bash
Sao chép mã
# HELP http_requests_total The total number of HTTP requests
# TYPE http_requests_total counter
This metadata is useful for UI and querying but not stored in the same way as raw samples.

✅ 4. Label Indexes
Prometheus creates indexes on labels to efficiently query time series using PromQL.

For example, if you query:

promql
Sao chép mã
rate(http_requests_total{status="500"}[5m])
Prometheus uses an internal label index to quickly find all matching series.

🗄️ How Prometheus stores data on disk
Prometheus stores data on disk in its own custom format:

TSDB (Time Series DB): located in data/ directory (default)

Structure:

perl
Sao chép mã
data/
  wal/           # write-ahead log (recent, not yet compacted)
  chunks/        # compressed block data
  index/         # label index
Retention period: default is 15 days (configurable with --storage.tsdb.retention.time)

🛠️ Prometheus does NOT store:
Full logs

Raw application traces

Non-numeric data

High-cardinality unbounded labels (bad practice)

 Sample Query Example
If your app exposes:

text
Sao chép mã
http_requests_total{method="POST", status="500"}
Prometheus will store:

json
Sao chép mã
{
  "metric": "http_requests_total",
  "labels": {
    "method": "POST",
    "status": "500",
    "instance": "localhost:8080",
    "job": "spring-app"
  },
  "values": [
    [timestamp1, 10],
    [timestamp2, 11],
    [timestamp3, 15],
    ...
  ]
}
✅ Summary
Data Type	Stored in Prometheus?	Notes
Time series	✅ Yes	Core format: metric + labels + samples
Timestamps	✅ Yes	All metrics are time-stamped
Logs	❌ No	Use a log system like Loki, ELK
Traces	❌ No	Use tracing systems like Jaeger, Zipkin
Labels/Tags	✅ Yes	Used for filtering and grouping
Metric metadata	✅ Yes (limited)	HELP and TYPE sections from /metrics