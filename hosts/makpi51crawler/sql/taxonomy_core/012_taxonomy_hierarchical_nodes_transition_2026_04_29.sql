-- TAXONOMY_HIERARCHICAL_NODES transition candidate.
-- EN: This SQL file is a migration candidate. It must be tested on a scratch database before any live DB transition.
-- TR: Bu SQL dosyası bir migration adayıdır. Canlı DB geçişinden önce mutlaka scratch veritabanında test edilmelidir.

-- EN: Canonical target table name.
-- TR: Kanonik hedef tablo adı.
--   logistics.taxonomy_hierarchical_nodes

-- EN: Legacy table name to retire.
-- TR: Emekliye ayrılacak eski tablo adı.
--   logistics.taxonomy_nodes

-- EN: permanent compatibility view/alias is rejected by this migration candidate.
-- TR: permanent compatibility view/alias bu migration adayında reddedilir.
-- EN: Permanent compatibility view/alias for logistics.taxonomy_nodes is intentionally not created.
-- TR: logistics.taxonomy_nodes için kalıcı compatibility view/alias bilinçli olarak oluşturulmaz.

BEGIN;

-- EN: Keep migration failures fast and bounded during scratch/live execution.
-- TR: Scratch/canlı çalıştırmada migration hatalarını hızlı ve sınırlı tutar.
SET LOCAL lock_timeout = '10s';
SET LOCAL statement_timeout = '5min';
SET LOCAL idle_in_transaction_session_timeout = '5min';

-- EN: Preflight guard. Old table must exist; canonical target must not exist yet.
-- TR: Ön kontrol. Eski tablo var olmalı; kanonik hedef henüz var olmamalı.
DO $$
BEGIN
  IF to_regclass('logistics.taxonomy_nodes') IS NULL THEN
    RAISE EXCEPTION 'Required legacy table is missing: logistics.taxonomy_nodes';
  END IF;

  IF to_regclass('logistics.taxonomy_hierarchical_nodes') IS NOT NULL THEN
    RAISE EXCEPTION 'Canonical target table already exists: logistics.taxonomy_hierarchical_nodes';
  END IF;

  IF to_regclass('logistics.taxonomy_hierarchies') IS NOT NULL THEN
    RAISE EXCEPTION 'Rejected ambiguous table unexpectedly exists: logistics.taxonomy_hierarchies';
  END IF;
END
$$;

-- EN: Snapshot critical row counts before the rename.
-- TR: Rename öncesi kritik satır sayılarını mühürler.
CREATE TEMP TABLE _ls_taxonomy_hierarchical_nodes_before_counts AS
SELECT object_name, row_count
FROM (
  SELECT 'logistics.taxonomy_nodes'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_nodes

  UNION ALL

  SELECT 'logistics.taxonomy_closure'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_closure

  UNION ALL

  SELECT 'logistics.taxonomy_node_translations'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_node_translations

  UNION ALL

  SELECT 'logistics.taxonomy_keywords'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_keywords

  UNION ALL

  SELECT 'logistics.taxonomy_search_documents'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_search_documents
) AS count_snapshot;

-- EN: Capture dependent function/procedure definitions before rename, then rewrite legacy names explicitly.
-- TR: Rename öncesi function/procedure tanımlarını yakalar ve eski isimleri açıkça yeni kanonik isme çevirir.
CREATE TEMP TABLE _ls_taxonomy_hierarchical_nodes_function_rebuild_queue AS
SELECT
  n.nspname AS schema_name,
  p.proname AS routine_name,
  pg_get_function_identity_arguments(p.oid) AS routine_arguments,
  replace(
    replace(
      pg_get_functiondef(p.oid),
      'taxonomy_nodes_raw',
      'taxonomy_hierarchical_nodes_raw'
    ),
    'taxonomy_nodes',
    'taxonomy_hierarchical_nodes'
  ) AS new_definition
FROM pg_proc AS p
JOIN pg_namespace AS n
  ON n.oid = p.pronamespace
WHERE n.nspname = 'logistics'
  AND p.prokind IN ('f', 'p')
  AND pg_get_functiondef(p.oid) LIKE '%taxonomy_nodes%';

