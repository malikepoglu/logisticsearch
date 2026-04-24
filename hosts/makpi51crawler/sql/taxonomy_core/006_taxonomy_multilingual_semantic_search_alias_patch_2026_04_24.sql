\set ON_ERROR_STOP on
\pset pager off
\pset format aligned

BEGIN;

\echo == PATCH 006 R5 / LANGUAGE SCOPE ==
SELECT 'ALL_25_LANGUAGES' AS active_language_scope,
       'ar,bg,cs,de,el,en,es,fr,hu,it,ja,ko,nl,pt,ro,ru,tr,zh,hi,bn,ur,uk,id,vi,he' AS active_language_codes;

CREATE TEMP TABLE patch006_targets (
  lang_code text NOT NULL,
  node_code text NOT NULL,
  new_title text NOT NULL,
  new_keyword text NOT NULL,
  semantic_role text NOT NULL,
  PRIMARY KEY (lang_code, node_code)
) ON COMMIT DROP;

INSERT INTO patch006_targets (lang_code, node_code, new_title, new_keyword, semantic_role) VALUES
('ar','1.1','النقل البري','نقل الشاحنات','road_title_truck_keyword'),
('ar','1.2','النقل البحري','النقل البحري','sea_title_sea_keyword'),
('ar','5.1','برمجيات اللوجستيات','برمجيات اللوجستيات','software_title_software_keyword'),
('ar','9.2','السفن البحرية','السفن البحرية','marine_vessels_disambiguation'),
('bg','1.1','автомобилен транспорт','транспорт с камиони','road_title_truck_keyword'),
('bg','1.2','морски транспорт','морски транспорт','sea_title_sea_keyword'),
('bg','5.1','софтуерни решения','софтуерни решения','software_title_software_keyword'),
('bg','9.2','морски плавателни съдове','морски плавателни съдове','marine_vessels_disambiguation'),
('cs','1.1','silniční doprava','kamionová doprava','road_title_truck_keyword'),
('cs','1.2','námořní doprava','námořní doprava','sea_title_sea_keyword'),
('cs','5.1','softwarová řešení','softwarová řešení','software_title_software_keyword'),
('cs','9.2','námořní plavidla','námořní plavidla','marine_vessels_disambiguation'),
('de','1.1','Straßengütertransport','Lkw-Transport','road_title_truck_keyword'),
('de','1.2','Seefracht','Seefracht','sea_title_sea_keyword'),
('de','5.1','Softwarelösungen','Softwarelösungen','software_title_software_keyword'),
('de','9.2','Seeschiffe','Seeschiffe','marine_vessels_disambiguation'),
('el','1.1','οδικές εμπορευματικές μεταφορές','μεταφορά με φορτηγό','road_title_truck_keyword'),
('el','1.2','θαλάσσιες μεταφορές','θαλάσσιες μεταφορές','sea_title_sea_keyword'),
('el','5.1','λογισμικό logistics','λογισμικό logistics','software_title_software_keyword'),
('el','9.2','θαλάσσια σκάφη','θαλάσσια σκάφη','marine_vessels_disambiguation'),
('en','1.1','Road Freight & Truck Transport','Road Freight','road_title_truck_keyword'),
('en','1.2','Sea Freight & Maritime Transport','Sea Freight','sea_title_sea_keyword'),
('en','5.1','Logistics Software & Digital Systems','Logistics Software','software_title_software_keyword'),
('en','9.2','Marine Vessels','Marine Vessels','marine_vessels_disambiguation'),
('es','1.1','transporte por carretera','transporte en camión','road_title_truck_keyword'),
('es','1.2','transporte marítimo','transporte marítimo','sea_title_sea_keyword'),
('es','5.1','soluciones de software','soluciones de software','software_title_software_keyword'),
('es','9.2','embarcaciones marítimas','embarcaciones marítimas','marine_vessels_disambiguation'),
('fr','1.1','transport routier','transport par camion','road_title_truck_keyword'),
('fr','1.2','transport maritime','transport maritime','sea_title_sea_keyword'),
('fr','5.1','solutions logicielles','solutions logicielles','software_title_software_keyword'),
('fr','9.2','navires maritimes','navires maritimes','marine_vessels_disambiguation'),
('hu','1.1','közúti szállítás','teherautós szállítás','road_title_truck_keyword'),
('hu','1.2','tengeri szállítás','tengeri szállítás','sea_title_sea_keyword'),
('hu','5.1','szoftvermegoldások','szoftvermegoldások','software_title_software_keyword'),
('hu','9.2','tengeri hajók','tengeri hajók','marine_vessels_disambiguation'),
('it','1.1','trasporto su strada','trasporto camion','road_title_truck_keyword'),
('it','1.2','trasporto marittimo','trasporto marittimo','sea_title_sea_keyword'),
('it','5.1','soluzioni software','soluzioni software','software_title_software_keyword'),
('it','9.2','imbarcazioni marittime','imbarcazioni marittime','marine_vessels_disambiguation'),
('ja','1.1','道路貨物輸送','トラック輸送','road_title_truck_keyword'),
('ja','1.2','海上輸送','海上輸送','sea_title_sea_keyword'),
('ja','5.1','物流ソフトウェア','物流ソフトウェア','software_title_software_keyword'),
('ja','9.2','船舶','船舶','marine_vessels_disambiguation'),
('ko','1.1','도로 화물 운송','트럭 운송','road_title_truck_keyword'),
('ko','1.2','해상 운송','해상 운송','sea_title_sea_keyword'),
('ko','5.1','물류 소프트웨어','물류 소프트웨어','software_title_software_keyword'),
('ko','9.2','해양 선박','해양 선박','marine_vessels_disambiguation'),
('nl','1.1','wegtransport','vrachtwagentransport','road_title_truck_keyword'),
('nl','1.2','zeevaart','zeevaart','sea_title_sea_keyword'),
('nl','5.1','softwareoplossingen','softwareoplossingen','software_title_software_keyword'),
('nl','9.2','zeeschepen','zeeschepen','marine_vessels_disambiguation'),
('pt','1.1','transporte rodoviário','transporte por caminhão','road_title_truck_keyword'),
('pt','1.2','transporte marítimo','transporte marítimo','sea_title_sea_keyword'),
('pt','5.1','soluções de software','soluções de software','software_title_software_keyword'),
('pt','9.2','embarcações marítimas','embarcações marítimas','marine_vessels_disambiguation'),
('ro','1.1','transport rutier','transport cu camionul','road_title_truck_keyword'),
('ro','1.2','transport maritim','transport maritim','sea_title_sea_keyword'),
('ro','5.1','soluții software','soluții software','software_title_software_keyword'),
('ro','9.2','nave maritime','nave maritime','marine_vessels_disambiguation'),
('ru','1.1','автомобильные грузоперевозки','перевозка грузовиками','road_title_truck_keyword'),
('ru','1.2','морские перевозки','морские перевозки','sea_title_sea_keyword'),
('ru','5.1','логистическое программное обеспечение','логистическое программное обеспечение','software_title_software_keyword'),
('ru','9.2','морские суда','морские суда','marine_vessels_disambiguation'),
('tr','1.1','kara yolu taşımacılığı','kamyon taşımacılığı','road_title_truck_keyword'),
('tr','1.2','deniz taşımacılığı','deniz taşımacılığı','sea_title_sea_keyword'),
('tr','5.1','yazılım çözümleri','yazılım çözümleri','software_title_software_keyword'),
('tr','9.2','deniz taşıtları','deniz taşıtları','marine_vessels_disambiguation'),
('zh','1.1','公路货运','卡车运输','road_title_truck_keyword'),
('zh','1.2','海运','海运','sea_title_sea_keyword'),
('zh','5.1','物流软件','物流软件','software_title_software_keyword'),
('zh','9.2','海运船舶','海运船舶','marine_vessels_disambiguation'),
('hi','1.1','सड़क माल ढुलाई','ट्रक परिवहन','road_title_truck_keyword'),
('hi','1.2','समुद्री माल ढुलाई','समुद्री माल ढुलाई','sea_title_sea_keyword'),
('hi','5.1','लॉजिस्टिक्स सॉफ्टवेयर','लॉजिस्टिक्स सॉफ्टवेयर','software_title_software_keyword'),
('hi','9.2','समुद्री पोत','समुद्री पोत','marine_vessels_disambiguation'),
('bn','1.1','সড়ক মাল পরিবহন','ট্রাক পরিবহন','road_title_truck_keyword'),
('bn','1.2','সমুদ্র মাল পরিবহন','সমুদ্র মাল পরিবহন','sea_title_sea_keyword'),
('bn','5.1','লজিস্টিকস সফটওয়্যার','লজিস্টিকস সফটওয়্যার','software_title_software_keyword'),
('bn','9.2','সামুদ্রিক নৌযান','সামুদ্রিক নৌযান','marine_vessels_disambiguation'),
('ur','1.1','سڑک مال برداری','ٹرک ٹرانسپورٹ','road_title_truck_keyword'),
('ur','1.2','سمندری مال برداری','سمندری مال برداری','sea_title_sea_keyword'),
('ur','5.1','لاجسٹکس سافٹ ویئر','لاجسٹکس سافٹ ویئر','software_title_software_keyword'),
('ur','9.2','سمندری جہاز','سمندری جہاز','marine_vessels_disambiguation'),
('uk','1.1','автомобільні вантажні перевезення','вантажні перевезення вантажівками','road_title_truck_keyword'),
('uk','1.2','морські перевезення','морські перевезення','sea_title_sea_keyword'),
('uk','5.1','логістичне програмне забезпечення','логістичне програмне забезпечення','software_title_software_keyword'),
('uk','9.2','морські судна','морські судна','marine_vessels_disambiguation'),
('id','1.1','transportasi jalan','transportasi truk','road_title_truck_keyword'),
('id','1.2','angkutan laut','angkutan laut','sea_title_sea_keyword'),
('id','5.1','solusi perangkat lunak','solusi perangkat lunak','software_title_software_keyword'),
('id','9.2','kapal laut','kapal laut','marine_vessels_disambiguation'),
('vi','1.1','vận tải đường bộ','vận tải xe tải','road_title_truck_keyword'),
('vi','1.2','vận tải biển','vận tải biển','sea_title_sea_keyword'),
('vi','5.1','phần mềm logistics','phần mềm logistics','software_title_software_keyword'),
('vi','9.2','tàu biển','tàu biển','marine_vessels_disambiguation'),
('he','1.1','הובלה יבשתית','הובלת משאיות','road_title_truck_keyword'),
('he','1.2','הובלה ימית','הובלה ימית','sea_title_sea_keyword'),
('he','5.1','תוכנת לוגיסטיקה','תוכנת לוגיסטיקה','software_title_software_keyword'),
('he','9.2','כלי שיט ימיים','כלי שיט ימיים','marine_vessels_disambiguation');

