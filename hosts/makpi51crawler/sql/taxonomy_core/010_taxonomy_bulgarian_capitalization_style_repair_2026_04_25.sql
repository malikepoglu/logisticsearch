-- SECTION1_WEBCRAWLER / TAXONOMY CORE
-- EN: Stage5E Bulgarian capitalization/style repair patch.
-- TR: Stage5E Bulgarian büyük/küçük harf stil düzeltme patch'i.

-- EN: This patch is intentionally narrow.
-- TR: Bu patch özellikle dar kapsamlıdır.

-- EN: Scope is only Bulgarian bg / 10.2.3 and bg / 10.2.9.
-- TR: Kapsam yalnızca Bulgarian bg / 10.2.3 ve bg / 10.2.9 satırlarıdır.

-- EN: The patch updates the translation title and the exact current primary keyword text.
-- TR: Patch translation title ve exact current primary keyword metnini günceller.

BEGIN;

DO $$
DECLARE
    v_proposal_rows integer;
    v_target_node_rows integer;
    v_translation_current_rows integer;
    v_keyword_current_rows integer;
    v_new_translation_rows integer;
    v_new_keyword_rows integer;
    v_non_bg_rows integer;
    v_primary_language_touch integer;
BEGIN
    WITH proposal(node_code, current_title, current_keyword, proposed_title, proposed_keyword) AS (
        VALUES
            (
                '10.2.3',
                'Услуги за Наем на превозни средства',
                'Услуги за Наем на превозни средства',
                'Услуги за наем на превозни средства',
                'Услуги за наем на превозни средства'
            ),
            (
                '10.2.9',
                'Услуги за Наем на камион с оператор',
                'Услуги за Наем на камион с оператор',
                'Услуги за наем на камион с оператор',
                'Услуги за наем на камион с оператор'
            )
    ),
    target_nodes AS (
        SELECT n.id AS node_id, n.node_code
        FROM logistics.taxonomy_nodes AS n
        JOIN proposal AS p
          ON p.node_code = n.node_code
    )
    SELECT
        (SELECT COUNT(*) FROM proposal),
        (SELECT COUNT(*) FROM target_nodes),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_node_translations AS t
            JOIN target_nodes AS n
              ON n.node_id = t.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE t.lang_code = 'bg'
              AND t.title = p.current_title
        ),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_keywords AS k
            JOIN target_nodes AS n
              ON n.node_id = k.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE k.lang_code = 'bg'
              AND k.keyword = p.current_keyword
        ),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_node_translations AS t
            JOIN target_nodes AS n
              ON n.node_id = t.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE t.lang_code = 'bg'
              AND t.title = p.proposed_title
        ),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_keywords AS k
            JOIN target_nodes AS n
              ON n.node_id = k.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE k.lang_code = 'bg'
              AND k.keyword = p.proposed_keyword
        ),
        0,
        0
    INTO
        v_proposal_rows,
        v_target_node_rows,
        v_translation_current_rows,
        v_keyword_current_rows,
        v_new_translation_rows,
        v_new_keyword_rows,
        v_non_bg_rows,
        v_primary_language_touch;

    IF v_proposal_rows <> 2 THEN
        RAISE EXCEPTION 'Stage5E expected 2 proposal rows, got %', v_proposal_rows;
    END IF;

    IF v_target_node_rows <> 2 THEN
        RAISE EXCEPTION 'Stage5E expected 2 target nodes, got %', v_target_node_rows;
    END IF;

    IF v_translation_current_rows <> 2 THEN
        RAISE EXCEPTION 'Stage5E expected 2 current translation rows, got %', v_translation_current_rows;
    END IF;

    IF v_keyword_current_rows <> 2 THEN
        RAISE EXCEPTION 'Stage5E expected 2 current keyword rows, got %', v_keyword_current_rows;
    END IF;

    IF v_new_translation_rows <> 0 THEN
        RAISE EXCEPTION 'Stage5E expected 0 already-new translation rows, got %', v_new_translation_rows;
    END IF;

    IF v_new_keyword_rows <> 0 THEN
        RAISE EXCEPTION 'Stage5E expected 0 already-new keyword rows, got %', v_new_keyword_rows;
    END IF;
END $$;

WITH proposal(node_code, current_title, current_keyword, proposed_title, proposed_keyword) AS (
    VALUES
        (
            '10.2.3',
            'Услуги за Наем на превозни средства',
            'Услуги за Наем на превозни средства',
            'Услуги за наем на превозни средства',
            'Услуги за наем на превозни средства'
        ),
        (
            '10.2.9',
            'Услуги за Наем на камион с оператор',
            'Услуги за Наем на камион с оператор',
            'Услуги за наем на камион с оператор',
            'Услуги за наем на камион с оператор'
        )
),
target_rows AS (
    SELECT
        t.id AS translation_id,
        p.proposed_title
    FROM proposal AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_node_translations AS t
      ON t.node_id = n.id
     AND t.lang_code = 'bg'
     AND t.title = p.current_title
),
updated_rows AS (
    UPDATE logistics.taxonomy_node_translations AS t
    SET title = r.proposed_title
    FROM target_rows AS r
    WHERE t.id = r.translation_id
    RETURNING t.id
)
SELECT 'translation_update_rows' AS metric, COUNT(*)::text AS value
FROM updated_rows;