-- EN: Capture dependent view definitions before rename, then rewrite legacy names explicitly.
-- TR: Rename öncesi view tanımlarını yakalar ve eski isimleri açıkça yeni kanonik isme çevirir.
CREATE TEMP TABLE _ls_taxonomy_hierarchical_nodes_view_rebuild_queue AS
SELECT
  n.nspname AS schema_name,
  c.relname AS view_name,
  format(
    'CREATE OR REPLACE VIEW %I.%I AS %s',
    n.nspname,
    c.relname,
    replace(pg_get_viewdef(c.oid, true), 'taxonomy_nodes', 'taxonomy_hierarchical_nodes')
  ) AS new_view_sql
FROM pg_class AS c
JOIN pg_namespace AS n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'logistics'
  AND c.relkind = 'v'
  AND pg_get_viewdef(c.oid, true) LIKE '%taxonomy_nodes%';

-- EN: Rename the real table to the canonical table name.
-- TR: Gerçek tabloyu kanonik tablo adına taşır.
ALTER TABLE logistics.taxonomy_nodes
RENAME TO taxonomy_hierarchical_nodes;

-- EN: Rename the owned sequence if it exists and bind it back to the renamed id column.
-- TR: Varsa bağlı sequence nesnesini yeniden adlandırır ve id kolonuna yeniden bağlar.
DO $$
BEGIN
  IF to_regclass('logistics.taxonomy_nodes_id_seq') IS NOT NULL THEN
    ALTER SEQUENCE logistics.taxonomy_nodes_id_seq
    RENAME TO taxonomy_hierarchical_nodes_id_seq;
  END IF;

  IF to_regclass('logistics.taxonomy_hierarchical_nodes_id_seq') IS NOT NULL THEN
    ALTER SEQUENCE logistics.taxonomy_hierarchical_nodes_id_seq
    OWNED BY logistics.taxonomy_hierarchical_nodes.id;

    ALTER TABLE logistics.taxonomy_hierarchical_nodes
    ALTER COLUMN id
    SET DEFAULT nextval('logistics.taxonomy_hierarchical_nodes_id_seq'::regclass);
  END IF;
END
$$;

-- EN: Rename constraints that still carry the old taxonomy_nodes identifier.
-- TR: Eski taxonomy_nodes kimliğini taşıyan constraint adlarını yeniden adlandırır.
DO $$
DECLARE
  r record;
  v_new_name text;
BEGIN
  FOR r IN
    SELECT
      conrelid,
      conrelid::regclass::text AS table_name,
      conname
    FROM pg_constraint
    WHERE conname LIKE '%taxonomy_nodes%'
      AND (
        conrelid = 'logistics.taxonomy_hierarchical_nodes'::regclass
        OR confrelid = 'logistics.taxonomy_hierarchical_nodes'::regclass
      )
    ORDER BY conname
  LOOP
    v_new_name := replace(r.conname, 'taxonomy_nodes', 'taxonomy_hierarchical_nodes');

    IF v_new_name <> r.conname THEN
      IF EXISTS (
        SELECT 1
        FROM pg_constraint AS existing
        WHERE existing.conrelid = r.conrelid
          AND existing.conname = v_new_name
      ) THEN
        RAISE EXCEPTION 'Constraint rename collision on %: % -> %', r.table_name, r.conname, v_new_name;
      END IF;

      EXECUTE format(
        'ALTER TABLE %s RENAME CONSTRAINT %I TO %I',
        r.table_name,
        r.conname,
        v_new_name
      );
    END IF;
  END LOOP;
END
$$;

-- EN: Rename indexes that still carry the old taxonomy_nodes identifier.
-- TR: Eski taxonomy_nodes kimliğini taşıyan index adlarını yeniden adlandırır.
DO $$
DECLARE
  r record;
  v_new_name text;
BEGIN
  FOR r IN
    SELECT
      ns.nspname AS schema_name,
      cls.relname AS index_name,
      format('%I.%I', ns.nspname, cls.relname) AS qualified_index_name
    FROM pg_class AS cls
    JOIN pg_namespace AS ns
      ON ns.oid = cls.relnamespace
    WHERE ns.nspname = 'logistics'
      AND cls.relkind = 'i'
      AND cls.relname LIKE '%taxonomy_nodes%'
    ORDER BY cls.relname
  LOOP
    v_new_name := replace(r.index_name, 'taxonomy_nodes', 'taxonomy_hierarchical_nodes');

    IF to_regclass(format('%I.%I', r.schema_name, v_new_name)) IS NOT NULL THEN
      RAISE EXCEPTION 'Index rename collision: %.% -> %', r.schema_name, r.index_name, v_new_name;
    END IF;

    EXECUTE format(
      'ALTER INDEX %s RENAME TO %I',
      r.qualified_index_name,
      v_new_name
    );
  END LOOP;
