# EN: We enable postponed evaluation of annotations so type hints can stay
# EN: readable even when they refer to classes declared later in this file.
# TR: Type hint'ler bu dosyada daha sonra tanımlanan sınıflara referans verse
# TR: bile okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because small structured result objects are much
# EN: clearer than loose tuples or unnamed dictionaries.
# TR: Küçük yapılı sonuç nesneleri dağınık tuple veya isimsiz sözlüklere göre
# TR: çok daha açık olduğu için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import Path because filesystem path work is clearer and safer with
# EN: pathlib objects than with raw strings.
# TR: Filesystem path işlemleri pathlib nesneleriyle ham metinlere göre daha
# TR: açık ve daha güvenli olduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import os because writability checks use operating-system permission
# EN: probing.
# TR: Yazılabilirlik kontrolleri işletim sistemi izin probe'u kullandığı için
# TR: os modülünü içe aktarıyoruz.
import os


# EN: This constant expresses the user's canonical raw/working collection root.
# TR: Bu sabit, kullanıcının kanonik ham/çalışma veri toplama kökünü ifade eder.
RAW_COLLECTION_ROOT = Path("/srv/webcrawler/raw_fetch")

# EN: This constant is the first preferred destination for processed output.
# TR: Bu sabit işlenmiş çıktı için ilk tercih edilen hedeftir.
PROCESSED_PRIMARY_ROOT = Path("/srv/data")

# EN: This constant is the temporary fallback destination for processed output
# EN: when the primary root is not currently usable.
# TR: Bu sabit, birincil kök o anda kullanılamıyorsa işlenmiş çıktı için geçici
# TR: fallback hedeftir.
PROCESSED_FALLBACK_ROOT = Path("/srv/buffer")


# EN: This dataclass stores the observed state of one storage path.
# TR: Bu dataclass tek bir storage path'inin gözlenen durumunu tutar.
@dataclass(slots=True)
class StoragePathStatus:
    # EN: path is the filesystem path that was checked.
    # TR: path kontrol edilen filesystem path'idir.
    path: str

    # EN: exists tells whether the path exists at all.
    # TR: exists path'in hiç var olup olmadığını söyler.
    exists: bool

    # EN: is_dir tells whether the path is a directory.
    # TR: is_dir path'in bir dizin olup olmadığını söyler.
    is_dir: bool

    # EN: is_mount tells whether the path is currently a mountpoint.
    # TR: is_mount path'in şu anda bir mountpoint olup olmadığını söyler.
    is_mount: bool

    # EN: is_writable tells whether the current process appears able to write there.
    # TR: is_writable mevcut sürecin oraya yazabiliyor görünüp görünmediğini söyler.
    is_writable: bool

    # EN: reason stores a short explanation when the path is not usable.
    # TR: reason path kullanılamıyorsa kısa açıklama nedenini tutar.
    reason: str | None


# EN: This dataclass stores the minimal final storage decision for processed output.
# TR: Bu dataclass işlenmiş çıktı için asgari nihai storage kararını tutar.
@dataclass(slots=True)
class ProcessedOutputPlan:
    # EN: raw_collection_root is the canonical place where raw evidence
    # EN: accumulation lives.
    # TR: raw_collection_root ham kanıtın bulunduğu kanonik yerdir.
    raw_collection_root: str

    # EN: processed_output_root is the selected destination for normal processed
    # EN: output writes. It becomes None when crawler must pause first.
    # TR: processed_output_root normal işlenmiş çıktı yazımları için seçilen
    # TR: hedeftir. Crawler önce pause olmak zorundaysa None olur.
    processed_output_root: str | None

    # EN: using_fallback tells whether /srv/buffer was selected for normal writes.
    # TR: using_fallback normal yazımlar için /srv/buffer seçilip seçilmediğini söyler.
    using_fallback: bool

    # EN: buffer_backlog_present tells whether /srv/buffer currently appears to
    # EN: contain buffered processed-output backlog.
    # TR: buffer_backlog_present /srv/buffer içinde şu anda buffer işlenmiş çıktı
    # TR: backlog'u var görünüp görünmediğini söyler.
    buffer_backlog_present: bool

    # EN: drain_buffer_to_data_first tells whether buffered backlog must be fully
    # EN: moved into /srv/data before crawler resumes normal processed writes.
    # TR: drain_buffer_to_data_first buffer backlog'unun crawler normal işlenmiş
    # TR: yazımlara dönmeden önce tamamen /srv/data tarafına taşınması gerekip
    # TR: gerekmediğini söyler.
    drain_buffer_to_data_first: bool

    # EN: pause_crawler tells whether crawler must pause instead of continuing
    # EN: normal processed-output emission.
    # TR: pause_crawler crawler'ın normal işlenmiş çıktı üretimine devam etmek
    # TR: yerine pause olması gerekip gerekmediğini söyler.
    pause_crawler: bool

    # EN: primary_status is the observed live state of /srv/data.
    # TR: primary_status /srv/data yolunun gözlenen canlı durumudur.
    primary_status: StoragePathStatus

    # EN: fallback_status is the observed live state of /srv/buffer.
    # TR: fallback_status /srv/buffer yolunun gözlenen canlı durumudur.
    fallback_status: StoragePathStatus

    # EN: explanation stores a short human-readable explanation of the decision.
    # TR: explanation kararın kısa insan-okunur açıklamasını tutar.
    explanation: str


