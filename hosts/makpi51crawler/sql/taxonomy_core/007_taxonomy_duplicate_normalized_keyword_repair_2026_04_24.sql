\set ON_ERROR_STOP on
\pset pager off
\pset format aligned

BEGIN;

\echo == PATCH 007_R2B / LANGUAGE SCOPE ==
SELECT
  'ALL_25_LANGUAGES' AS active_language_scope,
  string_agg(lang_code, ',' ORDER BY sort_order) AS active_language_codes
FROM logistics.supported_languages
WHERE is_active = true;

CREATE TEMP TABLE _patch007_language_affix (
  lang_code text PRIMARY KEY,
  rental_prefix text NOT NULL,
  rental_suffix text NOT NULL,
  leasing_prefix text NOT NULL,
  leasing_suffix text NOT NULL
) ON COMMIT DROP;

INSERT INTO _patch007_language_affix
  (lang_code, rental_prefix, rental_suffix, leasing_prefix, leasing_suffix)
VALUES
  ('ar','خدمات ','','خدمات تأجير تمويلي ',''),
  ('bg','Услуги за ','','Лизингови услуги за ',''),
  ('cs','',' služby','',' leasingové služby'),
  ('de','Dienstleistungen für ','','Leasingdienstleistungen für ',''),
  ('el','Υπηρεσίες: ','','Υπηρεσίες leasing: ',''),
  ('en','',' Services','',' Leasing Services'),
  ('es','servicios de ','','servicios de leasing de ',''),
  ('fr','services de ','','services de leasing de ',''),
  ('hu','',' szolgáltatások','',' lízingszolgáltatások'),
  ('it','servizi di ','','servizi di leasing per ',''),
  ('ja','','サービス','','リースサービス'),
  ('ko','',' 서비스','',' 리스 서비스'),
  ('nl','',' diensten','',' leasingdiensten'),
  ('pt','serviços de ','','serviços de leasing de ',''),
  ('ro','Servicii de ','','Servicii de leasing pentru ',''),
  ('ru','Услуги: ','','Лизинговые услуги: ',''),
  ('tr','',' hizmetleri','',' leasing hizmetleri'),
  ('zh','','服务','','租赁服务'),
  ('hi','',' सेवाएँ','',' लीजिंग सेवाएँ'),
  ('bn','',' সেবা','',' লিজিং সেবা'),
  ('ur','خدمات ','','لیزنگ خدمات ',''),
  ('uk','Послуги: ','','Лізингові послуги: ',''),
  ('id','Layanan ','','Layanan leasing ',''),
  ('vi','Dịch vụ ','','Dịch vụ leasing ',''),
  ('he','שירותי ','','שירותי ליסינג ','');

CREATE TEMP TABLE _patch007_base AS
WITH primary_kw AS (
  SELECT
    k.node_id,
    k.lang_code,
    k.keyword,
    k.keyword_normalized
  FROM logistics.taxonomy_keywords AS k
  WHERE k.keyword_type = 'primary'
    AND k.is_official = true
    AND k.is_negative = false
)
SELECT
  sl.sort_order,
  sl.lang_code,
  sl.english_name,
  sl.turkish_name,
  sl.native_name,
  n.id AS node_id,
  n.node_code,
  t.title,
  pk.keyword,
  t.title_normalized,
  pk.keyword_normalized
FROM logistics.supported_languages AS sl
JOIN logistics.taxonomy_nodes AS n
  ON true
JOIN logistics.taxonomy_node_translations AS t
  ON t.node_id = n.id
 AND t.lang_code = sl.lang_code
JOIN primary_kw AS pk
  ON pk.node_id = n.id
 AND pk.lang_code = sl.lang_code
WHERE sl.is_active = true;

CREATE TEMP TABLE _patch007_dup_key AS
SELECT
  lang_code,
  keyword_normalized
FROM _patch007_base
GROUP BY
  lang_code,
  keyword_normalized
HAVING count(*) > 1;

CREATE TEMP TABLE _patch007_dup_member AS
SELECT
  b.*
FROM _patch007_base AS b
JOIN _patch007_dup_key AS d
  ON d.lang_code = b.lang_code
 AND d.keyword_normalized = b.keyword_normalized;

