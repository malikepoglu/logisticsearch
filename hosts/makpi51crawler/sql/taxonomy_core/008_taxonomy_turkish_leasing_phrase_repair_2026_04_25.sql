\set ON_ERROR_STOP on

-- EN: Stage2F Turkish minimal phrase repair.
-- TR: Stage2F Türkçe minimal ifade düzeltmesi.
--
-- EN: Scope is deliberately limited to Turkish nodes 10.3.2 and 10.3.3.
-- TR: Kapsam bilinçli olarak yalnızca Türkçe 10.3.2 ve 10.3.3 node'larıyla sınırlıdır.
--
-- EN: This patch updates base tables only:
-- EN:   1) logistics.taxonomy_node_translations
-- EN:   2) logistics.taxonomy_keywords
-- TR: Bu patch yalnızca temel tabloları günceller:
-- TR:   1) logistics.taxonomy_node_translations
-- TR:   2) logistics.taxonomy_keywords
--
-- EN: logistics.taxonomy_search_documents is intentionally not updated here because current schema exposes it as a non-updatable view.
-- TR: logistics.taxonomy_search_documents burada bilinçli olarak güncellenmez; mevcut şemada update edilemeyen view olarak görünür.

BEGIN;

-- EN: Exact target rows and proposed values.
-- TR: Exact hedef satırlar ve önerilen değerler.
CREATE TEMP TABLE stage2f_patch_target (
    lang_code text NOT NULL,
    node_code text NOT NULL,
    current_text text NOT NULL,
    proposed_text text NOT NULL,
    proposed_normalized text NOT NULL
) ON COMMIT DROP;

INSERT INTO stage2f_patch_target
    (lang_code, node_code, current_text, proposed_text, proposed_normalized)
VALUES
    ('tr', '10.3.2',
     'Hafif Kamyon / SUV Leasingi leasing hizmetleri',
     'Hafif Kamyon / SUV Leasing Hizmetleri',
     'hafif kamyon / suv leasing hizmetleri'),
    ('tr', '10.3.3',
     'Yolcu Vanı / Minivan Leasingi leasing hizmetleri',
     'Yolcu Vanı / Minivan Leasing Hizmetleri',
     'yolcu vanı / minivan leasing hizmetleri');

-- EN: Precondition guard; both translation and exact keyword targets must exist exactly once.
-- TR: Ön koşul koruması; translation ve exact keyword hedefleri tam olarak birer kez bulunmalıdır.
DO $$
DECLARE
    v_translation_targets integer;
    v_keyword_targets integer;
    v_semantic_touch integer;
BEGIN
    SELECT COUNT(*)
      INTO v_translation_targets
      FROM stage2f_patch_target p
      JOIN logistics.taxonomy_nodes n
        ON n.node_code = p.node_code
      JOIN logistics.taxonomy_node_translations tr
        ON tr.node_id = n.id
       AND tr.lang_code = p.lang_code
       AND tr.title = p.current_text;

    SELECT COUNT(*)
      INTO v_keyword_targets
      FROM stage2f_patch_target p
      JOIN logistics.taxonomy_nodes n
        ON n.node_code = p.node_code
      JOIN logistics.taxonomy_keywords k
        ON k.node_id = n.id
       AND k.lang_code = p.lang_code
       AND k.keyword = p.current_text;

    SELECT COUNT(*)
      INTO v_semantic_touch
      FROM stage2f_patch_target
     WHERE node_code IN ('1.1', '1.2', '5.1');

    IF v_translation_targets <> 2 THEN
        RAISE EXCEPTION 'Stage2F precondition failed: translation targets %, expected 2', v_translation_targets;
    END IF;

    IF v_keyword_targets <> 2 THEN
        RAISE EXCEPTION 'Stage2F precondition failed: exact keyword targets %, expected 2', v_keyword_targets;
    END IF;

    IF v_semantic_touch <> 0 THEN
        RAISE EXCEPTION 'Stage2F safety failed: semantic target touch count %, expected 0', v_semantic_touch;
    END IF;
END $$;

-- EN: Update only the two exact Turkish translation rows.
-- TR: Yalnızca iki exact Türkçe translation satırını güncelle.
WITH target AS (
    SELECT
        tr.id AS translation_id,
        p.proposed_text,
        p.proposed_normalized
    FROM stage2f_patch_target p
    JOIN logistics.taxonomy_nodes n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_node_translations tr
      ON tr.node_id = n.id
     AND tr.lang_code = p.lang_code
     AND tr.title = p.current_text
)
UPDATE logistics.taxonomy_node_translations tr
   SET title = target.proposed_text,
       title_normalized = target.proposed_normalized,
       updated_at = now()
  FROM target
 WHERE tr.id = target.translation_id;

