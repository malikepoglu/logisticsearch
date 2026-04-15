\set ON_ERROR_STOP on

-- EN
-- Controlled apply surface for taxonomy_core on Pi51crawler.
-- This file applies the canonical host-scoped taxonomy runtime SQL in the
-- required order.
--
-- Order:
-- 1) base runtime objects
-- 2) prepare/load functions
-- 3) overlay/runtime extension layer
--
-- TR
-- Pi51crawler üzerinde taxonomy_core için kontrollü apply yüzeyi.
-- Bu dosya, kanonik host-scoped taxonomy runtime SQL yüzeyini gerekli sırayla uygular.
--
-- Sıra:
-- 1) temel runtime nesneleri
-- 2) hazırlama/yükleme fonksiyonları
-- 3) overlay/runtime genişleme katmanı

\echo
\echo == TAXONOMY_CORE CONTROLLED APPLY ==
\echo

\echo == 1) APPLY 001_taxonomy_runtime_base.sql ==
\i hosts/makpi51crawler/sql/taxonomy_core/001_taxonomy_runtime_base.sql

\echo
\echo == 2) APPLY 002_taxonomy_runtime_prepare_functions.sql ==
\i hosts/makpi51crawler/sql/taxonomy_core/002_taxonomy_runtime_prepare_functions.sql

\echo
\echo == 3) APPLY 003_taxonomy_runtime_overlay.sql ==
\i hosts/makpi51crawler/sql/taxonomy_core/003_taxonomy_runtime_overlay.sql

\echo
\echo TAXONOMY_CORE_APPLY_RESULT=PASS