CREATE TEMP TABLE _patch007_proposal AS
SELECT
  dm.sort_order,
  dm.lang_code,
  dm.english_name,
  dm.turkish_name,
  dm.native_name,
  dm.node_id,
  dm.node_code,
  dm.title AS current_title,
  dm.keyword AS current_keyword,
  dm.title_normalized AS current_title_normalized,
  dm.keyword_normalized AS current_keyword_normalized,
  CASE
    WHEN dm.node_code LIKE '10.2.%' THEN 'rental_service_side_minimal_change'
    WHEN dm.node_code LIKE '10.3.%' THEN 'leasing_service_side_minimal_change'
    ELSE 'not_selected_for_minimal_change'
  END AS proposal_role,
  CASE
    WHEN dm.node_code LIKE '10.2.%' THEN la.rental_prefix || dm.title || la.rental_suffix
    WHEN dm.node_code LIKE '10.3.%' THEN la.leasing_prefix || dm.title || la.leasing_suffix
    ELSE dm.title
  END AS proposed_title,
  CASE
    WHEN dm.node_code LIKE '10.2.%' THEN la.rental_prefix || dm.keyword || la.rental_suffix
    WHEN dm.node_code LIKE '10.3.%' THEN la.leasing_prefix || dm.keyword || la.leasing_suffix
    ELSE dm.keyword
  END AS proposed_keyword
FROM _patch007_dup_member AS dm
JOIN _patch007_language_affix AS la
  ON la.lang_code = dm.lang_code
WHERE dm.node_code LIKE '10.2.%'
   OR dm.node_code LIKE '10.3.%';

\echo == PATCH 007_R2B / PRE-UPDATE PROPOSAL SUMMARY ==
SELECT
  count(*) AS proposal_rows,
  count(DISTINCT lang_code) AS touched_languages,
  count(*) FILTER (WHERE node_code IN ('1.1','1.2','5.1','9.2')) AS blocked_target_rows,
  count(*) FILTER (WHERE proposed_title IS NULL OR btrim(proposed_title) = '') AS blank_title_proposals,
  count(*) FILTER (WHERE proposed_keyword IS NULL OR btrim(proposed_keyword) = '') AS blank_keyword_proposals,
  count(*) FILTER (WHERE NOT (node_code LIKE '10.2.%' OR node_code LIKE '10.3.%')) AS non_service_side_proposals
FROM _patch007_proposal;

\echo == PATCH 007_R2B / PRE-UPDATE LANGUAGE SUMMARY ==
SELECT
  sl.sort_order,
  sl.lang_code,
  sl.english_name || ' / ' || sl.turkish_name AS language_name,
  count(DISTINCT dk.keyword_normalized) AS duplicate_group_count,
  count(p.*) AS proposed_service_side_rows
FROM logistics.supported_languages AS sl
LEFT JOIN _patch007_dup_key AS dk
  ON dk.lang_code = sl.lang_code
LEFT JOIN _patch007_proposal AS p
  ON p.lang_code = sl.lang_code
WHERE sl.is_active = true
GROUP BY
  sl.sort_order,
  sl.lang_code,
  sl.english_name,
  sl.turkish_name
ORDER BY
  sl.sort_order;

DO $$
DECLARE
  v_current_dup int;
  v_dup_members int;
  v_proposals int;
  v_blocked_target int;
  v_blank_title int;
  v_blank_keyword int;
  v_non_service int;
  v_covered_groups int;
  v_virtual_dup int;
  v_virtual_target_dup int;
  v_lang_count int;
  v_counts text;
