-- SECTION1_WEBCRAWLER / TAXONOMY CORE SEMANTIC QUALITY PATCH
--
-- EN:
-- This patch improves user-facing taxonomy wording without changing the taxonomy
-- structure. It removes internal "Overlay" wording from selected user-visible
-- labels and strengthens a few English search-facing labels for common logistics
-- queries.
--
-- TR:
-- Bu patch taxonomy yapısını değiştirmeden kullanıcıya görünen metin kalitesini
-- iyileştirir. Seçili başlıklardan iç sistem işareti gibi duran "Overlay"
-- kelimesini kaldırır ve yaygın lojistik aramalar için birkaç İngilizce etiketi
-- güçlendirir.
--
-- Safety / Güvenlik:
-- - No table is dropped.
-- - No row is deleted.
-- - No row is inserted.
-- - Only title and primary keyword text values are updated.
-- - Normalized/search_vector fields are refreshed by canonical prepare functions.

BEGIN;

CREATE TEMP TABLE taxonomy_semantic_quality_patch_work (
  lang_code text NOT NULL,
  node_code text NOT NULL,
  new_title text NOT NULL,
  PRIMARY KEY (lang_code, node_code)
) ON COMMIT DROP;

INSERT INTO taxonomy_semantic_quality_patch_work (lang_code, node_code, new_title)
VALUES
  -- English semantic search strengthening.
  ('en', '1.1', 'Road Freight & Truck Transport'),
  ('en', '1.2', 'Sea Freight & Maritime Transport'),
  ('en', '5.1', 'Logistics Software & Digital Systems'),

  -- English overlay marker cleanup.
  ('en', '10', 'Charter, Rental & Leasing Services'),
  ('en', '10.1', 'Charter Services'),
  ('en', '10.2', 'Rental Services'),
  ('en', '10.3', 'Leasing Services'),
  ('en', '11', 'Maintenance, Fueling, Storage & Support Services'),
  ('en', '11.7', 'Fleet Management Support'),

  -- Turkish overlay marker cleanup.
  ('tr', '10', 'Charter, Kiralama ve Leasing Hizmetleri'),
  ('tr', '10.1', 'Charter Hizmetleri'),
  ('tr', '10.2', 'Kiralama Hizmetleri'),
  ('tr', '10.3', 'Leasing Hizmetleri'),
  ('tr', '11', 'Bakım, Yakıt İkmali, Depolama ve Destek Hizmetleri'),
  ('tr', '11.7', 'Filo Yönetimi Desteği'),

  -- German overlay marker cleanup.
  ('de', '10', 'Charter-, Miet- und Leasingdienste'),
  ('de', '10.1', 'Charterdienste'),
  ('de', '10.2', 'Mietdienste'),
  ('de', '10.3', 'Leasingdienste'),
  ('de', '11', 'Wartung, Betankung, Lagerung und Support'),
  ('de', '11.7', 'Flottenmanagement-Support'),

  -- Bulgarian overlay marker cleanup.
  ('bg', '10', 'Чартър, наем и лизинг услуги'),
  ('bg', '10.1', 'Чартърни услуги'),
  ('bg', '10.2', 'Услуги за наем'),
  ('bg', '10.3', 'Лизингови услуги'),
  ('bg', '11', 'Поддръжка, зареждане, съхранение и оперативна подкрепа'),
  ('bg', '11.7', 'Подкрепа за управление на автопарк'),

  -- Czech overlay marker cleanup.
  ('cs', '10', 'Charterové, nájemní a leasingové služby'),
  ('cs', '10.1', 'Charterové služby'),
  ('cs', '10.2', 'Nájemní služby'),
  ('cs', '10.3', 'Leasingové služby'),
  ('cs', '11', 'Údržba, tankování, skladování a podpora'),
  ('cs', '11.7', 'Podpora správy vozového parku'),

  -- Spanish overlay marker cleanup.
  ('es', '10', 'Servicios de chárter, alquiler y leasing'),
  ('es', '10.1', 'Servicios chárter'),
  ('es', '10.2', 'Servicios de alquiler'),
  ('es', '10.3', 'Servicios de leasing'),
  ('es', '11', 'Servicios de mantenimiento, repostaje, almacenamiento y soporte'),
  ('es', '11.7', 'Soporte de gestión de flotas'),

  -- French overlay marker cleanup.
  ('fr', '10', 'Services d’affrètement, de location et de leasing'),
  ('fr', '10.1', 'Services d’affrètement'),
  ('fr', '10.2', 'Services de location'),
  ('fr', '10.3', 'Services de leasing'),
  ('fr', '11', 'Maintenance, ravitaillement, stockage et support'),
  ('fr', '11.7', 'Support à la gestion de flotte'),

  -- Hungarian overlay marker cleanup.
  ('hu', '10', 'Charter-, bérleti és lízingszolgáltatások'),
  ('hu', '10.1', 'Charter szolgáltatások'),
  ('hu', '10.2', 'Bérleti szolgáltatások'),
  ('hu', '10.3', 'Lízingszolgáltatások'),
  ('hu', '11', 'Karbantartás, üzemanyag-feltöltés, tárolás és támogatás'),
  ('hu', '11.7', 'Flottakezelési támogatás'),

  -- Italian overlay marker cleanup.
  ('it', '10', 'Servizi di charter, noleggio e leasing'),
  ('it', '10.1', 'Servizi charter'),
  ('it', '10.2', 'Servizi di noleggio'),
  ('it', '10.3', 'Servizi di leasing'),
  ('it', '11', 'Manutenzione, rifornimento, stoccaggio e supporto'),
  ('it', '11.7', 'Supporto alla gestione flotte'),

  -- Dutch overlay marker cleanup.
  ('nl', '10', 'Charter-, verhuur- en leasingdiensten'),
  ('nl', '10.1', 'Charterdiensten'),
  ('nl', '10.2', 'Verhuurdiensten'),
  ('nl', '10.3', 'Leasingdiensten'),
  ('nl', '11', 'Onderhoud, tanken, opslag en ondersteuning'),
  ('nl', '11.7', 'Ondersteuning voor wagenparkbeheer'),

  -- Portuguese overlay marker cleanup.
  ('pt', '10', 'Serviços de fretamento, aluguel e leasing'),
  ('pt', '10.1', 'Serviços de fretamento'),
  ('pt', '10.2', 'Serviços de aluguel'),
  ('pt', '10.3', 'Serviços de leasing'),
  ('pt', '11', 'Manutenção, abastecimento, armazenagem e suporte'),
  ('pt', '11.7', 'Suporte à gestão de frotas'),

  -- Romanian overlay marker cleanup.
  ('ro', '10', 'Servicii de charter, închiriere și leasing'),
  ('ro', '10.1', 'Servicii charter'),
  ('ro', '10.2', 'Servicii de închiriere'),
  ('ro', '10.3', 'Servicii de leasing'),
  ('ro', '11', 'Mentenanță, alimentare, depozitare și suport'),
  ('ro', '11.7', 'Suport pentru managementul flotei'),

  -- Indonesian overlay marker cleanup.
  ('id', '10', 'Layanan charter, sewa, dan leasing'),
  ('id', '10.1', 'Layanan charter'),
  ('id', '10.2', 'Layanan sewa'),
  ('id', '10.3', 'Layanan leasing'),
  ('id', '11', 'Perawatan, pengisian bahan bakar, penyimpanan, dan dukungan'),
  ('id', '11.7', 'Dukungan manajemen armada');

