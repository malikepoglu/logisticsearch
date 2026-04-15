\set ON_ERROR_STOP on

-- EN
-- Taxonomy runtime prepare/load function surface for Pi51crawler.
-- This file promotes staging taxonomy material into the runtime logistics schema
-- and prepares the structures that crawler_core and parse_core will use.
--
-- Authority alignment rule:
-- The runtime function names must intentionally align with the proven authority
-- function family where possible:
--   - logistics.rebuild_taxonomy_closure()
--   - logistics.taxonomy_keywords_prepare()
--   - logistics.taxonomy_node_translations_prepare()
--
-- Current scope:
-- 1) text normalization helper
-- 2) translation prepare function
-- 3) keyword prepare function
-- 4) closure rebuild functions
-- 5) staging -> runtime controlled promotion function
--
-- TR
-- Pi51crawler için taxonomy runtime hazırlama/yükleme fonksiyon yüzeyi.
-- Bu dosya staging taxonomy materyalini runtime logistics şemasına taşır ve
-- crawler_core ile parse_core'un kullanacağı yapıları hazırlar.
--
-- Authority hizalama kuralı:
-- Runtime fonksiyon adları, mümkün olan yerlerde kanıtlanmış authority fonksiyon
-- ailesiyle bilinçli olarak hizalı olmalıdır:
--   - logistics.rebuild_taxonomy_closure()
--   - logistics.taxonomy_keywords_prepare()
--   - logistics.taxonomy_node_translations_prepare()
--
-- Güncel kapsam:
-- 1) metin normalize helper'ı
-- 2) translation prepare fonksiyonu
-- 3) keyword prepare fonksiyonu
-- 4) closure rebuild fonksiyonları
-- 5) staging -> runtime kontrollü promotion fonksiyonu

CREATE OR REPLACE FUNCTION logistics.normalize_taxonomy_text(p_text text)
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $function$
    SELECT NULLIF(
        regexp_replace(
            lower(btrim(coalesce(p_text, ''))),
            '\s+',
            ' ',
            'g'
        ),
        ''
    );
$function$;


CREATE OR REPLACE FUNCTION logistics.taxonomy_node_translations_prepare()
RETURNS bigint
LANGUAGE plpgsql
AS $function$
DECLARE
    v_rowcount bigint;
BEGIN
    UPDATE logistics.taxonomy_node_translations AS t
       SET title_normalized =
               COALESCE(logistics.normalize_taxonomy_text(t.title), ''),
           short_title_normalized =
               logistics.normalize_taxonomy_text(t.short_title),
           search_vector =
               setweight(
                   to_tsvector(
                       'simple',
                       coalesce(logistics.normalize_taxonomy_text(t.title), '')
                   ),
                   'A'
               )
               ||
               setweight(
                   to_tsvector(
                       'simple',
                       coalesce(logistics.normalize_taxonomy_text(t.short_title), '')
                   ),
                   'B'
               )
               ||
               setweight(
                   to_tsvector(
                       'simple',
                       coalesce(logistics.normalize_taxonomy_text(t.description), '')
                   ),
                   'C'
               ),
           updated_at = now();

    GET DIAGNOSTICS v_rowcount = ROW_COUNT;
    RETURN v_rowcount;
END;
$function$;


CREATE OR REPLACE FUNCTION logistics.taxonomy_keywords_prepare()
RETURNS bigint
LANGUAGE plpgsql
AS $function$
DECLARE
    v_rowcount bigint;
BEGIN
    UPDATE logistics.taxonomy_keywords AS k
       SET keyword_normalized =
               COALESCE(logistics.normalize_taxonomy_text(k.keyword), ''),
           search_vector =
               setweight(
                   to_tsvector(
                       'simple',
                       coalesce(logistics.normalize_taxonomy_text(k.keyword), '')
                   ),
                   'A'
               ),
           updated_at = now();

    GET DIAGNOSTICS v_rowcount = ROW_COUNT;
    RETURN v_rowcount;
END;
$function$;


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
        FROM logistics.taxonomy_nodes AS n

        UNION ALL

        SELECT
            cb.ancestor_id,
            child.id AS descendant_id,
            cb.depth + 1 AS depth
        FROM closure_build AS cb
        JOIN logistics.taxonomy_nodes AS child
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


CREATE OR REPLACE FUNCTION logistics.rebuild_taxonomy_overlay_closure()
RETURNS bigint
LANGUAGE plpgsql
AS $function$
DECLARE
    v_rowcount bigint;
BEGIN
    TRUNCATE TABLE logistics.taxonomy_overlay_closure;

    WITH RECURSIVE closure_build AS (
        SELECT
            n.id AS ancestor_id,
            n.id AS descendant_id,
            0    AS depth
        FROM logistics.taxonomy_overlay_nodes AS n

        UNION ALL

        SELECT
            cb.ancestor_id,
            child.id AS descendant_id,
            cb.depth + 1 AS depth
        FROM closure_build AS cb
        JOIN logistics.taxonomy_overlay_nodes AS child
          ON child.parent_id = cb.descendant_id
    )
    INSERT INTO logistics.taxonomy_overlay_closure (
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
          AND table_name = 'taxonomy_nodes_raw'
    ) THEN
        RAISE EXCEPTION 'staging.taxonomy_nodes_raw is missing';
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

    INSERT INTO logistics.taxonomy_nodes (
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
    FROM staging.taxonomy_nodes_raw AS s
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
    JOIN logistics.taxonomy_nodes AS n
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
    JOIN logistics.taxonomy_nodes AS n
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
        pg_get_serial_sequence('logistics.taxonomy_nodes', 'id'),
        greatest(coalesce((SELECT max(id) FROM logistics.taxonomy_nodes), 1), 1),
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
             FROM logistics.taxonomy_nodes),
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

-- EN
-- This file intentionally creates the preparation and promotion functions only.
-- Live apply and fingerprint verification come in the controlled apply/audit steps.
--
-- TR
-- Bu dosya bilinçli olarak yalnızca hazırlama ve promotion fonksiyonlarını oluşturur.
-- Canlı apply ve fingerprint doğrulaması kontrollü apply/audit adımlarında gelir.
