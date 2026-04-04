# SQL Surface

This directory is intended for tracked SQL assets that belong in the canonical LogisticSearch repository. Its purpose is to hold durable database-side materials such as DDL, import logic, audit queries, validation queries, and other structured SQL content that should remain versioned, reviewable, and reusable.

Bu dizin, kanonik LogisticSearch repository’sinde izlenmesi gereken SQL varlıkları için ayrılmıştır. Amacı; DDL, import mantığı, audit sorguları, doğrulama sorguları ve versiyonlu, gözden geçirilebilir ve yeniden kullanılabilir kalması gereken diğer yapısal SQL içeriklerini barındırmaktır.

## Policy

Only repository-worthy SQL should live here. Throwaway experiments, host-local scraps, temporary exports, and machine-specific runtime outputs should not accumulate inside this directory. The goal is to gradually shape this area into a clear and disciplined SQL surface.

Burada yalnızca repository’ye girmeye değer SQL içerikleri yer almalıdır. Tek kullanımlık deneyler, host’a özel geçici parçalar, temporary export’lar ve makineye özgü runtime çıktıları bu dizinde birikmemelidir. Amaç bu alanı zamanla net ve disiplinli bir SQL yüzeyine dönüştürmektir.

## Expected Direction

The likely long-term role of this directory includes schema definitions, import queries, audit checks, controlled transformations, and other database-side building blocks that support the LogisticSearch data pipeline.

Bu dizinin muhtemel uzun vadeli rolü; LogisticSearch veri hattını destekleyen şema tanımları, import sorguları, audit kontrolleri, kontrollü dönüşümler ve diğer veritabanı tarafı yapı taşlarını içermektir.