CREATE TEMP TABLE patch006_pre_duplicate_count AS
SELECT count(*)::int AS duplicate_group_count
FROM (
  SELECT lang_code, keyword_normalized
  FROM logistics.taxonomy_keywords
  GROUP BY lang_code, keyword_normalized
  HAVING count(*) > 1
) AS d;

UPDATE logistics.taxonomy_node_translations AS t
SET title = p.new_title
FROM patch006_targets AS p
JOIN logistics.taxonomy_nodes AS n
  ON n.node_code = p.node_code
WHERE t.node_id = n.id
  AND t.lang_code = p.lang_code
  AND t.title IS DISTINCT FROM p.new_title;

UPDATE logistics.taxonomy_keywords AS k
SET keyword = p.new_keyword
FROM patch006_targets AS p
JOIN logistics.taxonomy_nodes AS n
  ON n.node_code = p.node_code
WHERE k.node_id = n.id
  AND k.lang_code = p.lang_code
  AND k.keyword_type = 'primary'
  AND k.is_official = true
  AND k.is_negative = false
  AND k.keyword IS DISTINCT FROM p.new_keyword;

SELECT logistics.taxonomy_node_translations_prepare() AS refreshed_translation_rows;
SELECT logistics.taxonomy_keywords_prepare() AS refreshed_keyword_rows;