BEGIN
  SELECT count(*) INTO v_current_dup FROM _patch007_dup_key;
  SELECT count(*) INTO v_dup_members FROM _patch007_dup_member;
  SELECT count(*) INTO v_proposals FROM _patch007_proposal;

  SELECT count(*) INTO v_blocked_target
  FROM _patch007_proposal
  WHERE node_code IN ('1.1','1.2','5.1','9.2');

  SELECT count(*) INTO v_blank_title
  FROM _patch007_proposal
  WHERE proposed_title IS NULL OR btrim(proposed_title) = '';

  SELECT count(*) INTO v_blank_keyword
  FROM _patch007_proposal
  WHERE proposed_keyword IS NULL OR btrim(proposed_keyword) = '';

  SELECT count(*) INTO v_non_service
  FROM _patch007_proposal
  WHERE NOT (node_code LIKE '10.2.%' OR node_code LIKE '10.3.%');

  WITH coverage AS (
    SELECT
      d.lang_code,
      d.keyword_normalized,
      count(dm.*) AS duplicate_member_rows,
      count(p.*) AS proposal_rows,
      count(dm.*) FILTER (WHERE NOT (dm.node_code LIKE '10.2.%' OR dm.node_code LIKE '10.3.%')) AS preserved_rows
    FROM _patch007_dup_key AS d
    JOIN _patch007_dup_member AS dm
      ON dm.lang_code = d.lang_code
     AND dm.keyword_normalized = d.keyword_normalized
    LEFT JOIN _patch007_proposal AS p
      ON p.lang_code = dm.lang_code
     AND p.node_id = dm.node_id
    GROUP BY
      d.lang_code,
      d.keyword_normalized
  )
  SELECT count(*) INTO v_covered_groups
  FROM coverage
  WHERE duplicate_member_rows = 2
    AND proposal_rows = 1
    AND preserved_rows = 1;

  WITH virtual_keywords AS (
    SELECT
      b.lang_code,
      b.node_code,
      COALESCE(logistics.normalize_taxonomy_text(p.proposed_keyword), b.keyword_normalized) AS virtual_keyword_normalized
    FROM _patch007_base AS b
    LEFT JOIN _patch007_proposal AS p
      ON p.lang_code = b.lang_code
     AND p.node_id = b.node_id
  ),
  virtual_dup AS (
    SELECT
      lang_code,
      virtual_keyword_normalized
    FROM virtual_keywords
    GROUP BY
      lang_code,
      virtual_keyword_normalized
    HAVING count(*) > 1
  ),
  virtual_target_dup AS (
    SELECT
      lang_code,
      virtual_keyword_normalized
    FROM virtual_keywords
    GROUP BY
      lang_code,
      virtual_keyword_normalized
    HAVING count(*) > 1
       AND bool_or(node_code IN ('1.1','1.2','5.1','9.2'))
  )
  SELECT
    (SELECT count(*) FROM virtual_dup),
    (SELECT count(*) FROM virtual_target_dup)
  INTO
    v_virtual_dup,
    v_virtual_target_dup;

  SELECT count(*) INTO v_lang_count
  FROM logistics.supported_languages
  WHERE is_active = true;

  SELECT
    (SELECT count(*) FROM logistics.supported_languages)::text || '|' ||
    (SELECT count(*) FROM logistics.supported_languages WHERE is_active)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_nodes)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_node_translations)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_keywords)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_search_documents)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_closure)::text
  INTO v_counts;

  IF v_current_dup <> 73 THEN
    RAISE EXCEPTION 'expected 73 duplicate groups before patch, got %', v_current_dup;
  END IF;

  IF v_dup_members <> 146 THEN
    RAISE EXCEPTION 'expected 146 duplicate member rows before patch, got %', v_dup_members;
  END IF;

  IF v_proposals <> 73 THEN
    RAISE EXCEPTION 'expected 73 minimal service-side proposals, got %', v_proposals;
  END IF;

  IF v_blocked_target <> 0 THEN
    RAISE EXCEPTION 'proposal touches semantic target rows: %', v_blocked_target;
  END IF;

  IF v_blank_title <> 0 OR v_blank_keyword <> 0 THEN
    RAISE EXCEPTION 'blank proposal detected title=% keyword=%', v_blank_title, v_blank_keyword;
  END IF;

  IF v_non_service <> 0 THEN
    RAISE EXCEPTION 'non-service-side proposals detected: %', v_non_service;
  END IF;

  IF v_covered_groups <> 73 THEN
    RAISE EXCEPTION 'not every duplicate group has exactly one service-side proposal: %', v_covered_groups;
  END IF;

  IF v_virtual_dup <> 0 THEN
    RAISE EXCEPTION 'virtual duplicate count after proposal is not zero: %', v_virtual_dup;
  END IF;

  IF v_virtual_target_dup <> 0 THEN
    RAISE EXCEPTION 'virtual target-related duplicate count after proposal is not zero: %', v_virtual_target_dup;
  END IF;

  IF v_lang_count <> 25 THEN
    RAISE EXCEPTION 'active language count drifted: %', v_lang_count;
  END IF;

  IF v_counts <> '25|25|335|8375|8375|8375|995' THEN
    RAISE EXCEPTION 'global count precondition drifted: %', v_counts;
  END IF;
END $$;

\echo == PATCH 007_R2B / APPLY TRANSLATION TITLE UPDATES ==
WITH updated AS (
  UPDATE logistics.taxonomy_node_translations AS t
  SET title = p.proposed_title
  FROM _patch007_proposal AS p
  WHERE t.node_id = p.node_id
    AND t.lang_code = p.lang_code
  RETURNING t.node_id, t.lang_code
)
SELECT count(*) AS updated_translation_rows
FROM updated;

