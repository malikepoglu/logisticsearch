-- SECTION1_WEBCRAWLER / TAXONOMY CORE PATCH
-- EN: Stage4E Arabic leasing/rental wording repair for exact target rows only.
-- TR: Stage4E Arabic leasing/rental ifade düzeltmesi; yalnızca exact target satırlar.

BEGIN;

-- EN: This temporary proposal table defines the only rows allowed to change.
-- TR: Bu geçici proposal tablosu değişmesine izin verilen tek satırları tanımlar.
CREATE TEMP TABLE stage4e_arabic_patch_proposal (
    proposal_order integer PRIMARY KEY,
    lang_code text NOT NULL,
    node_code text NOT NULL,
    current_title text NOT NULL,
    current_keyword text NOT NULL,
    proposed_title text NOT NULL,
    proposed_keyword text NOT NULL
);

-- EN: Insert the five human-approved Arabic replacements from Stage4C.
-- TR: Stage4C'de insan kararıyla onaylanan beş Arabic düzeltmeyi ekle.
INSERT INTO stage4e_arabic_patch_proposal (
    proposal_order,
    lang_code,
    node_code,
    current_title,
    current_keyword,
    proposed_title,
    proposed_keyword
)
VALUES
    (
        1,
        'ar',
        '10.2.5',
        'تأجير أو ليزينغ طائرات الركاب',
        'تأجير أو ليزينغ طائرات الركاب',
        'تأجير قصير أو طويل الأجل لطائرات الركاب',
        'تأجير قصير أو طويل الأجل لطائرات الركاب'
    ),
    (
        2,
        'ar',
        '10.3.1',
        'ليزينغ سيارات سيدان / كوبيه / ستيشن واجن',
        'ليزينغ سيارات سيدان / كوبيه / ستيشن واجن',
        'تأجير طويل الأجل لسيارات سيدان / كوبيه / ستيشن واجن',
        'تأجير طويل الأجل لسيارات سيدان / كوبيه / ستيشن واجن'
    ),
    (
        3,
        'ar',
        '10.3.2',
        'ليزينغ شاحنات خفيفة / SUV',
        'ليزينغ شاحنات خفيفة / SUV',
        'تأجير طويل الأجل لشاحنات خفيفة / سيارات رياضية متعددة الاستخدامات',
        'تأجير طويل الأجل لشاحنات خفيفة / سيارات رياضية متعددة الاستخدامات'
    ),
    (
        4,
        'ar',
        '10.3.3',
        'ليزينغ فان ركاب / ميني فان',
        'ليزينغ فان ركاب / ميني فان',
        'تأجير طويل الأجل لمركبات ركاب / حافلات صغيرة',
        'تأجير طويل الأجل لمركبات ركاب / حافلات صغيرة'
    ),
    (
        5,
        'ar',
        '10.3.4',
        'ليزينغ وسائط النقل',
        'ليزينغ وسائط النقل',
        'تأجير طويل الأجل لوسائط النقل',
        'تأجير طويل الأجل لوسائط النقل'
    );

-- EN: Keep update counters in a temporary audit table so the patch can assert itself before COMMIT.
-- TR: COMMIT öncesi patch kendini doğrulasın diye update sayaçlarını geçici audit tablosunda tut.
CREATE TEMP TABLE stage4e_arabic_patch_apply_audit (
    metric text PRIMARY KEY,
    value integer NOT NULL
);

-- EN: Hard preflight checks: exact scope, exact language, exact current target rows.
-- TR: Sert ön kontrol: exact kapsam, exact dil, exact mevcut hedef satırlar.
DO $$
DECLARE
    c integer;
BEGIN
    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal;

    IF c <> 5 THEN
        RAISE EXCEPTION 'Arabic proposal row count mismatch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal
    WHERE lang_code <> 'ar';

    IF c <> 0 THEN
        RAISE EXCEPTION 'Non-Arabic proposal rows detected: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal
    WHERE node_code NOT IN ('10.2.5', '10.3.1', '10.3.2', '10.3.3', '10.3.4');

    IF c <> 0 THEN
        RAISE EXCEPTION 'Unexpected Arabic proposal node rows detected: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal
    WHERE lang_code IN ('en', 'tr');

    IF c <> 0 THEN
        RAISE EXCEPTION 'Primary search language touch detected in Arabic patch proposal: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_node_translations AS t
      ON t.node_id = n.id
     AND t.lang_code = p.lang_code
     AND t.title = p.current_title
    JOIN logistics.taxonomy_keywords AS k
      ON k.node_id = n.id
     AND k.lang_code = p.lang_code
     AND k.keyword = p.current_keyword;

    IF c <> 5 THEN
        RAISE EXCEPTION 'Exact current Arabic target row count mismatch before patch: %', c;
    END IF;
END $$;