CREATE TEMP TABLE patch006_queries (
  lang_code text NOT NULL,
  query_group text NOT NULL,
  query_text text NOT NULL,
  expected_node_code text NOT NULL,
  PRIMARY KEY (lang_code, query_group)
) ON COMMIT DROP;

INSERT INTO patch006_queries (lang_code, query_group, query_text, expected_node_code)
SELECT lang_code, 'road', new_title, '1.1' FROM patch006_targets WHERE node_code='1.1'
UNION ALL
SELECT lang_code, 'sea', new_title, '1.2' FROM patch006_targets WHERE node_code='1.2'
UNION ALL
SELECT lang_code, 'software', new_title, '5.1' FROM patch006_targets WHERE node_code='5.1'
UNION ALL
SELECT lang_code, 'truck',
       CASE WHEN lang_code='en' THEN 'truck transport' ELSE new_keyword END,
       '1.1'
FROM patch006_targets
WHERE node_code='1.1';

CREATE TEMP TABLE patch006_top_matches AS
WITH scored AS (
  SELECT
    q.lang_code,
    q.query_group,
    q.query_text,
    q.expected_node_code,
    n.node_code AS top_node_code,
    t.title,
    k.keyword AS positive_keywords,
    GREATEST(
      similarity(logistics.normalize_taxonomy_text(q.query_text), t.title_normalized),
      similarity(logistics.normalize_taxonomy_text(q.query_text), k.keyword_normalized)
    ) AS score
  FROM patch006_queries AS q
  JOIN logistics.taxonomy_node_translations AS t
    ON t.lang_code = q.lang_code
  JOIN logistics.taxonomy_nodes AS n
    ON n.id = t.node_id
  JOIN logistics.taxonomy_keywords AS k
    ON k.node_id = n.id
   AND k.lang_code = q.lang_code
   AND k.keyword_type = 'primary'
   AND k.is_official = true
   AND k.is_negative = false
)
SELECT DISTINCT ON (lang_code, query_group)
  lang_code,
  query_group,
  query_text,
  expected_node_code,
  top_node_code,
  title,
  positive_keywords,
  round(score::numeric, 4) AS score,
  (top_node_code = expected_node_code) AS expected_top_match