WITH proposal(node_code, current_title, current_keyword, proposed_title, proposed_keyword) AS (
    VALUES
        (
            '10.2.3',
            'Услуги за Наем на превозни средства',
            'Услуги за Наем на превозни средства',
            'Услуги за наем на превозни средства',
            'Услуги за наем на превозни средства'
        ),
        (
            '10.2.9',
            'Услуги за Наем на камион с оператор',
            'Услуги за Наем на камион с оператор',
            'Услуги за наем на камион с оператор',
            'Услуги за наем на камион с оператор'
        )
),
target_rows AS (
    SELECT
        k.id AS keyword_id,
        p.proposed_keyword
    FROM proposal AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_keywords AS k
      ON k.node_id = n.id
     AND k.lang_code = 'bg'
     AND k.keyword = p.current_keyword
),
updated_rows AS (
    UPDATE logistics.taxonomy_keywords AS k
    SET keyword = r.proposed_keyword
    FROM target_rows AS r
    WHERE k.id = r.keyword_id
    RETURNING k.id
)
SELECT 'keyword_update_rows' AS metric, COUNT(*)::text AS value
FROM updated_rows;

DO $$
DECLARE
    v_patched_translation_rows integer;
    v_patched_keyword_rows integer;
    v_old_translation_rows integer;
    v_old_keyword_rows integer;
    v_search_rows integer;
BEGIN
    WITH proposal(node_code, current_title, current_keyword, proposed_title, proposed_keyword) AS (
        VALUES
            (
                '10.2.3',
                'Услуги за Наем на превозни средства',
                'Услуги за Наем на превозни средства',
                'Услуги за наем на превозни средства',
                'Услуги за наем на превозни средства'
            ),
            (
                '10.2.9',
                'Услуги за Наем на камион с оператор',
                'Услуги за Наем на камион с оператор',
                'Услуги за наем на камион с оператор',
                'Услуги за наем на камион с оператор'
            )
    ),
    target_nodes AS (
        SELECT n.id AS node_id, n.node_code
        FROM logistics.taxonomy_nodes AS n
        JOIN proposal AS p
          ON p.node_code = n.node_code
    )
    SELECT
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_node_translations AS t
            JOIN target_nodes AS n
              ON n.node_id = t.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE t.lang_code = 'bg'
              AND t.title = p.proposed_title
        ),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_keywords AS k
            JOIN target_nodes AS n
              ON n.node_id = k.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE k.lang_code = 'bg'
              AND k.keyword = p.proposed_keyword
        ),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_node_translations AS t
            JOIN target_nodes AS n
              ON n.node_id = t.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE t.lang_code = 'bg'
              AND t.title = p.current_title
        ),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_keywords AS k
            JOIN target_nodes AS n
              ON n.node_id = k.node_id
            JOIN proposal AS p
              ON p.node_code = n.node_code
            WHERE k.lang_code = 'bg'
              AND k.keyword = p.current_keyword
        ),
        (
            SELECT COUNT(*)
            FROM logistics.taxonomy_search_documents AS sd
            JOIN proposal AS p
              ON p.node_code = sd.node_code
            WHERE sd.lang_code = 'bg'
              AND sd.title = p.proposed_title
              AND sd.positive_keywords = p.proposed_keyword
        )
    INTO
        v_patched_translation_rows,
        v_patched_keyword_rows,
        v_old_translation_rows,
        v_old_keyword_rows,
        v_search_rows;

    IF v_patched_translation_rows <> 2 THEN
        RAISE EXCEPTION 'Stage5E expected 2 patched translation rows, got %', v_patched_translation_rows;
    END IF;

    IF v_patched_keyword_rows <> 2 THEN
        RAISE EXCEPTION 'Stage5E expected 2 patched keyword rows, got %', v_patched_keyword_rows;
    END IF;

    IF v_old_translation_rows <> 0 THEN
        RAISE EXCEPTION 'Stage5E expected 0 old translation rows, got %', v_old_translation_rows;
    END IF;

    IF v_old_keyword_rows <> 0 THEN
        RAISE EXCEPTION 'Stage5E expected 0 old keyword rows, got %', v_old_keyword_rows;
    END IF;

    IF v_search_rows <> 2 THEN
        RAISE EXCEPTION 'Stage5E expected 2 reflected search document rows, got %', v_search_rows;
    END IF;
END $$;

COMMIT;
