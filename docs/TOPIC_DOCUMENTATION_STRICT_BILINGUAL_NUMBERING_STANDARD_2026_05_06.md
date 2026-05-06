# 0. Documentation Strict Bilingual Numbering Standard

## EN 0.1 Purpose

This document defines the strict canonical structure for Markdown documentation in the LogisticSearch repository.

The goal is not visual beauty. The goal is auditability, predictable navigation, and easy EN/TR consistency checking.

## EN 0.2 Required document shape

Every Markdown document should use one root H1 heading.

The root H1 must start with `# 0. `.

After the root H1, the document must contain the complete English block first and the complete Turkish block second.

## EN 0.3 Required heading format

Every content heading below the root H1 must carry a language marker and a hierarchical number.

Required examples:

- `## EN 0.1 Purpose`
- `### EN 0.1.1 Scope`
- `## TR 0.1 Amaç`
- `### TR 0.1.1 Kapsam`

## EN 0.4 EN/TR numbering equality rule

The English and Turkish heading number sequences must match exactly.

If English has `0.1`, `0.1.1`, and `0.2`, Turkish must also have `0.1`, `0.1.1`, and `0.2` in the same semantic order.

## EN 0.5 Language order rule

English must come first.

Turkish must come second.

A document must not alternate as EN, TR, EN, TR across the main body.

## EN 0.6 Code block and command exception

Code fences, terminal commands, file paths, package names, function names, class names, database names, host names, and commit hashes stay exact.

They must not be translated merely to satisfy bilingual formatting.

## EN 0.7 Safety rule

Documentation restructuring must not execute crawler controls, start services, mutate databases, touch pi51c runtime, or run systemd commands.

Documentation audits and formatting patches remain `NO_CONTROL_SCRIPT_EXECUTION`.

## EN 0.8 Migration rule

Existing documents must be converted in small batches.

A batch must be validated before commit.

High-risk documents that are missing one language or have unclear heading ownership must not be blindly auto-patched.

## TR 0.1 Amaç

Bu doküman LogisticSearch repository içindeki Markdown dokümantasyonu için kesin kanonik yapıyı tanımlar.

Hedef görsel güzellik değildir. Hedef denetlenebilirlik, öngörülebilir gezinme ve EN/TR tutarlılığının kolay kontrol edilebilmesidir.

## TR 0.2 Zorunlu doküman şekli

Her Markdown dokümanı tek bir kök H1 başlığı kullanmalıdır.

Kök H1 başlığı `# 0. ` ile başlamalıdır.

Kök H1 başlığından sonra önce eksiksiz İngilizce blok, sonra eksiksiz Türkçe blok gelmelidir.

## TR 0.3 Zorunlu başlık formatı

Kök H1 altındaki her içerik başlığı dil etiketi ve hiyerarşik numara taşımalıdır.

Zorunlu örnekler:

- `## EN 0.1 Purpose`
- `### EN 0.1.1 Scope`
- `## TR 0.1 Amaç`
- `### TR 0.1.1 Kapsam`

## TR 0.4 EN/TR numara eşitliği kuralı

İngilizce ve Türkçe başlık numara dizileri birebir aynı olmalıdır.

İngilizcede `0.1`, `0.1.1` ve `0.2` varsa Türkçede de aynı semantik sırada `0.1`, `0.1.1` ve `0.2` bulunmalıdır.

## TR 0.5 Dil sırası kuralı

İngilizce önce gelmelidir.

Türkçe sonra gelmelidir.

Bir doküman ana gövdede EN, TR, EN, TR şeklinde dönüşümlü ilerlememelidir.

## TR 0.6 Kod bloğu ve komut istisnası

Code fence blokları, terminal komutları, dosya yolları, paket adları, fonksiyon adları, sınıf adları, veritabanı adları, host adları ve commit hash değerleri exact kalır.

Bunlar yalnızca çift dilli biçimi sağlamak için çevrilmemelidir.

## TR 0.7 Güvenlik kuralı

Dokümantasyon yeniden düzenlemesi crawler kontrollerini çalıştırmamalı, servis başlatmamalı, veritabanı değiştirmemeli, pi51c runtime yüzeyine dokunmamalı ve systemd komutu çalıştırmamalıdır.

Dokümantasyon audit ve format patch işlemleri `NO_CONTROL_SCRIPT_EXECUTION` kuralını korur.

## TR 0.8 Migration kuralı

Mevcut dokümanlar küçük batch'ler halinde dönüştürülmelidir.

Her batch commit öncesi doğrulanmalıdır.

Tek dili eksik olan veya başlık sahipliği belirsiz olan yüksek riskli dokümanlar kör auto-patch ile dönüştürülmemelidir.