END
$$;

-- EN: Rename triggers that still carry the old taxonomy_nodes identifier.
-- TR: Eski taxonomy_nodes kimliğini taşıyan trigger adlarını yeniden adlandırır.
DO $$
DECLARE
  r record;
  v_new_name text;
BEGIN
  FOR r IN
    SELECT tgname
    FROM pg_trigger
    WHERE tgrelid = 'logistics.taxonomy_hierarchical_nodes'::regclass
      AND NOT tgisinternal
      AND tgname LIKE '%taxonomy_nodes%'
    ORDER BY tgname
  LOOP
    v_new_name := replace(r.tgname, 'taxonomy_nodes', 'taxonomy_hierarchical_nodes');

    EXECUTE format(
      'ALTER TRIGGER %I ON logistics.taxonomy_hierarchical_nodes RENAME TO %I',
      r.tgname,
      v_new_name
    );
  END LOOP;
END
$$;

-- EN: Rebuild captured functions/procedures with the canonical table/staging names.
-- TR: Yakalanan function/procedure tanımlarını kanonik tablo/staging isimleriyle yeniden kurar.
DO $$
DECLARE
  r record;
BEGIN
  FOR r IN
    SELECT new_definition
    FROM _ls_taxonomy_hierarchical_nodes_function_rebuild_queue
    ORDER BY schema_name, routine_name, routine_arguments
  LOOP
    EXECUTE r.new_definition;
  END LOOP;
END
$$;

-- EN: Rebuild captured views with the canonical table name.
-- TR: Yakalanan view tanımlarını kanonik tablo adıyla yeniden kurar.
DO $$
DECLARE
  r record;
BEGIN
  FOR r IN
    SELECT new_view_sql
    FROM _ls_taxonomy_hierarchical_nodes_view_rebuild_queue
    ORDER BY schema_name, view_name
  LOOP
    EXECUTE r.new_view_sql;
  END LOOP;
END
$$;

-- EN: Snapshot critical row counts after the rename/rebuild.
-- TR: Rename/rebuild sonrası kritik satır sayılarını yeniden mühürler.
CREATE TEMP TABLE _ls_taxonomy_hierarchical_nodes_after_counts AS
SELECT object_name, row_count
FROM (
  SELECT 'logistics.taxonomy_hierarchical_nodes'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_hierarchical_nodes

  UNION ALL

  SELECT 'logistics.taxonomy_closure'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_closure

  UNION ALL

  SELECT 'logistics.taxonomy_node_translations'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_node_translations

  UNION ALL

  SELECT 'logistics.taxonomy_keywords'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_keywords

  UNION ALL

  SELECT 'logistics.taxonomy_search_documents'::text AS object_name, count(*)::bigint AS row_count
  FROM logistics.taxonomy_search_documents
) AS count_snapshot;

-- EN: Validate old/new object state, row counts, and remaining legacy references.
-- TR: Eski/yeni nesne durumunu, satır sayılarını ve kalan legacy referansları doğrular.
DO $$
DECLARE
  v_hierarchical_node_count bigint;
  v_before_node_count bigint;
  v_after_mismatch_count bigint;
  v_old_table_exists boolean;
  v_target_table_exists boolean;
  v_old_named_class_count bigint;
  v_old_named_constraint_count bigint;
  v_old_named_trigger_count bigint;
  v_old_routine_reference_count bigint;
  v_old_view_reference_count bigint;
