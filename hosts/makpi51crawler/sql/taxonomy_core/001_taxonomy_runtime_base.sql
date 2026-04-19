\set ON_ERROR_STOP on

-- EN
-- Taxonomy runtime base surface for Pi51crawler.
-- This file creates the runtime-ready logistics taxonomy layer that both
-- crawler_core and parse_core are expected to use.
--
-- Hard rule:
-- staging tables are not runtime truth.
-- Runtime truth must live in the logistics schema with constraints, indexes,
-- timestamps, and explicit language coverage.
--
-- Current scope of this file:
-- 1) create core runtime schema objects
-- 2) seed the supported 25-language registry
-- 3) create normalized runtime taxonomy tables
-- 4) create the first index and trigger safety layer
--
-- TR
-- Pi51crawler için taksonomi runtime temel yüzeyi.
-- Bu dosya, hem crawler_core hem parse_core tarafından kullanılması beklenen
-- runtime-hazır logistics taxonomy katmanını kurar.
--
-- Sert kural:
-- staging tablolar runtime doğrusu değildir.
-- Runtime doğrusu; constraints, indexes, timestamps ve açık dil kapsamı ile
-- logistics şemasında yaşamalıdır.
--
-- Bu dosyanın güncel kapsamı:
-- 1) çekirdek runtime şema nesnelerini oluşturmak
-- 2) desteklenen 25 dil kayıt katmanını tohumlamak
-- 3) normalize runtime taxonomy tablolarını oluşturmak
-- 4) ilk index ve trigger güvenlik katmanını kurmak

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE SCHEMA IF NOT EXISTS logistics;

CREATE OR REPLACE FUNCTION logistics.touch_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$function$;

CREATE TABLE IF NOT EXISTS logistics.supported_languages (
    lang_code text PRIMARY KEY,
    english_name text NOT NULL,
    native_name text NOT NULL,
    sort_order integer NOT NULL DEFAULT 0,
    is_active boolean NOT NULL DEFAULT true,
    is_primary_search_language boolean NOT NULL DEFAULT false,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT chk_supported_languages_lang_code_format
        CHECK (lang_code ~ '^[a-z]{2}$'),
    CONSTRAINT chk_supported_languages_sort_order_nonnegative
        CHECK (sort_order >= 0)
);

ALTER TABLE logistics.supported_languages
    ADD COLUMN IF NOT EXISTS sort_order integer;

ALTER TABLE logistics.supported_languages
    ALTER COLUMN sort_order SET DEFAULT 0;

UPDATE logistics.supported_languages
SET sort_order = 0
WHERE sort_order IS NULL;

ALTER TABLE logistics.supported_languages
    ALTER COLUMN sort_order SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'chk_supported_languages_sort_order_nonnegative'
          AND conrelid = 'logistics.supported_languages'::regclass
    ) THEN
        ALTER TABLE logistics.supported_languages
            ADD CONSTRAINT chk_supported_languages_sort_order_nonnegative
            CHECK (sort_order >= 0);
    END IF;
END
$$;