FROM scored
ORDER BY lang_code, query_group, score DESC, top_node_code;

\echo == PATCH 006 R5 COMPACT LANGUAGE SUMMARY ==
SELECT
  sl.sort_order,
  sl.lang_code,
  sl.lang_name_en || ' / ' || sl.lang_name_tr AS language_name,
  count(*) FILTER (WHERE m.expected_top_match = false) AS failed_semantic_queries,
  count(*) AS tested_semantic_queries
FROM logistics.supported_languages AS sl
JOIN patch006_top_matches AS m
  ON m.lang_code = sl.lang_code
GROUP BY sl.sort_order, sl.lang_code, sl.lang_name_en, sl.lang_name_tr
ORDER BY sl.sort_order;

\echo == PATCH 006 R5 COMPACT GLOBAL COUNTS ==
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

\echo == PATCH 006 R5 COMPACT DUPLICATE SUMMARY ==
WITH post_dup AS (
  SELECT count(*)::int AS duplicate_group_count
  FROM (
    SELECT lang_code, keyword_normalized
    FROM logistics.taxonomy_keywords
    GROUP BY lang_code, keyword_normalized
    HAVING count(*) > 1
  ) AS d
),
target_dup AS (
  SELECT count(*)::int AS duplicate_group_count
  FROM (
    SELECT k.lang_code, k.keyword_normalized
    FROM logistics.taxonomy_keywords AS k
    JOIN (
      SELECT DISTINCT lang_code, logistics.normalize_taxonomy_text(new_keyword) AS keyword_normalized
      FROM patch006_targets
    ) AS p
      ON p.lang_code = k.lang_code
     AND p.keyword_normalized = k.keyword_normalized
    GROUP BY k.lang_code, k.keyword_normalized
    HAVING count(*) > 1
  ) AS d
)
SELECT
  pre.duplicate_group_count AS pre_duplicate_group_count,
  post_dup.duplicate_group_count AS post_duplicate_group_count,
  target_dup.duplicate_group_count AS target_related_duplicate_group_count