DO $$
DECLARE
  v_missing bigint;
BEGIN
  SELECT count(*)
  INTO v_missing
  FROM taxonomy_semantic_quality_patch_work AS p
  LEFT JOIN logistics.taxonomy_nodes AS n
    ON n.node_code = p.node_code
  LEFT JOIN logistics.taxonomy_node_translations AS t
    ON t.node_id = n.id
   AND t.lang_code = p.lang_code
  WHERE n.id IS NULL
     OR t.node_id IS NULL;

  IF v_missing <> 0 THEN
    RAISE EXCEPTION 'Semantic patch has % missing node/translation targets', v_missing;
  END IF;
END $$;

WITH patch AS (
  SELECT
    p.lang_code,
    p.node_code,
    p.new_title,
    n.id AS node_id
  FROM taxonomy_semantic_quality_patch_work AS p
  JOIN logistics.taxonomy_nodes AS n
    ON n.node_code = p.node_code
)
UPDATE logistics.taxonomy_node_translations AS t
SET title = patch.new_title
FROM patch
WHERE t.node_id = patch.node_id
  AND t.lang_code = patch.lang_code
  AND t.title IS DISTINCT FROM patch.new_title;

WITH patch AS (
  SELECT
    p.lang_code,
    p.node_code,
    p.new_title,
    n.id AS node_id
  FROM taxonomy_semantic_quality_patch_work AS p
  JOIN logistics.taxonomy_nodes AS n
    ON n.node_code = p.node_code
)
UPDATE logistics.taxonomy_keywords AS k
SET keyword = patch.new_title
FROM patch
WHERE k.node_id = patch.node_id
  AND k.lang_code = patch.lang_code
  AND k.keyword_type = 'primary'
  AND k.is_official = true
  AND k.is_negative = false
  AND k.keyword IS DISTINCT FROM patch.new_title;

SELECT logistics.taxonomy_node_translations_prepare() AS refreshed_translation_rows;
SELECT logistics.taxonomy_keywords_prepare() AS refreshed_keyword_rows;

DO $$
DECLARE
  v_mismatch bigint;
BEGIN
  WITH patch AS (
    SELECT
      p.lang_code,
      p.node_code,
      p.new_title,
      n.id AS node_id
    FROM taxonomy_semantic_quality_patch_work AS p
    JOIN logistics.taxonomy_nodes AS n
      ON n.node_code = p.node_code
  )
  SELECT count(*)
  INTO v_mismatch
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
  WHERE t.title IS DISTINCT FROM patch.new_title
     OR k.keyword IS DISTINCT FROM patch.new_title
     OR t.title_normalized IS DISTINCT FROM logistics.normalize_taxonomy_text(t.title)
     OR k.keyword_normalized IS DISTINCT FROM logistics.normalize_taxonomy_text(k.keyword)
     OR t.search_vector IS NULL
     OR k.search_vector IS NULL;

  IF v_mismatch <> 0 THEN
    RAISE EXCEPTION 'Semantic patch post-apply mismatch count is %, expected 0', v_mismatch;
  END IF;
END $$;

COMMIT;