INSERT INTO logistics.supported_languages (
    lang_code,
    english_name,
    native_name,
    sort_order,
    is_active,
    is_primary_search_language
)
VALUES
    ('ar', 'Arabic',      'العربية',           1,  true, false),
    ('bg', 'Bulgarian',   'Български',         2,  true, false),
    ('cs', 'Czech',       'Čeština',           3,  true, false),
    ('de', 'German',      'Deutsch',           4,  true, false),
    ('el', 'Greek',       'Ελληνικά',          5,  true, false),
    ('en', 'English',     'English',           6,  true, true),
    ('es', 'Spanish',     'Español',           7,  true, false),
    ('fr', 'French',      'Français',          8,  true, false),
    ('hu', 'Hungarian',   'Magyar',            9,  true, false),
    ('it', 'Italian',     'Italiano',         10,  true, false),
    ('ja', 'Japanese',    '日本語',             11,  true, false),
    ('ko', 'Korean',      '한국어',             12,  true, false),
    ('nl', 'Dutch',       'Nederlands',       13,  true, false),
    ('pt', 'Portuguese',  'Português',        14,  true, false),
    ('ro', 'Romanian',    'Română',           15,  true, false),
    ('ru', 'Russian',     'Русский',          16,  true, false),
    ('tr', 'Turkish',     'Türkçe',           17,  true, true),
    ('zh', 'Chinese',     '中文',              18,  true, false),
    ('hi', 'Hindi',       'हिन्दी',           19,  true, false),
    ('bn', 'Bengali',     'বাংলা',            20,  true, false),
    ('ur', 'Urdu',        'اردو',             21,  true, false),
    ('uk', 'Ukrainian',   'Українська',       22,  true, false),
    ('id', 'Indonesian',  'Bahasa Indonesia', 23,  true, false),
    ('vi', 'Vietnamese',  'Tiếng Việt',       24,  true, false),
    ('he', 'Hebrew',      'עברית',            25,  true, false)
ON CONFLICT (lang_code) DO UPDATE
SET english_name = EXCLUDED.english_name,
    native_name = EXCLUDED.native_name,
    sort_order = EXCLUDED.sort_order,
    is_active = EXCLUDED.is_active,
    is_primary_search_language = EXCLUDED.is_primary_search_language,
    updated_at = now();