-- EN: Update only the two exact Turkish keyword rows.
-- TR: Yalnızca iki exact Türkçe keyword satırını güncelle.
WITH target AS (
    SELECT
        k.id AS keyword_id,
        p.proposed_text,
        p.proposed_normalized
    FROM stage2f_patch_target p
    JOIN logistics.taxonomy_nodes n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_keywords k
      ON k.node_id = n.id
     AND k.lang_code = p.lang_code
     AND k.keyword = p.current_text
)
UPDATE logistics.taxonomy_keywords k
   SET keyword = target.proposed_text,
       keyword_normalized = target.proposed_normalized,
       updated_at = now()
  FROM target
 WHERE k.id = target.keyword_id;

-- EN: Refresh writable translation search vectors if the column is a normal writable column.
-- TR: Kolon normal yazılabilir kolonsa translation search_vector değerlerini yenile.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
          FROM information_schema.columns
         WHERE table_schema = 'logistics'
           AND table_name = 'taxonomy_node_translations'
           AND column_name = 'search_vector'
           AND is_generated = 'NEVER'
    ) THEN
        UPDATE logistics.taxonomy_node_translations tr
           SET search_vector = to_tsvector('simple', coalesce(tr.title, ''))
          FROM stage2f_patch_target p
          JOIN logistics.taxonomy_nodes n
            ON n.node_code = p.node_code
         WHERE tr.node_id = n.id
           AND tr.lang_code = p.lang_code;
    END IF;

    IF EXISTS (
        SELECT 1
          FROM information_schema.columns
         WHERE table_schema = 'logistics'
           AND table_name = 'taxonomy_keywords'
           AND column_name = 'search_vector'
           AND is_generated = 'NEVER'
    ) THEN
        UPDATE logistics.taxonomy_keywords k
           SET search_vector = to_tsvector('simple', coalesce(k.keyword, ''))
          FROM stage2f_patch_target p
          JOIN logistics.taxonomy_nodes n
            ON n.node_code = p.node_code
         WHERE k.node_id = n.id
           AND k.lang_code = p.lang_code;
    END IF;
END $$;

-- EN: Postcondition guard; patched rows must exist and old rows must be gone.
-- TR: Son koşul koruması; patchlenmiş satırlar var olmalı ve eski satırlar kalmamalıdır.
DO $$
DECLARE
    v_patched_translations integer;
    v_patched_keywords integer;
    v_old_translations integer;
    v_old_keywords integer;
    v_duplicate_groups integer;
BEGIN
    SELECT COUNT(*)
      INTO v_patched_translations
      FROM stage2f_patch_target p
      JOIN logistics.taxonomy_nodes n
        ON n.node_code = p.node_code
      JOIN logistics.taxonomy_node_translations tr
        ON tr.node_id = n.id
       AND tr.lang_code = p.lang_code
       AND tr.title = p.proposed_text
       AND tr.title_normalized = p.proposed_normalized;

    SELECT COUNT(*)
      INTO v_patched_keywords
      FROM stage2f_patch_target p
      JOIN logistics.taxonomy_nodes n
        ON n.node_code = p.node_code
      JOIN logistics.taxonomy_keywords k
        ON k.node_id = n.id
       AND k.lang_code = p.lang_code
       AND k.keyword = p.proposed_text
       AND k.keyword_normalized = p.proposed_normalized;

    SELECT COUNT(*)
      INTO v_old_translations
      FROM stage2f_patch_target p
      JOIN logistics.taxonomy_nodes n
        ON n.node_code = p.node_code
      JOIN logistics.taxonomy_node_translations tr
        ON tr.node_id = n.id
       AND tr.lang_code = p.lang_code
       AND tr.title = p.current_text;

    SELECT COUNT(*)
      INTO v_old_keywords
      FROM stage2f_patch_target p
      JOIN logistics.taxonomy_nodes n
        ON n.node_code = p.node_code
      JOIN logistics.taxonomy_keywords k
        ON k.node_id = n.id
       AND k.lang_code = p.lang_code
       AND k.keyword = p.current_text;

    SELECT COUNT(*)
      INTO v_duplicate_groups
      FROM (
        SELECT lang_code, keyword_normalized, COUNT(*) AS c
          FROM logistics.taxonomy_keywords
         GROUP BY lang_code, keyword_normalized
        HAVING COUNT(*) > 1
      ) d;

    IF v_patched_translations <> 2 THEN
        RAISE EXCEPTION 'Stage2F postcondition failed: patched translations %, expected 2', v_patched_translations;
    END IF;

    IF v_patched_keywords <> 2 THEN
        RAISE EXCEPTION 'Stage2F postcondition failed: patched keywords %, expected 2', v_patched_keywords;
    END IF;

    IF v_old_translations <> 0 THEN
        RAISE EXCEPTION 'Stage2F postcondition failed: old translations %, expected 0', v_old_translations;
    END IF;

    IF v_old_keywords <> 0 THEN
        RAISE EXCEPTION 'Stage2F postcondition failed: old keywords %, expected 0', v_old_keywords;
    END IF;

    IF v_duplicate_groups <> 0 THEN
        RAISE EXCEPTION 'Stage2F postcondition failed: duplicate keyword groups %, expected 0', v_duplicate_groups;
    END IF;
END $$;

COMMIT;
