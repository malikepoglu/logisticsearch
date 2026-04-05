# Pi51 Export Source

## Overview

**Pi51 Export Source** is the producer-scoped subtree for crawler export material that originates from the Pi51 crawler node and is intentionally promoted into the canonical LogisticSearch repository flow. This subtree exists to separate source identity clearly: it shows that the export artifacts below it belong to the Pi51-origin crawler path, not to a generic or mixed producer pool.

## Genel Bakış

**Pi51 Export Source**, Pi51 crawler düğümünden üretilen ve kanonik LogisticSearch repository akışına bilinçli olarak alınan export materyalleri için üretici-kapsamlı alt ağaçtır. Bu alt ağaç, kaynak kimliğini açıkça ayırmak için vardır: altındaki export artefact’larının genel veya karışık bir üretici havuzuna değil, Pi51 kökenli crawler yoluna ait olduğunu gösterir.
## Purpose

This subtree provides a clean source boundary inside `crawler_exports/`. Its role is to group together all repository-worthy export channels that originate from Pi51, so that downstream consumers can understand the producer context without depending on hidden operational assumptions.

## Amaç

Bu alt ağaç, `crawler_exports/` içinde temiz bir kaynak sınırı sağlar. Rolü; Pi51’den gelen ve repository’ye girmeye değer tüm export kanallarını bir arada tutarak, aşağı akıştaki tüketicilerin üretici bağlamını gizli operasyon varsayımlarına ihtiyaç duymadan anlayabilmesini sağlamaktır.
## Producer Identity

Pi51 is treated as a dedicated crawler and data-origin node in the current LogisticSearch architecture. It is not the final decision layer for ranking or outreach and is not intended to be a mixed application runtime surface. Therefore, this subtree should be read as a producer-origin export surface for crawler-side outputs that have crossed into the GitHub-mediated transport path.

## Üretici Kimliği

Pi51, mevcut LogisticSearch mimarisinde özel bir crawler ve veri-kaynağı düğümü olarak ele alınmaktadır. Nihai sıralama veya outreach karar katmanı değildir ve karışık bir uygulama runtime yüzeyi olması amaçlanmamaktadır. Bu nedenle bu alt ağaç, GitHub aracılı taşıma yoluna girmiş crawler tarafı çıktılar için bir üretici-köken export yüzeyi olarak okunmalıdır.
## Expected Contents

This area is expected to contain channel-scoped subtrees that represent concrete export delivery families from Pi51. A channel may define its own directory contract, catalog files, batch layout, and integrity conventions, but all such material should still remain aligned with the broader `crawler_exports/` discipline.

## Beklenen İçerik

Bu alanın, Pi51’den gelen somut export teslim ailelerini temsil eden kanal-kapsamlı alt ağaçlar içermesi beklenir. Her kanal kendi dizin sözleşmesini, catalog dosyalarını, batch yerleşimini ve bütünlük kurallarını tanımlayabilir; ancak tüm bu materyal yine de daha geniş `crawler_exports/` disipliniyle uyumlu kalmalıdır.
## Operational Meaning

Operationally, this subtree helps answer a simple but important question: “Which producer created the export artifacts that were later imported on Ubuntu Desktop?” Keeping that boundary explicit improves reviewability, troubleshooting, and data lineage clarity.

## Operasyonel Anlam

Operasyonel olarak bu alt ağaç basit ama önemli bir soruya cevap verir: “Daha sonra Ubuntu Desktop üzerinde import edilen export artefact’larını hangi üretici oluşturdu?” Bu sınırın açık tutulması; gözden geçirilebilirliği, sorun gidermeyi ve veri soy ağacı netliğini iyileştirir.
## What Belongs Here

Only Pi51-origin export material that has been intentionally accepted into the repository transport flow should live here. Durable channel structures, valid batch records, catalog material, and producer-relevant export metadata are suitable for this subtree.

## Burada Ne Yer Alır

Burada yalnızca repository taşıma akışına bilinçli olarak kabul edilmiş Pi51 kökenli export materyalleri yer almalıdır. Kalıcı kanal yapıları, geçerli batch kayıtları, catalog materyalleri ve üreticiyle ilgili export metadata’ları bu alt ağaç için uygundur.
## What Does Not Belong Here

Machine-local scratch files, hidden temporary work products, disposable experiments, and unrelated Pi51 host artifacts should not accumulate here. This subtree is not a raw host dump and should remain tightly scoped to canonical export delivery.

## Burada Ne Yer Almaz

Makineye özel geçici dosyalar, gizli temporary çalışma çıktıları, tek kullanımlık deneyler ve Pi51 host’una ait ilgisiz artefact’lar burada birikmemelidir. Bu alt ağaç ham bir host dökümü değildir; kanonik export teslimatıyla sıkı biçimde sınırlı kalmalıdır.
## Current Status

At present, the active repository-visible export channel under this producer subtree is `github_batch_v1`. Additional producer-specific channels may be introduced later, but they should follow the same discipline: explicit structure, reviewable metadata, and clear transport intent.

## Mevcut Durum

Şu anda bu üretici alt ağacı altında repository’de görünür aktif export kanalı `github_batch_v1`’dir. İleride ek üretici-özel kanallar tanımlanabilir; ancak aynı disiplini izlemelidirler: açık yapı, gözden geçirilebilir metadata ve net taşıma amacı.
## Notes

This subtree is best understood as a source identity boundary inside the broader export fabric.

## Notlar

Bu alt ağaç, daha geniş export dokusu içinde bir kaynak kimliği sınırı olarak anlaşılmalıdır.