# EN: This helper probes one filesystem path conservatively without creating
# EN: files or mutating any live state.
# TR: Bu yardımcı tek bir filesystem path'ini dosya oluşturmadan ve canlı durumu
# TR: değiştirmeden muhafazakâr biçimde probe eder.
def probe_storage_path(path: Path) -> StoragePathStatus:
    # EN: We first ask whether the path exists because all later checks depend on it.
    # TR: Tüm sonraki kontroller buna bağlı olduğu için önce path'in var olup
    # TR: olmadığına bakıyoruz.
    exists = path.exists()

    # EN: We only ask whether it is a directory if it exists.
    # TR: Bunun dizin olup olmadığını yalnızca mevcutsa soruyoruz.
    is_dir = path.is_dir() if exists else False

    # EN: We only ask whether it is a mountpoint if it exists.
    # TR: Bunun mountpoint olup olmadığını yalnızca mevcutsa soruyoruz.
    is_mount = path.is_mount() if exists else False

    # EN: We consider the path writable only when it exists, is a directory,
    # EN: is mounted, and current process permissions allow writing.
    # TR: Bir path'i ancak mevcutsa, dizinse, mounted ise ve mevcut süreç izinleri
    # TR: yazmaya izin veriyorsa yazılabilir kabul ediyoruz.
    is_writable = bool(
        exists
        and is_dir
        and is_mount
        and os.access(path, os.W_OK)
    )

    # EN: We derive one short reason for non-usable states.
    # TR: Kullanılamayan durumlar için tek bir kısa neden türetiyoruz.
    if not exists:
        reason = "path_missing"
    elif not is_dir:
        reason = "not_a_directory"
    elif not is_mount:
        reason = "not_mounted"
    elif not is_writable:
        reason = "not_writable"
    else:
        reason = None

    # EN: We return one explicit structured status object.
    # TR: Tek bir açık yapılı durum nesnesi döndürüyoruz.
    return StoragePathStatus(
        path=str(path),
        exists=exists,
        is_dir=is_dir,
        is_mount=is_mount,
        is_writable=is_writable,
        reason=reason,
    )


# EN: This helper decides whether a probed path is usable for normal processed
# EN: output writes.
# TR: Bu yardımcı probe edilmiş bir path'in normal işlenmiş çıktı yazımları için
# TR: kullanılabilir olup olmadığını belirler.
def path_is_usable(status: StoragePathStatus) -> bool:
    # EN: All required observable conditions must be true together.
    # TR: Gerekli tüm gözlenebilir koşullar birlikte doğru olmalıdır.
    return (
        status.exists
        and status.is_dir
        and status.is_mount
        and status.is_writable
    )


# EN: This helper checks whether /srv/buffer currently appears to contain
# EN: processed-output backlog that is waiting to be moved into /srv/data.
# TR: Bu yardımcı /srv/buffer içinde şu anda /srv/data tarafına taşınmayı bekleyen
# TR: işlenmiş çıktı backlog'u var görünüp görünmediğini kontrol eder.
def detect_buffer_backlog(buffer_path: Path = PROCESSED_FALLBACK_ROOT) -> bool:
    # EN: If the fallback root does not exist or is not a directory, no usable
    # EN: backlog scan can happen, so we conservatively report no backlog here.
    # TR: Fallback kök mevcut değilse veya dizin değilse kullanılabilir backlog
    # TR: taraması yapılamaz; burada muhafazakâr olarak backlog yok diyoruz.
    if not buffer_path.exists() or not buffer_path.is_dir():
        return False

    # EN: We iterate through directory children and ignore lost+found because
    # EN: ext4 may create it even when no crawler-produced backlog exists.
    # TR: Dizin çocuklarını geziyoruz ve lost+found öğesini yok sayıyoruz; çünkü
    # TR: ext4 crawler kaynaklı backlog olmasa bile bunu oluşturabilir.
    for child in buffer_path.iterdir():
        if child.name == "lost+found":
            continue
        return True

    # EN: If we found nothing except optional filesystem boilerplate, backlog
    # EN: is currently absent.
    # TR: Opsiyonel filesystem boilerplate dışında hiçbir şey bulmadıysak backlog
    # TR: şu anda yoktur.
    return False