BEGIN
  v_old_table_exists := to_regclass('logistics.taxonomy_nodes') IS NOT NULL;
  v_target_table_exists := to_regclass('logistics.taxonomy_hierarchical_nodes') IS NOT NULL;

  IF v_old_table_exists THEN
    RAISE EXCEPTION 'Legacy table still resolves after migration: logistics.taxonomy_nodes';
  END IF;

  IF NOT v_target_table_exists THEN
    RAISE EXCEPTION 'Canonical table does not resolve after migration: logistics.taxonomy_hierarchical_nodes';
  END IF;

  SELECT row_count
  INTO v_before_node_count
  FROM _ls_taxonomy_hierarchical_nodes_before_counts
  WHERE object_name = 'logistics.taxonomy_nodes';

  SELECT count(*)::bigint
  INTO v_hierarchical_node_count
  FROM logistics.taxonomy_hierarchical_nodes;

  IF v_before_node_count <> v_hierarchical_node_count THEN
    RAISE EXCEPTION 'Node row count changed during rename: before %, after %', v_before_node_count, v_hierarchical_node_count;
  END IF;

  IF v_hierarchical_node_count <> 335 THEN
    RAISE EXCEPTION 'Unexpected hierarchical node row count: %', v_hierarchical_node_count;
  END IF;

  SELECT count(*)::bigint
  INTO v_after_mismatch_count
  FROM (
    SELECT
      b.object_name AS before_object_name,
      CASE
        WHEN b.object_name = 'logistics.taxonomy_nodes'
          THEN 'logistics.taxonomy_hierarchical_nodes'
        ELSE b.object_name
      END AS after_object_name,
      b.row_count AS before_count,
      a.row_count AS after_count
    FROM _ls_taxonomy_hierarchical_nodes_before_counts AS b
    LEFT JOIN _ls_taxonomy_hierarchical_nodes_after_counts AS a
      ON a.object_name = CASE
        WHEN b.object_name = 'logistics.taxonomy_nodes'
          THEN 'logistics.taxonomy_hierarchical_nodes'
        ELSE b.object_name
      END
    WHERE a.row_count IS DISTINCT FROM b.row_count
  ) AS mismatches;

  IF v_after_mismatch_count <> 0 THEN
    RAISE EXCEPTION 'Critical row count mismatch after migration: % mismatches', v_after_mismatch_count;
  END IF;

  SELECT count(*)::bigint
  INTO v_old_named_class_count
  FROM pg_class AS c
  JOIN pg_namespace AS n
    ON n.oid = c.relnamespace
  WHERE n.nspname = 'logistics'
    AND c.relname LIKE '%taxonomy_nodes%';

  IF v_old_named_class_count <> 0 THEN
    RAISE EXCEPTION 'Old taxonomy_nodes class names remain after migration: %', v_old_named_class_count;
  END IF;

  SELECT count(*)::bigint
  INTO v_old_named_constraint_count
  FROM pg_constraint
  WHERE conname LIKE '%taxonomy_nodes%';

  IF v_old_named_constraint_count <> 0 THEN
    RAISE EXCEPTION 'Old taxonomy_nodes constraint names remain after migration: %', v_old_named_constraint_count;
  END IF;

  SELECT count(*)::bigint
  INTO v_old_named_trigger_count
  FROM pg_trigger
  WHERE NOT tgisinternal
    AND tgname LIKE '%taxonomy_nodes%';

  IF v_old_named_trigger_count <> 0 THEN
    RAISE EXCEPTION 'Old taxonomy_nodes trigger names remain after migration: %', v_old_named_trigger_count;
  END IF;

  SELECT count(*)::bigint
  INTO v_old_routine_reference_count
  FROM pg_proc AS p
  JOIN pg_namespace AS n
    ON n.oid = p.pronamespace
  WHERE n.nspname = 'logistics'
    AND p.prokind IN ('f', 'p')
    AND pg_get_functiondef(p.oid) LIKE '%taxonomy_nodes%';

  IF v_old_routine_reference_count <> 0 THEN
    RAISE EXCEPTION 'Old taxonomy_nodes routine references remain after migration: %', v_old_routine_reference_count;
  END IF;

  SELECT count(*)::bigint
  INTO v_old_view_reference_count
  FROM pg_class AS c
  JOIN pg_namespace AS n
    ON n.oid = c.relnamespace
  WHERE n.nspname = 'logistics'
    AND c.relkind = 'v'
    AND pg_get_viewdef(c.oid, true) LIKE '%taxonomy_nodes%';

  IF v_old_view_reference_count <> 0 THEN
    RAISE EXCEPTION 'Old taxonomy_nodes view references remain after migration: %', v_old_view_reference_count;
  END IF;
END
$$;