CREATE TABLE IF NOT EXISTS logistics.taxonomy_nodes (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    parent_id bigint NULL REFERENCES logistics.taxonomy_nodes(id) ON DELETE RESTRICT,
    node_code text NOT NULL UNIQUE,
    level_no smallint NOT NULL,
    sort_order integer NOT NULL DEFAULT 0,
    domain_type text NOT NULL,
    node_kind text NOT NULL,
    unspsc_code character varying(8),
    unspsc_match_type text NOT NULL DEFAULT 'unknown',
    entity_scope text[] NOT NULL DEFAULT '{}'::text[],
    is_leaf boolean NOT NULL DEFAULT false,
    is_searchable boolean NOT NULL DEFAULT true,
    is_active boolean NOT NULL DEFAULT true,
    notes text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT chk_taxonomy_nodes_node_code_not_blank CHECK (btrim(node_code) <> ''),
    CONSTRAINT chk_taxonomy_nodes_level_no_positive CHECK (level_no >= 1),
    CONSTRAINT chk_taxonomy_nodes_sort_order_nonnegative CHECK (sort_order >= 0),
    CONSTRAINT chk_taxonomy_nodes_no_self_parent CHECK (parent_id IS NULL OR parent_id <> id),
    CONSTRAINT chk_taxonomy_nodes_unspsc_format CHECK (
        unspsc_code IS NULL OR unspsc_code ~ '^[0-9]{8}$'
    )
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_node_translations (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    node_id bigint NOT NULL REFERENCES logistics.taxonomy_nodes(id) ON DELETE CASCADE,
    lang_code text NOT NULL REFERENCES logistics.supported_languages(lang_code) ON DELETE RESTRICT,
    title text NOT NULL,
    title_normalized text NOT NULL,
    short_title text,
    short_title_normalized text,
    description text,
    slug text NOT NULL,
    search_vector tsvector,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT uq_taxonomy_node_translations_node_lang UNIQUE (node_id, lang_code),
    CONSTRAINT uq_taxonomy_node_translations_lang_slug UNIQUE (lang_code, slug),
    CONSTRAINT chk_taxonomy_node_translations_title_not_blank CHECK (btrim(title) <> ''),
    CONSTRAINT chk_taxonomy_node_translations_title_normalized_not_blank CHECK (btrim(title_normalized) <> ''),
    CONSTRAINT chk_taxonomy_node_translations_slug_not_blank CHECK (btrim(slug) <> '')
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_keywords (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    node_id bigint NOT NULL REFERENCES logistics.taxonomy_nodes(id) ON DELETE CASCADE,
    lang_code text NOT NULL REFERENCES logistics.supported_languages(lang_code) ON DELETE RESTRICT,
    keyword text NOT NULL,
    keyword_normalized text NOT NULL,
    keyword_type text NOT NULL,
    weight numeric NOT NULL DEFAULT 1.0,
    is_official boolean NOT NULL DEFAULT false,
    is_negative boolean NOT NULL DEFAULT false,
    search_vector tsvector,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT uq_taxonomy_keywords_unique UNIQUE (node_id, lang_code, keyword_normalized),
    CONSTRAINT chk_taxonomy_keywords_keyword_not_blank CHECK (btrim(keyword) <> ''),
    CONSTRAINT chk_taxonomy_keywords_keyword_normalized_not_blank CHECK (btrim(keyword_normalized) <> ''),
    CONSTRAINT chk_taxonomy_keywords_keyword_type_not_blank CHECK (btrim(keyword_type) <> ''),
    CONSTRAINT chk_taxonomy_keywords_weight_positive CHECK (weight > 0)
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_closure (
    ancestor_id bigint NOT NULL REFERENCES logistics.taxonomy_nodes(id) ON DELETE CASCADE,
    descendant_id bigint NOT NULL REFERENCES logistics.taxonomy_nodes(id) ON DELETE CASCADE,
    depth integer NOT NULL,
    CONSTRAINT taxonomy_closure_pkey PRIMARY KEY (ancestor_id, descendant_id),
    CONSTRAINT chk_taxonomy_closure_depth_nonnegative CHECK (depth >= 0)
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_overlay_nodes (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    parent_id bigint NULL REFERENCES logistics.taxonomy_overlay_nodes(id) ON DELETE RESTRICT,
    node_code text NOT NULL UNIQUE,
    level_no smallint NOT NULL,
    sort_order integer NOT NULL DEFAULT 0,
    overlay_family text NOT NULL,
    domain_type text NOT NULL,
    node_kind text NOT NULL,
    unspsc_code character varying(8),
    unspsc_match_type text,
    entity_scope text[] NOT NULL DEFAULT '{}'::text[],
    is_leaf boolean NOT NULL DEFAULT false,
    is_searchable boolean NOT NULL DEFAULT false,
    is_active boolean NOT NULL DEFAULT false,
    is_passive boolean NOT NULL DEFAULT true,
    notes text NOT NULL DEFAULT '',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT chk_taxonomy_overlay_nodes_node_code_not_blank CHECK (btrim(node_code) <> ''),
    CONSTRAINT chk_taxonomy_overlay_nodes_level_no_positive CHECK (level_no >= 1),
    CONSTRAINT chk_taxonomy_overlay_nodes_sort_order_nonnegative CHECK (sort_order >= 0),
    CONSTRAINT chk_taxonomy_overlay_nodes_no_self_parent CHECK (parent_id IS NULL OR parent_id <> id),
    CONSTRAINT chk_taxonomy_overlay_nodes_unspsc_format CHECK (
        unspsc_code IS NULL OR unspsc_code ~ '^[0-9]{8}$'
    )
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_overlay_node_translations (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    node_id bigint NOT NULL REFERENCES logistics.taxonomy_overlay_nodes(id) ON DELETE CASCADE,
    lang_code text NOT NULL REFERENCES logistics.supported_languages(lang_code) ON DELETE RESTRICT,
    title text NOT NULL,
    title_normalized text,
    short_title text,
    short_title_normalized text,
    description text,
    slug text,
    search_vector tsvector,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT uq_taxonomy_overlay_node_translations_node_lang UNIQUE (node_id, lang_code),
    CONSTRAINT chk_taxonomy_overlay_node_translations_title_not_blank CHECK (btrim(title) <> '')
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_overlay_keywords (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    node_id bigint NOT NULL REFERENCES logistics.taxonomy_overlay_nodes(id) ON DELETE CASCADE,
    lang_code text NOT NULL REFERENCES logistics.supported_languages(lang_code) ON DELETE RESTRICT,
    keyword text NOT NULL,
    keyword_normalized text NOT NULL,
    keyword_type text NOT NULL,
    weight numeric NOT NULL DEFAULT 1.0,
    is_official boolean NOT NULL DEFAULT false,
    is_negative boolean NOT NULL DEFAULT false,
    search_vector tsvector,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT taxonomy_overlay_keywords_dedupe_uq UNIQUE (
        node_id, lang_code, keyword, keyword_type, is_official, is_negative
    ),
    CONSTRAINT chk_taxonomy_overlay_keywords_keyword_not_blank CHECK (btrim(keyword) <> ''),
    CONSTRAINT chk_taxonomy_overlay_keywords_keyword_normalized_not_blank CHECK (btrim(keyword_normalized) <> ''),
    CONSTRAINT chk_taxonomy_overlay_keywords_keyword_type_not_blank CHECK (btrim(keyword_type) <> ''),
    CONSTRAINT chk_taxonomy_overlay_keywords_weight_positive CHECK (weight > 0)
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_overlay_closure (
    ancestor_id bigint NOT NULL REFERENCES logistics.taxonomy_overlay_nodes(id) ON DELETE CASCADE,
    descendant_id bigint NOT NULL REFERENCES logistics.taxonomy_overlay_nodes(id) ON DELETE CASCADE,
    depth integer NOT NULL,
    CONSTRAINT taxonomy_overlay_closure_pkey PRIMARY KEY (ancestor_id, descendant_id),
    CONSTRAINT chk_taxonomy_overlay_closure_depth_nonnegative CHECK (depth >= 0)
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_requirements (
    id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    node_id bigint NOT NULL REFERENCES logistics.taxonomy_nodes(id) ON DELETE CASCADE,
    requirement_type text NOT NULL,
    requirement_code text,
    requirement_name text NOT NULL,
    issuer_name text,
    country_code character(2),
    is_mandatory boolean NOT NULL DEFAULT false,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT chk_taxonomy_requirements_type_not_blank CHECK (btrim(requirement_type) <> ''),
    CONSTRAINT chk_taxonomy_requirements_name_not_blank CHECK (btrim(requirement_name) <> '')
);

CREATE INDEX IF NOT EXISTS idx_taxonomy_nodes_parent_id
    ON logistics.taxonomy_nodes (parent_id);

CREATE INDEX IF NOT EXISTS idx_taxonomy_nodes_domain_type
    ON logistics.taxonomy_nodes (domain_type);

CREATE INDEX IF NOT EXISTS idx_taxonomy_nodes_unspsc_code
    ON logistics.taxonomy_nodes (unspsc_code);

CREATE INDEX IF NOT EXISTS idx_taxonomy_nodes_entity_scope_gin
    ON logistics.taxonomy_nodes USING gin (entity_scope);

CREATE INDEX IF NOT EXISTS idx_taxonomy_node_translations_node_lang
    ON logistics.taxonomy_node_translations (node_id, lang_code);

CREATE INDEX IF NOT EXISTS idx_taxonomy_node_translations_slug
    ON logistics.taxonomy_node_translations (lang_code, slug);

CREATE INDEX IF NOT EXISTS idx_taxonomy_node_translations_title_trgm
    ON logistics.taxonomy_node_translations USING gin (title_normalized gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_taxonomy_node_translations_search_vector
    ON logistics.taxonomy_node_translations USING gin (search_vector);

CREATE INDEX IF NOT EXISTS idx_taxonomy_keywords_node_lang
    ON logistics.taxonomy_keywords (node_id, lang_code);

CREATE INDEX IF NOT EXISTS idx_taxonomy_keywords_keyword_trgm
    ON logistics.taxonomy_keywords USING gin (keyword_normalized gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_taxonomy_keywords_search_vector
    ON logistics.taxonomy_keywords USING gin (search_vector);

CREATE INDEX IF NOT EXISTS idx_taxonomy_closure_descendant
    ON logistics.taxonomy_closure (descendant_id, ancestor_id);

CREATE INDEX IF NOT EXISTS idx_taxonomy_overlay_nodes_parent_id
    ON logistics.taxonomy_overlay_nodes (parent_id);

CREATE INDEX IF NOT EXISTS idx_taxonomy_overlay_nodes_family_sort
    ON logistics.taxonomy_overlay_nodes (overlay_family, sort_order);

CREATE INDEX IF NOT EXISTS idx_taxonomy_overlay_nodes_code
    ON logistics.taxonomy_overlay_nodes (node_code);

CREATE INDEX IF NOT EXISTS idx_taxonomy_overlay_node_translations_node_lang
    ON logistics.taxonomy_overlay_node_translations (node_id, lang_code);

CREATE INDEX IF NOT EXISTS idx_taxonomy_overlay_keywords_node_lang
    ON logistics.taxonomy_overlay_keywords (node_id, lang_code);

CREATE INDEX IF NOT EXISTS idx_taxonomy_overlay_closure_descendant
    ON logistics.taxonomy_overlay_closure (descendant_id);

CREATE INDEX IF NOT EXISTS idx_taxonomy_requirements_node_id
    ON logistics.taxonomy_requirements (node_id);

DROP TRIGGER IF EXISTS trg_supported_languages_touch_updated_at
    ON logistics.supported_languages;
CREATE TRIGGER trg_supported_languages_touch_updated_at
BEFORE UPDATE ON logistics.supported_languages
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

DROP TRIGGER IF EXISTS trg_taxonomy_nodes_touch_updated_at
    ON logistics.taxonomy_nodes;
CREATE TRIGGER trg_taxonomy_nodes_touch_updated_at
BEFORE UPDATE ON logistics.taxonomy_nodes
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

DROP TRIGGER IF EXISTS trg_taxonomy_node_translations_touch_updated_at
    ON logistics.taxonomy_node_translations;
CREATE TRIGGER trg_taxonomy_node_translations_touch_updated_at
BEFORE UPDATE ON logistics.taxonomy_node_translations
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

DROP TRIGGER IF EXISTS trg_taxonomy_keywords_touch_updated_at
    ON logistics.taxonomy_keywords;
CREATE TRIGGER trg_taxonomy_keywords_touch_updated_at
BEFORE UPDATE ON logistics.taxonomy_keywords
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

DROP TRIGGER IF EXISTS trg_taxonomy_overlay_nodes_touch_updated_at
    ON logistics.taxonomy_overlay_nodes;
CREATE TRIGGER trg_taxonomy_overlay_nodes_touch_updated_at
BEFORE UPDATE ON logistics.taxonomy_overlay_nodes
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

DROP TRIGGER IF EXISTS trg_taxonomy_overlay_node_translations_touch_updated_at
    ON logistics.taxonomy_overlay_node_translations;
CREATE TRIGGER trg_taxonomy_overlay_node_translations_touch_updated_at
BEFORE UPDATE ON logistics.taxonomy_overlay_node_translations
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

DROP TRIGGER IF EXISTS trg_taxonomy_overlay_keywords_touch_updated_at
    ON logistics.taxonomy_overlay_keywords;
CREATE TRIGGER trg_taxonomy_overlay_keywords_touch_updated_at
BEFORE UPDATE ON logistics.taxonomy_overlay_keywords
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

DROP TRIGGER IF EXISTS trg_taxonomy_requirements_touch_updated_at
    ON logistics.taxonomy_requirements;
CREATE TRIGGER trg_taxonomy_requirements_touch_updated_at
BEFORE UPDATE ON logistics.taxonomy_requirements
FOR EACH ROW
EXECUTE FUNCTION logistics.touch_updated_at();

-- EN
-- This base layer intentionally does not yet load staging data into runtime.
-- That controlled promotion will live in later apply/prepare surfaces.
--
-- TR
-- Bu temel katman bilinçli olarak staging verisini henüz runtime'a yüklemez.
-- Bu kontrollü terfi, daha sonraki apply/prepare yüzeylerinde yaşayacaktır.