# EN: This function implements the user's simple canonical rule:
# EN: raw data stays under /srv, processed output goes to /srv/data when usable,
# EN: otherwise to /srv/buffer, and if /srv/data becomes usable while buffer
# EN: backlog exists, crawler must pause until buffer is fully drained into /srv/data.
# TR: Bu fonksiyon kullanıcının sade kanonik kuralını uygular:
# TR: ham veri /srv altında kalır, işlenmiş çıktı kullanılabiliyorsa /srv/data
# TR: yoluna gider, aksi halde /srv/buffer yoluna gider ve /srv/data tekrar
# TR: kullanılabilir hale geldiğinde buffer backlog'u varsa crawler buffer tamamen
# TR: /srv/data tarafına boşaltılana kadar pause olur.
def choose_processed_output_plan(
    primary_path: Path = PROCESSED_PRIMARY_ROOT,
    fallback_path: Path = PROCESSED_FALLBACK_ROOT,
    raw_root: Path = RAW_COLLECTION_ROOT,
) -> ProcessedOutputPlan:
    # EN: We probe the primary processed-output root first because it is the
    # EN: intended normal destination.
    # TR: Birincil işlenmiş çıktı kökü normal hedef olduğu için önce onu probe ediyoruz.
    primary_status = probe_storage_path(primary_path)

    # EN: We probe the fallback processed-output root second because it is used
    # EN: only when the primary route is unavailable.
    # TR: Fallback işlenmiş çıktı kökü yalnızca birincil rota kullanılamadığında
    # TR: kullanıldığı için ikinci olarak onu probe ediyoruz.
    fallback_status = probe_storage_path(fallback_path)

    # EN: We detect whether buffered backlog currently exists in /srv/buffer.
    # TR: /srv/buffer içinde şu anda buffer backlog'u var mı bunu tespit ediyoruz.
    buffer_backlog_present = detect_buffer_backlog(fallback_path)

    # EN: If the primary processed-output path is usable and buffer backlog
    # EN: exists, crawler must pause first so backlog can be fully moved into /srv/data.
    # TR: Birincil işlenmiş çıktı path'i kullanılabiliyor ve buffer backlog'u varsa
    # TR: crawler önce pause olmalıdır; böylece backlog tamamen /srv/data tarafına taşınır.
    if path_is_usable(primary_status) and buffer_backlog_present:
        return ProcessedOutputPlan(
            raw_collection_root=str(raw_root),
            processed_output_root=None,
            using_fallback=False,
            buffer_backlog_present=True,
            drain_buffer_to_data_first=True,
            pause_crawler=True,
            primary_status=primary_status,
            fallback_status=fallback_status,
            explanation="primary processed output root is usable again; pause crawler until /srv/buffer is fully drained into /srv/data",
        )

    # EN: If the primary processed-output path is usable and no backlog blocks it,
    # EN: we use /srv/data.
    # TR: Birincil işlenmiş çıktı path'i kullanılabiliyor ve onu engelleyen backlog
    # TR: yoksa /srv/data yolunu kullanırız.
    if path_is_usable(primary_status):
        return ProcessedOutputPlan(
            raw_collection_root=str(raw_root),
            processed_output_root=str(primary_path),
            using_fallback=False,
            buffer_backlog_present=buffer_backlog_present,
            drain_buffer_to_data_first=False,
            pause_crawler=False,
            primary_status=primary_status,
            fallback_status=fallback_status,
            explanation="primary processed output root is usable; write processed output to /srv/data",
        )

    # EN: If the primary path is not usable but fallback is usable, we preserve
    # EN: continuity by writing processed output to /srv/buffer.
    # TR: Birincil path kullanılamıyor ama fallback kullanılabiliyorsa sürekliliği
    # TR: işlenmiş çıktıyı /srv/buffer yoluna yazarak koruruz.
    if path_is_usable(fallback_status):
        return ProcessedOutputPlan(
            raw_collection_root=str(raw_root),
            processed_output_root=str(fallback_path),
            using_fallback=True,
            buffer_backlog_present=buffer_backlog_present,
            drain_buffer_to_data_first=False,
            pause_crawler=False,
            primary_status=primary_status,
            fallback_status=fallback_status,
            explanation="primary processed output root is unusable; write processed output to /srv/buffer",
        )

    # EN: If neither path is usable, crawler must pause and surface a hard error.
    # TR: İki path de kullanılamıyorsa crawler pause olmalı ve sert hata vermelidir.
    return ProcessedOutputPlan(
        raw_collection_root=str(raw_root),
        processed_output_root=None,
        using_fallback=False,
        buffer_backlog_present=buffer_backlog_present,
        drain_buffer_to_data_first=False,
        pause_crawler=True,
        primary_status=primary_status,
        fallback_status=fallback_status,
        explanation="neither /srv/data nor /srv/buffer is currently usable; crawler must pause and surface an explicit error",
    )