\echo == PATCH 007_R2B / APPLY PRIMARY KEYWORD UPDATES ==
WITH updated AS (
  UPDATE logistics.taxonomy_keywords AS k
  SET keyword = p.proposed_keyword
  FROM _patch007_proposal AS p
  WHERE k.node_id = p.node_id
    AND k.lang_code = p.lang_code
    AND k.keyword_type = 'primary'
    AND k.is_official = true
    AND k.is_negative = false
  RETURNING k.node_id, k.lang_code
)
SELECT count(*) AS updated_primary_keyword_rows
FROM updated;

\echo == PATCH 007_R2B / REFRESH NORMALIZED RUNTIME FIELDS ==
SELECT logistics.taxonomy_node_translations_prepare() AS refreshed_translation_rows;
SELECT logistics.taxonomy_keywords_prepare() AS refreshed_keyword_rows;

CREATE TEMP TABLE _patch007_duplicate_after AS
SELECT
  lang_code,
  keyword_normalized,
  count(*) AS row_count
FROM logistics.taxonomy_keywords AS k
WHERE k.keyword_type = 'primary'
  AND k.is_official = true
  AND k.is_negative = false
GROUP BY
  lang_code,
  keyword_normalized
HAVING count(*) > 1;

CREATE TEMP TABLE _patch007_semantic_expectations AS
WITH target_rows AS (
  SELECT
    sl.sort_order,
    sl.lang_code,
    sl.english_name || ' / ' || sl.turkish_name AS language_name,
    n.node_code,
    t.title,
    k.keyword
  FROM logistics.supported_languages AS sl
  JOIN logistics.taxonomy_nodes AS n
    ON n.node_code IN ('1.1','1.2','5.1')
  JOIN logistics.taxonomy_node_translations AS t
    ON t.node_id = n.id
   AND t.lang_code = sl.lang_code
  JOIN logistics.taxonomy_keywords AS k
    ON k.node_id = n.id
   AND k.lang_code = sl.lang_code
   AND k.keyword_type = 'primary'
   AND k.is_official = true
   AND k.is_negative = false
  WHERE sl.is_active = true
)
SELECT sort_order, lang_code, language_name, 'road' AS query_group, title AS query_text, '1.1' AS expected_node_code
FROM target_rows
WHERE node_code = '1.1'
UNION ALL
SELECT sort_order, lang_code, language_name, 'sea' AS query_group, title AS query_text, '1.2' AS expected_node_code
FROM target_rows
WHERE node_code = '1.2'
UNION ALL
SELECT sort_order, lang_code, language_name, 'software' AS query_group, title AS query_text, '5.1' AS expected_node_code
FROM target_rows
WHERE node_code = '5.1'
UNION ALL
SELECT sort_order, lang_code, language_name, 'truck' AS query_group, keyword AS query_text, '1.1' AS expected_node_code
FROM target_rows
WHERE node_code = '1.1';

CREATE TEMP TABLE _patch007_semantic_result AS
WITH matches AS (
  SELECT
    e.sort_order,
    e.lang_code,
    e.query_group,
    n.node_code AS matched_node_code
  FROM _patch007_semantic_expectations AS e
  JOIN logistics.taxonomy_search_documents AS sd
    ON sd.lang_code = e.lang_code
  JOIN logistics.taxonomy_nodes AS n
    ON n.id = sd.node_id
  WHERE logistics.normalize_taxonomy_text(sd.title) = logistics.normalize_taxonomy_text(e.query_text)
     OR logistics.normalize_taxonomy_text(sd.positive_keywords) = logistics.normalize_taxonomy_text(e.query_text)
)
SELECT
  e.sort_order,
  e.lang_code,
  e.language_name,
  e.query_group,
  e.query_text,
  e.expected_node_code,
  count(m.matched_node_code) AS exact_match_node_count,
  string_agg(m.matched_node_code, ',' ORDER BY m.matched_node_code) AS exact_match_node_codes,
  bool_or(m.matched_node_code = e.expected_node_code) AS expected_node_present,
  (
    count(m.matched_node_code) = 1
    AND bool_or(m.matched_node_code = e.expected_node_code)
  ) AS expected_top_match
FROM _patch007_semantic_expectations AS e
LEFT JOIN matches AS m
  ON m.sort_order = e.sort_order
 AND m.lang_code = e.lang_code
 AND m.query_group = e.query_group
GROUP BY
  e.sort_order,
  e.lang_code,
  e.language_name,
  e.query_group,
  e.query_text,
  e.expected_node_code;