-- EN: Update only exact matching Arabic translation rows.
-- TR: Yalnızca exact eşleşen Arabic translation satırlarını güncelle.
WITH updated AS (
    UPDATE logistics.taxonomy_node_translations AS t
       SET title = p.proposed_title
      FROM stage4e_arabic_patch_proposal AS p
      JOIN logistics.taxonomy_nodes AS n
        ON n.node_code = p.node_code
     WHERE t.node_id = n.id
       AND t.lang_code = p.lang_code
       AND t.title = p.current_title
     RETURNING t.id
)
INSERT INTO stage4e_arabic_patch_apply_audit(metric, value)
SELECT 'translation_update_rows', COUNT(*)::integer
FROM updated;

-- EN: Update only exact matching Arabic primary keyword rows.
-- TR: Yalnızca exact eşleşen Arabic primary keyword satırlarını güncelle.
WITH updated AS (
    UPDATE logistics.taxonomy_keywords AS k
       SET keyword = p.proposed_keyword
      FROM stage4e_arabic_patch_proposal AS p
      JOIN logistics.taxonomy_nodes AS n
        ON n.node_code = p.node_code
     WHERE k.node_id = n.id
       AND k.lang_code = p.lang_code
       AND k.keyword = p.current_keyword
     RETURNING k.id
)
INSERT INTO stage4e_arabic_patch_apply_audit(metric, value)
SELECT 'keyword_update_rows', COUNT(*)::integer
FROM updated;

-- EN: Assert exact update cardinality before any COMMIT can happen.
-- TR: COMMIT olabilmeden önce exact update sayısını doğrula.
DO $$
DECLARE
    c integer;
BEGIN
    SELECT value INTO c
    FROM stage4e_arabic_patch_apply_audit
    WHERE metric = 'translation_update_rows';

    IF c <> 5 THEN
        RAISE EXCEPTION 'Arabic translation update row count mismatch: %', c;
    END IF;

    SELECT value INTO c
    FROM stage4e_arabic_patch_apply_audit
    WHERE metric = 'keyword_update_rows';

    IF c <> 5 THEN
        RAISE EXCEPTION 'Arabic keyword update row count mismatch: %', c;
    END IF;
END $$;

-- EN: Post-update guards inside the same transaction.
-- TR: Aynı transaction içinde patch sonrası güvenlik kontrolleri.
DO $$
DECLARE
    c integer;
BEGIN
    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_node_translations AS t
      ON t.node_id = n.id
     AND t.lang_code = p.lang_code
     AND t.title = p.proposed_title;

    IF c <> 5 THEN
        RAISE EXCEPTION 'Patched Arabic translation rows mismatch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_keywords AS k
      ON k.node_id = n.id
     AND k.lang_code = p.lang_code
     AND k.keyword = p.proposed_keyword;

    IF c <> 5 THEN
        RAISE EXCEPTION 'Patched Arabic keyword rows mismatch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_node_translations AS t
      ON t.node_id = n.id
     AND t.lang_code = p.lang_code
     AND t.title = p.current_title;

    IF c <> 0 THEN
        RAISE EXCEPTION 'Old Arabic translation rows still exist after patch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM stage4e_arabic_patch_proposal AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
    JOIN logistics.taxonomy_keywords AS k
      ON k.node_id = n.id
     AND k.lang_code = p.lang_code
     AND k.keyword = p.current_keyword;

    IF c <> 0 THEN
        RAISE EXCEPTION 'Old Arabic keyword rows still exist after patch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM (
        SELECT
            lang_code,
            logistics.normalize_taxonomy_text(keyword) AS normalized_keyword,
            COUNT(*) AS row_count
        FROM logistics.taxonomy_keywords
        GROUP BY
            lang_code,
            logistics.normalize_taxonomy_text(keyword)
        HAVING COUNT(*) > 1
    ) AS duplicate_groups;

    IF c <> 0 THEN
        RAISE EXCEPTION 'Duplicate normalized primary keyword groups after Arabic patch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM logistics.taxonomy_node_translations
    WHERE btrim(COALESCE(title, '')) = '';

    IF c <> 0 THEN
        RAISE EXCEPTION 'Blank taxonomy title rows after Arabic patch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM logistics.taxonomy_keywords
    WHERE btrim(COALESCE(keyword, '')) = '';

    IF c <> 0 THEN
        RAISE EXCEPTION 'Blank taxonomy keyword rows after Arabic patch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM logistics.taxonomy_keywords;

    IF c <> 8375 THEN
        RAISE EXCEPTION 'taxonomy_keywords count changed unexpectedly after Arabic patch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM logistics.taxonomy_node_translations;

    IF c <> 8375 THEN
        RAISE EXCEPTION 'taxonomy_node_translations count changed unexpectedly after Arabic patch: %', c;
    END IF;

    SELECT COUNT(*) INTO c
    FROM logistics.taxonomy_search_documents;

    IF c <> 8375 THEN
        RAISE EXCEPTION 'taxonomy_search_documents count changed unexpectedly after Arabic patch: %', c;
    END IF;
END $$;

-- EN: Emit a small apply audit for operator visibility.
-- TR: Operatör görünürlüğü için küçük apply audit çıktısı üret.
SELECT metric, value
FROM stage4e_arabic_patch_apply_audit
ORDER BY metric;

COMMIT;