-- EN: Emit a deterministic summary row for scratch/live audit logs.
-- TR: Scratch/canlı audit logları için deterministik özet satırı üretir.
SELECT
  'TAXONOMY_HIERARCHICAL_NODES_TRANSITION' AS migration_name,
  to_regclass('logistics.taxonomy_nodes') IS NULL AS legacy_table_removed,
  to_regclass('logistics.taxonomy_hierarchical_nodes') IS NOT NULL AS canonical_table_present,
  (SELECT count(*) FROM logistics.taxonomy_hierarchical_nodes) AS hierarchical_node_rows,
  (SELECT count(*) FROM logistics.taxonomy_closure) AS taxonomy_closure_rows,
  (SELECT count(*) FROM logistics.taxonomy_node_translations) AS taxonomy_node_translation_rows,
  (SELECT count(*) FROM logistics.taxonomy_keywords) AS taxonomy_keyword_rows,
  (SELECT count(*) FROM logistics.taxonomy_search_documents) AS taxonomy_search_document_rows;

-- =============================================================================
-- R4_R2_R2_DB_CATALOG_DEPENDENT_FUNCTION_AND_VIEW_REBUILD_REPAIR
-- =============================================================================
-- EN: This section rebuilds real dependent routine/view surfaces exported from
-- EN: the current Desktop PostgreSQL catalog in read-only mode.
-- TR: Bu bölüm, mevcut Desktop PostgreSQL catalog yüzeyinden read-only olarak
-- TR: çıkarılmış gerçek dependent function/view yüzeylerini yeniden kurar.
--
-- EN: Natural English explanation: hierarchical taxonomy nodes.
-- TR: Doğal İngilizce açıklama: hierarchical taxonomy nodes.
--
-- EN: Canonical technical identifier: TAXONOMY_HIERARCHICAL_NODES.
-- TR: Kanonik teknik kimlik: TAXONOMY_HIERARCHICAL_NODES.
--
-- EN: Canonical DB table after transition: logistics.taxonomy_hierarchical_nodes.
-- TR: Geçiş sonrası kanonik DB tablosu: logistics.taxonomy_hierarchical_nodes.
--
-- EN: Legacy table before transition: logistics.taxonomy_nodes.
-- TR: Geçiş öncesi legacy tablo: logistics.taxonomy_nodes.
--
-- EN: This candidate does not create a permanent compatibility view/alias for
-- EN: logistics.taxonomy_nodes.
-- TR: Bu aday, logistics.taxonomy_nodes için kalıcı compatibility view/alias
-- TR: oluşturmaz.

CREATE OR REPLACE FUNCTION logistics.rebuild_taxonomy_closure()
 RETURNS bigint
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_rowcount bigint;
BEGIN
    TRUNCATE TABLE logistics.taxonomy_closure;

    WITH RECURSIVE closure_build AS (
        SELECT
            n.id AS ancestor_id,
            n.id AS descendant_id,
            0    AS depth
        FROM logistics.taxonomy_hierarchical_nodes AS n

        UNION ALL

        SELECT
            cb.ancestor_id,
            child.id AS descendant_id,
            cb.depth + 1 AS depth
        FROM closure_build AS cb
        JOIN logistics.taxonomy_hierarchical_nodes AS child
          ON child.parent_id = cb.descendant_id
    )
    INSERT INTO logistics.taxonomy_closure (
        ancestor_id,
        descendant_id,
        depth
    )
    SELECT DISTINCT
        ancestor_id,
        descendant_id,
        depth
    FROM closure_build
    ORDER BY ancestor_id, descendant_id, depth;

    GET DIAGNOSTICS v_rowcount = ROW_COUNT;
    RETURN v_rowcount;
END;
$function$;