\echo == PATCH 007_R2B / POST-DUPLICATE SUMMARY ==
SELECT
  count(*) AS duplicate_group_count_after_patch
FROM _patch007_duplicate_after;

\echo == PATCH 007_R2B / 25-LANGUAGE SEMANTIC SUMMARY ==
SELECT
  sort_order,
  lang_code,
  language_name,
  count(*) FILTER (WHERE NOT expected_top_match) AS failed_semantic_queries,
  count(*) AS tested_semantic_queries
FROM _patch007_semantic_result
GROUP BY
  sort_order,
  lang_code,
  language_name
ORDER BY
  sort_order;

\echo == PATCH 007_R2B / HARD STRUCTURAL COUNTS ==
SELECT
  (SELECT count(*) FROM logistics.supported_languages) AS supported_languages,
  (SELECT count(*) FROM logistics.supported_languages WHERE is_active) AS active_supported_languages,
  (SELECT string_agg(lang_code, ',' ORDER BY sort_order) FROM logistics.supported_languages WHERE is_active) AS canonical_order,
  (SELECT string_agg(lang_code, ',' ORDER BY sort_order) FROM logistics.supported_languages WHERE is_primary_search_language) AS primary_langs,
  (SELECT count(*) FROM logistics.taxonomy_nodes) AS taxonomy_nodes,
  (SELECT count(*) FROM logistics.taxonomy_node_translations) AS taxonomy_node_translations,
  (SELECT count(*) FROM logistics.taxonomy_keywords) AS taxonomy_keywords,
  (SELECT count(*) FROM logistics.taxonomy_search_documents) AS taxonomy_search_documents,
  (SELECT count(*) FROM logistics.taxonomy_closure) AS taxonomy_closure_rows;

\echo == PATCH 007_R2B / CHANGED SERVICE ROWS SNAPSHOT ==
SELECT
  p.sort_order,
  p.lang_code,
  p.english_name || ' / ' || p.turkish_name AS language_name,
  p.node_code,
  p.proposal_role,
  p.current_title,
  p.proposed_title,
  p.current_keyword,
  p.proposed_keyword,
  logistics.normalize_taxonomy_text(p.proposed_keyword) AS proposed_keyword_normalized
FROM _patch007_proposal AS p
ORDER BY
  p.sort_order,
  p.current_keyword_normalized,
  p.node_code;

DO $$
DECLARE
  v_translation_updates int;
  v_keyword_updates int;
  v_duplicate_after int;
  v_target_duplicate_after int;
  v_semantic_rows int;
  v_semantic_failures int;
  v_counts text;
  v_blank_count int;
  v_orphan_count int;
  v_marker_count int;
  v_required_function_count int;
