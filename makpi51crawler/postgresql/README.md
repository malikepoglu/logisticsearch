# PostgreSQL JSON Runtime Topology / PostgreSQL JSON Runtime Topolojisi

EN: PostgreSQL is the runtime authority. JSON and JSONB are the controlled representation layer.
TR: PostgreSQL runtime otoritesidir. JSON ve JSONB kontrollü temsil katmanıdır.

EN: Do not recreate top-level sql/ or makpi51crawler/sql/.
TR: top-level sql/ veya makpi51crawler/sql/ tekrar oluşturulmaz.

Current topology:

```text
makpi51crawler/postgresql/
  README.md
  schemas/
    postgresql_runtime_manifest.v1.schema.json
  databases/
    crawler_core/
      README.md
      raw_fetch/
        README.md
        frontier_queue.v1.json
        http_raw_capture.v1.json
```
