-- SECTION1_WEBCRAWLER / TAXONOMY CORE SEMANTIC SEARCH ALIAS REPAIR
--
-- EN:
-- This repair keeps the user-facing English titles but changes selected
-- English primary keywords into short search aliases so trigram search ranks
-- road freight, sea freight, and logistics software correctly.
--
-- TR:
-- Bu onarım kullanıcıya görünen İngilizce başlıkları korur; fakat seçili
-- İngilizce primary keyword değerlerini kısa arama aliaslarına çevirir.
-- Böylece road freight, sea freight ve logistics software aramaları doğru
-- taxonomy node sonucunu en üste çıkarır.

BEGIN;

CREATE TEMP TABLE taxonomy_semantic_search_alias_repair_work (
  lang_code text NOT NULL,
  node_code text NOT NULL,
  expected_title text NOT NULL,
  new_primary_keyword text NOT NULL,
  PRIMARY KEY (lang_code, node_code)
) ON COMMIT DROP;

INSERT INTO taxonomy_semantic_search_alias_repair_work (
  lang_code,
  node_code,
  expected_title,
  new_primary_keyword
)
VALUES
  ('en', '1.1', 'Road Freight & Truck Transport', 'Road Freight'),
  ('en', '1.2', 'Sea Freight & Maritime Transport', 'Sea Freight'),
  ('en', '5.1', 'Logistics Software & Digital Systems', 'Logistics Software');

DO $$
DECLARE
  v_missing bigint;
BEGIN
  SELECT count(*)
  INTO v_missing
  FROM taxonomy_semantic_search_alias_repair_work AS p
  LEFT JOIN logistics.taxonomy_nodes AS n
    ON n.node_code = p.node_code
  LEFT JOIN logistics.taxonomy_node_translations AS t
    ON t.node_id = n.id
   AND t.lang_code = p.lang_code
  LEFT JOIN logistics.taxonomy_keywords AS k
    ON k.node_id = n.id
   AND k.lang_code = p.lang_code
   AND k.keyword_type = 'primary'
   AND k.is_official = true
   AND k.is_negative = false
  WHERE n.id IS NULL
     OR t.node_id IS NULL
     OR k.node_id IS NULL;

  IF v_missing <> 0 THEN
    RAISE EXCEPTION 'Search alias repair has % missing targets', v_missing;
  END IF;
END $$;

WITH patch AS (
  SELECT
    p.lang_code,
    p.node_code,
    p.expected_title,
    p.new_primary_keyword,
    n.id AS node_id
  FROM taxonomy_semantic_search_alias_repair_work AS p
  JOIN logistics.taxonomy_nodes AS n
    ON n.node_code = p.node_code
)
UPDATE logistics.taxonomy_node_translations AS t
SET title = patch.expected_title
FROM patch
WHERE t.node_id = patch.node_id
  AND t.lang_code = patch.lang_code
  AND t.title IS DISTINCT FROM patch.expected_title;

WITH patch AS (
  SELECT
    p.lang_code,
    p.node_code,
    p.expected_title,
    p.new_primary_keyword,
    n.id AS node_id
  FROM taxonomy_semantic_search_alias_repair_work AS p
  JOIN logistics.taxonomy_nodes AS n
    ON n.node_code = p.node_code
)
UPDATE logistics.taxonomy_keywords AS k
SET keyword = patch.new_primary_keyword
FROM patch
WHERE k.node_id = patch.node_id
  AND k.lang_code = patch.lang_code
  AND k.keyword_type = 'primary'
  AND k.is_official = true
  AND k.is_negative = false
  AND k.keyword IS DISTINCT FROM patch.new_primary_keyword;

SELECT logistics.taxonomy_node_translations_prepare() AS refreshed_translation_rows;
SELECT logistics.taxonomy_keywords_prepare() AS refreshed_keyword_rows;

DO $$
DECLARE
  v_bad bigint;
BEGIN
  WITH patch AS (
    SELECT
      p.lang_code,
      p.node_code,
      p.expected_title,
      p.new_primary_keyword,
      n.id AS node_id
    FROM taxonomy_semantic_search_alias_repair_work AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
  )
  SELECT count(*)
  INTO v_bad
  FROM patch
  JOIN logistics.taxonomy_node_translations AS t
    ON t.node_id = patch.node_id
   AND t.lang_code = patch.lang_code
  JOIN logistics.taxonomy_keywords AS k
    ON k.node_id = patch.node_id
   AND k.lang_code = patch.lang_code
   AND k.keyword_type = 'primary'
   AND k.is_official = true
   AND k.is_negative = false
  WHERE t.title IS DISTINCT FROM patch.expected_title
     OR k.keyword IS DISTINCT FROM patch.new_primary_keyword
     OR t.title_normalized IS DISTINCT FROM logistics.normalize_taxonomy_text(t.title)
     OR k.keyword_normalized IS DISTINCT FROM logistics.normalize_taxonomy_text(k.keyword)
     OR t.search_vector IS NULL
     OR k.search_vector IS NULL;

  IF v_bad <> 0 THEN
    RAISE EXCEPTION 'Search alias repair post-check bad count is %, expected 0', v_bad;
  END IF;
END $$;

COMMIT;
