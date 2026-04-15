# Taxonomy Core SQL Surface
# Taksonomi Çekirdek SQL Yüzeyi

## Purpose
## Amaç

This surface defines the Pi51crawler-side runtime taxonomy layer used by crawler_core and parse_core.

Bu yüzey, crawler_core ve parse_core tarafından kullanılacak Pi51crawler tarafı runtime taxonomy katmanını tanımlar.

## Hard rule
## Sert kural

Raw staging tables are not runtime truth.

Ham staging tablolar runtime doğrusu değildir.

The runtime truth must live in a normalized `logistics` schema with constraints, indexes, and controlled prepare/rebuild functions.

Runtime doğrusu; constraint, index ve kontrollü prepare/rebuild fonksiyonlarına sahip normalize `logistics` şemasında yaşamalıdır.

## Immediate build order
## Acil kurulum sırası

1. supported_languages
2. taxonomy_nodes
3. taxonomy_node_translations
4. taxonomy_keywords
5. taxonomy_closure
6. taxonomy overlay family
7. prepare / rebuild functions
8. staging-to-runtime apply surface

1. supported_languages
2. taxonomy_nodes
3. taxonomy_node_translations
4. taxonomy_keywords
5. taxonomy_closure
6. taxonomy overlay ailesi
7. prepare / rebuild fonksiyonları
8. staging-to-runtime apply yüzeyi
