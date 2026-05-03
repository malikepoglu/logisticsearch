# TODO: Source Seed Planner / Worker

## English

### Current status

The 25-language canonical taxonomy JSON is ready with 337 records per language and 8,425 total records.

The taxonomy JSON bridge importer is sealed under the hierarchical webcrawler lib surface.

The next strategic direction is multilingual startpoint/source/seed planning for crawler_core.

### Ordered TODO

| Order | Task | Status |
|---:|---|---|
| 1 | Seal `source_seed_` naming rule in canonical documentation. | DONE_BY_THIS_DOC_SET |
| 2 | Seal `_planner` and `_worker` separation rule. | DONE_BY_THIS_DOC_SET |
| 3 | Keep all webcrawler phase-1 Python modules under hierarchical `python_live_runtime`. | ACTIVE_RULE |
| 4 | Define 25-language source/startpoint/seed matrix contract. | PLANNED |
| 5 | Define planner dry-run output files. | PLANNED |
| 6 | Create `logisticsearch1_1_0_2_multilingual_startpoint_seed_planner.py`. | PLANNED |
| 7 | Run planner validate-only audit. | PLANNED |
| 8 | Write source seed planner runbook. | PLANNED |
| 9 | Create worker only after planner dry-run PASS and runbook seal. | DEFERRED |
| 10 | Connect source seed output to crawler_core only after controlled audit. | DEFERRED |

### Planned Python modules

| Order | Module | Timing |
|---:|---|---|
| 1 | `logisticsearch1_1_0_1_startpoint_catalog_runtime.py` | Already exists. |
| 2 | `logisticsearch1_1_0_2_multilingual_startpoint_seed_planner.py` | Next implementation candidate after documentation seal. |
| 3 | `logisticsearch1_1_0_3_multilingual_startpoint_seed_worker.py` | Deferred until planner and runbook are sealed. |

### Hard safety rules

- Do not create the worker before the planner is proven.
- Do not write frontier rows from the planner.
- Do not touch Pi51c during design/doc/planner dry-run steps.
- Do not create DB or run SQL during planner design.
- Do not split one host into many top-level source families just because language/country paths differ.
- Do not bypass GitHub documentation and runbook discipline.

## Türkçe

### Mevcut durum

25 dilli canonical taxonomy JSON hazırdır: her dilde 337 kayıt, toplam 8.425 kayıt.

Taxonomy JSON bridge importer hiyerarşik webcrawler lib yüzeyi altında mühürlenmiştir.

Sıradaki stratejik yön crawler_core için çok dilli startpoint/source/seed planlamasıdır.

### Sıralı TODO

| Sıra | Görev | Durum |
|---:|---|---|
| 1 | `source_seed_` isimlendirme kuralını canonical dokümana yaz. | DONE_BY_THIS_DOC_SET |
| 2 | `_planner` ve `_worker` ayrımını mühürle. | DONE_BY_THIS_DOC_SET |
| 3 | Tüm webcrawler faz-1 Python modüllerini hiyerarşik `python_live_runtime` altında tut. | ACTIVE_RULE |
| 4 | 25 dilli source/startpoint/seed matrix contract tanımla. | PLANNED |
| 5 | Planner dry-run çıktı dosyalarını tanımla. | PLANNED |
| 6 | `logisticsearch1_1_0_2_multilingual_startpoint_seed_planner.py` oluştur. | PLANNED |
| 7 | Planner validate-only audit çalıştır. | PLANNED |
| 8 | Source seed planner runbook yaz. | PLANNED |
| 9 | Worker’ı sadece planner dry-run PASS ve runbook seal sonrası oluştur. | DEFERRED |
| 10 | Source seed çıktısını crawler_core’a sadece kontrollü audit sonrası bağla. | DEFERRED |

### Planlanan Python modülleri

| Sıra | Modül | Zamanlama |
|---:|---|---|
| 1 | `logisticsearch1_1_0_1_startpoint_catalog_runtime.py` | Zaten var. |
| 2 | `logisticsearch1_1_0_2_multilingual_startpoint_seed_planner.py` | Dokümantasyon seal sonrası sıradaki implementation adayı. |
| 3 | `logisticsearch1_1_0_3_multilingual_startpoint_seed_worker.py` | Planner ve runbook mühürlenene kadar ertelendi. |

### Sert güvenlik kuralları

- Planner kanıtlanmadan worker oluşturma.
- Planner içinden frontier satırı yazma.
- Design/doc/planner dry-run adımlarında Pi51c’ye dokunma.
- Planner design sırasında DB yaratma veya SQL çalıştırma.
- Bir host’u sadece dil/ülke path’i farklı diye birçok top-level source family’ye bölme.
- GitHub dokümantasyon ve runbook disiplinini atlama.