CREATE OR REPLACE FUNCTION logistics.refresh_taxonomy_runtime_from_staging()
 RETURNS jsonb
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_nodes_processed bigint;
    v_translations_processed bigint;
    v_keywords_processed bigint;
    v_translation_prepare_count bigint;
    v_keyword_prepare_count bigint;
    v_closure_count bigint;
    v_overlay_closure_count bigint;
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.schemata
        WHERE schema_name = 'staging'
    ) THEN
        RAISE EXCEPTION 'staging schema is missing';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'staging'
          AND table_name = 'taxonomy_hierarchical_nodes_raw'
    ) THEN
        RAISE EXCEPTION 'staging.taxonomy_hierarchical_nodes_raw is missing';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'staging'
          AND table_name = 'taxonomy_translations_raw'
    ) THEN
        RAISE EXCEPTION 'staging.taxonomy_translations_raw is missing';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'staging'
          AND table_name = 'taxonomy_keywords_raw'
    ) THEN
        RAISE EXCEPTION 'staging.taxonomy_keywords_raw is missing';
    END IF;

    INSERT INTO logistics.taxonomy_hierarchical_nodes (
        id,
        parent_id,
        node_code,
        level_no,
        sort_order,
        domain_type,
        node_kind,
        unspsc_code,
        unspsc_match_type,
        entity_scope,
        is_leaf,
        is_searchable,
        is_active,
        notes,
        metadata,
        created_at,
        updated_at
    )
    SELECT
        s.id,
        s.parent_id,
        s.node_code,
        s.level_no,
        coalesce(s.sort_order, 0),
        s.domain_type,
        s.node_kind,
        s.unspsc_code,
        coalesce(s.unspsc_match_type, 'unknown'),
        coalesce(s.entity_scope, '{}'::text[]),
        coalesce(s.is_leaf, false),
        coalesce(s.is_searchable, true),
        coalesce(s.is_active, true),
        s.notes,
        coalesce(s.metadata, '{}'::jsonb),
        coalesce(s.created_at, now()),
        coalesce(s.updated_at, now())
    FROM staging.taxonomy_hierarchical_nodes_raw AS s
    WHERE s.id IS NOT NULL
    ON CONFLICT (id) DO UPDATE
       SET parent_id = EXCLUDED.parent_id,
           node_code = EXCLUDED.node_code,
           level_no = EXCLUDED.level_no,
           sort_order = EXCLUDED.sort_order,
           domain_type = EXCLUDED.domain_type,
           node_kind = EXCLUDED.node_kind,
           unspsc_code = EXCLUDED.unspsc_code,
           unspsc_match_type = EXCLUDED.unspsc_match_type,
           entity_scope = EXCLUDED.entity_scope,
           is_leaf = EXCLUDED.is_leaf,
           is_searchable = EXCLUDED.is_searchable,
           is_active = EXCLUDED.is_active,
           notes = EXCLUDED.notes,
           metadata = EXCLUDED.metadata,
           created_at = EXCLUDED.created_at,
           updated_at = EXCLUDED.updated_at;

    GET DIAGNOSTICS v_nodes_processed = ROW_COUNT;

    INSERT INTO logistics.taxonomy_node_translations (
        id,
        node_id,
        lang_code,
        title,
        title_normalized,
        short_title,
        short_title_normalized,
        description,
        slug,
        search_vector,
        created_at,
        updated_at
    )
    SELECT
        s.id,
        s.node_id,
        s.lang_code,
        s.title,
        coalesce(logistics.normalize_taxonomy_text(s.title), ''),
        s.short_title,
        logistics.normalize_taxonomy_text(s.short_title),
        s.description,
        coalesce(s.slug, s.lang_code || '-' || s.node_id::text),
        NULL,
        coalesce(s.created_at, now()),
        coalesce(s.updated_at, now())
    FROM staging.taxonomy_translations_raw AS s
    JOIN logistics.taxonomy_hierarchical_nodes AS n
      ON n.id = s.node_id
    JOIN logistics.supported_languages AS l
      ON l.lang_code = s.lang_code
    WHERE s.id IS NOT NULL
    ON CONFLICT (id) DO UPDATE
       SET node_id = EXCLUDED.node_id,
           lang_code = EXCLUDED.lang_code,
           title = EXCLUDED.title,
           title_normalized = EXCLUDED.title_normalized,
           short_title = EXCLUDED.short_title,
           short_title_normalized = EXCLUDED.short_title_normalized,
           description = EXCLUDED.description,
           slug = EXCLUDED.slug,
           search_vector = EXCLUDED.search_vector,
           created_at = EXCLUDED.created_at,
           updated_at = EXCLUDED.updated_at;

    GET DIAGNOSTICS v_translations_processed = ROW_COUNT;

    INSERT INTO logistics.taxonomy_keywords (
        id,
        node_id,
        lang_code,
        keyword,
        keyword_normalized,
        keyword_type,
        weight,
        is_official,
        is_negative,
        search_vector,
        metadata,
        created_at,
        updated_at
    )
    SELECT
        s.id,
        s.node_id,
        s.lang_code,
        s.keyword,
        coalesce(logistics.normalize_taxonomy_text(s.keyword), ''),
        s.keyword_type,
        coalesce(s.weight, 1.0),
        coalesce(s.is_official, false),
        coalesce(s.is_negative, false),
        NULL,
        coalesce(s.metadata, '{}'::jsonb),
        coalesce(s.created_at, now()),
        coalesce(s.updated_at, now())
    FROM staging.taxonomy_keywords_raw AS s
    JOIN logistics.taxonomy_hierarchical_nodes AS n
      ON n.id = s.node_id
    JOIN logistics.supported_languages AS l
      ON l.lang_code = s.lang_code
    WHERE s.id IS NOT NULL
    ON CONFLICT (id) DO UPDATE
       SET node_id = EXCLUDED.node_id,
           lang_code = EXCLUDED.lang_code,
           keyword = EXCLUDED.keyword,
           keyword_normalized = EXCLUDED.keyword_normalized,
           keyword_type = EXCLUDED.keyword_type,
           weight = EXCLUDED.weight,
           is_official = EXCLUDED.is_official,
           is_negative = EXCLUDED.is_negative,
           search_vector = EXCLUDED.search_vector,
           metadata = EXCLUDED.metadata,
           created_at = EXCLUDED.created_at,
           updated_at = EXCLUDED.updated_at;

    GET DIAGNOSTICS v_keywords_processed = ROW_COUNT;

    PERFORM setval(
        pg_get_serial_sequence('logistics.taxonomy_hierarchical_nodes', 'id'),
        greatest(coalesce((SELECT max(id) FROM logistics.taxonomy_hierarchical_nodes), 1), 1),
        true
    );

    PERFORM setval(
        pg_get_serial_sequence('logistics.taxonomy_node_translations', 'id'),
        greatest(coalesce((SELECT max(id) FROM logistics.taxonomy_node_translations), 1), 1),
        true
    );

    PERFORM setval(
        pg_get_serial_sequence('logistics.taxonomy_keywords', 'id'),
        greatest(coalesce((SELECT max(id) FROM logistics.taxonomy_keywords), 1), 1),
        true
    );

    v_translation_prepare_count := logistics.taxonomy_node_translations_prepare();
    v_keyword_prepare_count := logistics.taxonomy_keywords_prepare();
    v_closure_count := logistics.rebuild_taxonomy_closure();
    v_overlay_closure_count := logistics.rebuild_taxonomy_overlay_closure();

    RETURN jsonb_build_object(
        'supported_language_count',
            (SELECT count(*)::bigint
             FROM logistics.supported_languages
             WHERE is_active),
        'node_count',
            (SELECT count(*)::bigint
             FROM logistics.taxonomy_hierarchical_nodes),
        'translation_count',
            (SELECT count(*)::bigint
             FROM logistics.taxonomy_node_translations),
        'keyword_count',
            (SELECT count(*)::bigint
             FROM logistics.taxonomy_keywords),
        'nodes_processed',
            v_nodes_processed,
        'translations_processed',
            v_translations_processed,
        'keywords_processed',
            v_keywords_processed,
        'translation_prepare_count',
            v_translation_prepare_count,
        'keyword_prepare_count',
            v_keyword_prepare_count,
        'closure_count',
            v_closure_count,
        'overlay_closure_count',
            v_overlay_closure_count
    );