FROM patch006_pre_duplicate_count AS pre, post_dup, target_dup;

\echo == PATCH 006 R5 COMPACT HARD ASSERTIONS ==
DO $$
DECLARE
  v_supported_languages int;
  v_active_supported_languages int;
  v_canonical_order text;
  v_primary_langs text;
  v_nodes int;
  v_translations int;
  v_keywords int;
  v_search_documents int;
  v_closure int;
  v_functions int;
  v_validated_fks int;
  v_semantic_fail_count int;
  v_pre_dup int;
  v_post_dup int;
  v_target_dup int;
  v_missing_or_bad int;
  v_marker_count int;
BEGIN
  SELECT count(*) INTO v_supported_languages FROM logistics.supported_languages;
  SELECT count(*) INTO v_active_supported_languages FROM logistics.supported_languages WHERE is_active;
  SELECT string_agg(lang_code, ',' ORDER BY sort_order) INTO v_canonical_order FROM logistics.supported_languages WHERE is_active;
  SELECT string_agg(lang_code, ',' ORDER BY sort_order) INTO v_primary_langs FROM logistics.supported_languages WHERE is_primary_search_language;
  SELECT count(*) INTO v_nodes FROM logistics.taxonomy_nodes;
  SELECT count(*) INTO v_translations FROM logistics.taxonomy_node_translations;
  SELECT count(*) INTO v_keywords FROM logistics.taxonomy_keywords;
  SELECT count(*) INTO v_search_documents FROM logistics.taxonomy_search_documents;
  SELECT count(*) INTO v_closure FROM logistics.taxonomy_closure;

  SELECT count(*) INTO v_functions
  FROM pg_proc p
  JOIN pg_namespace n ON n.oid = p.pronamespace
  WHERE n.nspname = 'logistics'
    AND p.proname IN (
      'normalize_taxonomy_text',
      'rebuild_taxonomy_closure',
      'rebuild_taxonomy_overlay_closure',
      'refresh_taxonomy_runtime_from_staging',
      'taxonomy_keywords_prepare',
      'taxonomy_node_translations_prepare'
    );

  SELECT count(*) INTO v_validated_fks
  FROM pg_constraint c
  JOIN pg_class r ON r.oid = c.conrelid
  JOIN pg_namespace n ON n.oid = r.relnamespace
  WHERE n.nspname = 'logistics'
    AND c.contype = 'f'
    AND c.convalidated
    AND c.conname IN (
      'taxonomy_keywords_lang_code_fkey',
      'taxonomy_node_translations_lang_code_fkey',
      'taxonomy_overlay_keywords_lang_code_fkey',
      'taxonomy_overlay_node_translations_lang_code_fkey'
    );

  SELECT count(*) INTO v_semantic_fail_count
  FROM patch006_top_matches
  WHERE expected_top_match = false;

  SELECT duplicate_group_count INTO v_pre_dup FROM patch006_pre_duplicate_count;

  SELECT count(*) INTO v_post_dup
  FROM (
    SELECT lang_code, keyword_normalized
    FROM logistics.taxonomy_keywords
    GROUP BY lang_code, keyword_normalized
    HAVING count(*) > 1
  ) AS d;

  SELECT count(*) INTO v_target_dup
  FROM (
    SELECT k.lang_code, k.keyword_normalized
    FROM logistics.taxonomy_keywords AS k
    JOIN (
      SELECT DISTINCT lang_code, logistics.normalize_taxonomy_text(new_keyword) AS keyword_normalized
      FROM patch006_targets
    ) AS p
      ON p.lang_code = k.lang_code
     AND p.keyword_normalized = k.keyword_normalized
    GROUP BY k.lang_code, k.keyword_normalized
    HAVING count(*) > 1
  ) AS d;

  WITH bads AS (
    SELECT count(*) AS bad_count
    FROM logistics.taxonomy_nodes n
    CROSS JOIN logistics.supported_languages sl
    LEFT JOIN logistics.taxonomy_node_translations t
      ON t.node_id = n.id AND t.lang_code = sl.lang_code
    LEFT JOIN logistics.taxonomy_keywords k
      ON k.node_id = n.id
     AND k.lang_code = sl.lang_code
     AND k.keyword_type = 'primary'
     AND k.is_official = true
     AND k.is_negative = false
    LEFT JOIN logistics.taxonomy_search_documents sd
      ON sd.node_id = n.id AND sd.lang_code = sl.lang_code
    WHERE sl.is_active
      AND (
        t.node_id IS NULL
        OR k.node_id IS NULL
        OR sd.node_id IS NULL
        OR nullif(btrim(t.title), '') IS NULL
        OR nullif(btrim(t.title_normalized), '') IS NULL
        OR nullif(btrim(k.keyword), '') IS NULL
        OR nullif(btrim(k.keyword_normalized), '') IS NULL
      )
  )
  SELECT bad_count INTO v_missing_or_bad FROM bads;

  SELECT count(*) INTO v_marker_count
  FROM logistics.taxonomy_node_translations t
  WHERE t.title ~* '(overlay|todo|placeholder|fixme|tbd)';

  IF v_supported_languages <> 25 THEN RAISE EXCEPTION 'supported_languages bad: %', v_supported_languages; END IF;
  IF v_active_supported_languages <> 25 THEN RAISE EXCEPTION 'active_supported_languages bad: %', v_active_supported_languages; END IF;
  IF v_canonical_order <> 'ar,bg,cs,de,el,en,es,fr,hu,it,ja,ko,nl,pt,ro,ru,tr,zh,hi,bn,ur,uk,id,vi,he' THEN RAISE EXCEPTION 'canonical order bad: %', v_canonical_order; END IF;
  IF v_primary_langs <> 'en,tr' THEN RAISE EXCEPTION 'primary languages bad: %', v_primary_langs; END IF;
  IF v_nodes <> 335 THEN RAISE EXCEPTION 'taxonomy_nodes bad: %', v_nodes; END IF;
  IF v_translations <> 8375 THEN RAISE EXCEPTION 'translations bad: %', v_translations; END IF;
  IF v_keywords <> 8375 THEN RAISE EXCEPTION 'keywords bad: %', v_keywords; END IF;
  IF v_search_documents <> 8375 THEN RAISE EXCEPTION 'search_documents bad: %', v_search_documents; END IF;
  IF v_closure <> 995 THEN RAISE EXCEPTION 'closure bad: %', v_closure; END IF;
  IF v_functions <> 6 THEN RAISE EXCEPTION 'function count bad: %', v_functions; END IF;
  IF v_validated_fks <> 4 THEN RAISE EXCEPTION 'validated FK count bad: %', v_validated_fks; END IF;
  IF v_semantic_fail_count <> 0 THEN RAISE EXCEPTION 'semantic failures bad: %', v_semantic_fail_count; END IF;
  IF v_post_dup > v_pre_dup THEN RAISE EXCEPTION 'duplicate group count increased: pre %, post %', v_pre_dup, v_post_dup; END IF;
  IF v_target_dup <> 0 THEN RAISE EXCEPTION 'target-related duplicate groups bad: %', v_target_dup; END IF;
  IF v_missing_or_bad <> 0 THEN RAISE EXCEPTION 'missing/blank structural rows bad: %', v_missing_or_bad; END IF;
  IF v_marker_count <> 0 THEN RAISE EXCEPTION 'overlay/todo/placeholder marker count bad: %', v_marker_count; END IF;

  RAISE NOTICE 'TAXONOMY_DESKTOP_25LANG_SEMANTIC_ALIAS_PATCH_006_R5_HARD_ASSERTIONS=PASS';
END $$;

COMMIT;