BEGIN
  SELECT count(*) INTO v_translation_updates
  FROM _patch007_proposal AS p
  JOIN logistics.taxonomy_node_translations AS t
    ON t.node_id = p.node_id
   AND t.lang_code = p.lang_code
   AND t.title = p.proposed_title;

  SELECT count(*) INTO v_keyword_updates
  FROM _patch007_proposal AS p
  JOIN logistics.taxonomy_keywords AS k
    ON k.node_id = p.node_id
   AND k.lang_code = p.lang_code
   AND k.keyword_type = 'primary'
   AND k.is_official = true
   AND k.is_negative = false
   AND k.keyword = p.proposed_keyword;

  SELECT count(*) INTO v_duplicate_after
  FROM _patch007_duplicate_after;

  SELECT count(*) INTO v_target_duplicate_after
  FROM _patch007_duplicate_after AS d
  WHERE EXISTS (
    SELECT 1
    FROM logistics.taxonomy_keywords AS k
    JOIN logistics.taxonomy_nodes AS n
      ON n.id = k.node_id
    WHERE k.lang_code = d.lang_code
      AND k.keyword_normalized = d.keyword_normalized
      AND n.node_code IN ('1.1','1.2','5.1','9.2')
      AND k.keyword_type = 'primary'
      AND k.is_official = true
      AND k.is_negative = false
  );

  SELECT count(*) INTO v_semantic_rows
  FROM _patch007_semantic_result;

  SELECT count(*) INTO v_semantic_failures
  FROM _patch007_semantic_result
  WHERE NOT expected_top_match;

  SELECT
    (SELECT count(*) FROM logistics.supported_languages)::text || '|' ||
    (SELECT count(*) FROM logistics.supported_languages WHERE is_active)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_nodes)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_node_translations)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_keywords)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_search_documents)::text || '|' ||
    (SELECT count(*) FROM logistics.taxonomy_closure)::text
  INTO v_counts;

  SELECT
    (
      SELECT count(*)
      FROM logistics.taxonomy_node_translations
      WHERE title IS NULL OR btrim(title) = ''
    )
    +
    (
      SELECT count(*)
      FROM logistics.taxonomy_keywords
      WHERE keyword IS NULL OR btrim(keyword) = ''
    )
  INTO v_blank_count;

  SELECT
    (
      SELECT count(*)
      FROM logistics.taxonomy_node_translations AS t
      LEFT JOIN logistics.taxonomy_nodes AS n
        ON n.id = t.node_id
      LEFT JOIN logistics.supported_languages AS sl
        ON sl.lang_code = t.lang_code
      WHERE n.id IS NULL OR sl.lang_code IS NULL
    )
    +
    (
      SELECT count(*)
      FROM logistics.taxonomy_keywords AS k
      LEFT JOIN logistics.taxonomy_nodes AS n
        ON n.id = k.node_id
      LEFT JOIN logistics.supported_languages AS sl
        ON sl.lang_code = k.lang_code
      WHERE n.id IS NULL OR sl.lang_code IS NULL
    )
    +
    (
      SELECT count(*)
      FROM logistics.taxonomy_search_documents AS sd
      LEFT JOIN logistics.taxonomy_nodes AS n
        ON n.id = sd.node_id
      LEFT JOIN logistics.supported_languages AS sl
        ON sl.lang_code = sd.lang_code
      WHERE n.id IS NULL OR sl.lang_code IS NULL
    )
  INTO v_orphan_count;

  SELECT
    (
      SELECT count(*)
      FROM logistics.taxonomy_node_translations
      WHERE title ~* '(TODO|TBD|PLACEHOLDER|OVERLAY)'
    )
    +
    (
      SELECT count(*)
      FROM logistics.taxonomy_keywords
      WHERE keyword ~* '(TODO|TBD|PLACEHOLDER|OVERLAY)'
    )
  INTO v_marker_count;

  SELECT count(*) INTO v_required_function_count
  FROM pg_proc AS p
  JOIN pg_namespace AS ns
    ON ns.oid = p.pronamespace
  WHERE ns.nspname = 'logistics'
    AND p.proname IN (
      'normalize_taxonomy_text',
      'taxonomy_node_translations_prepare',
      'taxonomy_keywords_prepare'
    );

  IF v_translation_updates <> 73 THEN
    RAISE EXCEPTION 'expected 73 translation rows updated, got %', v_translation_updates;
  END IF;

  IF v_keyword_updates <> 73 THEN
    RAISE EXCEPTION 'expected 73 primary keyword rows updated, got %', v_keyword_updates;
  END IF;

  IF v_duplicate_after <> 0 THEN
    RAISE EXCEPTION 'duplicate normalized keyword groups remain after patch: %', v_duplicate_after;
  END IF;

  IF v_target_duplicate_after <> 0 THEN
    RAISE EXCEPTION 'target-related duplicate groups remain after patch: %', v_target_duplicate_after;
  END IF;

  IF v_semantic_rows <> 100 THEN
    RAISE EXCEPTION 'semantic expectation row count must be 100, got %', v_semantic_rows;
  END IF;

  IF v_semantic_failures <> 0 THEN
    RAISE EXCEPTION 'semantic failures after patch: %', v_semantic_failures;
  END IF;

  IF v_counts <> '25|25|335|8375|8375|8375|995' THEN
    RAISE EXCEPTION 'global count drift after patch: %', v_counts;
  END IF;

  IF v_blank_count <> 0 THEN
    RAISE EXCEPTION 'blank title/keyword count after patch: %', v_blank_count;
  END IF;

  IF v_orphan_count <> 0 THEN
    RAISE EXCEPTION 'orphan translation/keyword/search-document count after patch: %', v_orphan_count;
  END IF;

  IF v_marker_count <> 0 THEN
    RAISE EXCEPTION 'TODO/TBD/PLACEHOLDER/OVERLAY marker count after patch: %', v_marker_count;
  END IF;

  IF v_required_function_count <> 3 THEN
    RAISE EXCEPTION 'required logistics helper function count should be 3, got %', v_required_function_count;
  END IF;

  RAISE NOTICE 'TAXONOMY_DUPLICATE_REPAIR_007_R2B_HARD_ASSERTIONS=PASS';
END $$;

COMMIT;