END;
$function$;

CREATE OR REPLACE VIEW logistics.taxonomy_search_documents AS
 SELECT n.id AS node_id,
    n.node_code,
    n.parent_id,
    n.level_no,
    n.domain_type,
    n.node_kind,
    n.unspsc_code,
    n.unspsc_match_type,
    n.entity_scope,
    t.lang_code,
    t.title,
    t.title_normalized,
    t.short_title,
    t.slug,
    t.description,
    COALESCE(string_agg(DISTINCT
        CASE
            WHEN k.is_negative = false THEN k.keyword
            ELSE NULL::text
        END, ' '::text) FILTER (WHERE k.is_negative = false), ''::text) AS positive_keywords,
    COALESCE(string_agg(DISTINCT
        CASE
            WHEN k.is_negative = true THEN k.keyword
            ELSE NULL::text
        END, ' '::text) FILTER (WHERE k.is_negative = true), ''::text) AS negative_keywords
   FROM logistics.taxonomy_hierarchical_nodes n
     JOIN logistics.taxonomy_node_translations t ON t.node_id = n.id
     LEFT JOIN logistics.taxonomy_keywords k ON k.node_id = n.id AND k.lang_code = t.lang_code
  WHERE n.is_active = true
  GROUP BY n.id, n.node_code, n.parent_id, n.level_no, n.domain_type, n.node_kind, n.unspsc_code, n.unspsc_match_type, n.entity_scope, t.lang_code, t.title, t.title_normalized, t.short_title, t.slug, t.description;;

COMMIT;
