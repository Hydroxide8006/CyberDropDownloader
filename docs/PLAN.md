# 🎼 CyberDropDownloader - Lazarus Protocol Implementation Plan

Bu plan, `cyberdrop-dl-patched` projesini tam stabiliteye ulaştırmak için 4 ana faza bölünmüştür.

## 🛠️ Faz 1: Stealth & Fallback Engine (Güvenlik Altyapısı)
**Sorumlu Agent:** `security-auditor`
- **Hedef:** Cloudflare ve DDoS-Guard korumalarını aşmak için FlareSolverr'a bağımlılığı azaltmak.
- **Görevler:**
  - `playwright` ve `playwright-stealth` entegrasyonu.
  - `ScraperClient` içerisine `impersonate_with_browser` metodu ekleyerek, `curl-cffi` başarısız olduğunda otomatik tarayıcı tabanlı scraping başlatmak.
  - Tarayıcı üzerinden alınan çerezlerin (cookies) asenkron `aiohttp` session'ına aktarılması.

## 🧩 Faz 2: Bunkr & Media Crawling Modernization
**Sorumlu Agent:** `backend-specialist`
- **Hedef:** Bunkr'ın kırılgan XOR şifrelemesini dinamik hale getirmek.
- **Görevler:**
  - `bunkrr.py` revizyonu: Statik XOR key (`SECRET_KEY_...`) yerine, sayfadaki JS kodundan anahtarı Regex/Playwright ile dinamik yakalayan bir logic geliştirilmesi.
  - CDN hostlarının (milkshake, gigachad vb.) dinamik olarak listelenmesi ve güncellenmesi.
  - Bozuk `albumFiles` parser'ının modernize edilmesi.

## 🌐 Faz 3: Dynamic Domain & Infrastructure
**Sorumlu Agent:** `backend-specialist` & `devops-engineer`
- **Hedef:** Domain değişikliklerini kod değiştirmeden (hardcoded olmadan) yönetmek.
- **Görevler:**
  - `DynamicDomainManager` modülünün oluşturulması.
  - Coomer, Kemono ve Bunkr domainlerinin bir Remote JSON (örn: GitHub Gist veya Repo raw) üzerinden anlık çekilmesi.
  - `SupportedDomains` sınıfının bu dinamik yapıya entegre edilmesi.

## 🧪 Faz 4: Verification & Smoke Tests
**Sorumlu Agent:** `test-engineer`
- **Hedef:** Yapılan değişikliklerin doğrulanması.
- **Görevler:**
  - En popüler 5 site (Bunkr, Coomer, Kemono, Erome, GoFile) için otomatik smoke test script'i (`tests/smoke_test.py`) yazılması.
  - Çerez çıkarma (cookie extraction) testlerinin her tarayıcı (Chrome, Firefox, Brave) için doğrulanması.

---

## 🎼 Orchestration Report (Phase 1)
- **Invoked Agents:** `project-planner`, `explorer-agent`
- **Deliverable:** `docs/PLAN.md`
- **Status:** Planning Complete.

**Onay veriyor musunuz? (Y/N)**
- Y: Uygulamaya geç (Phase 2 start)
- N: Planı revize et
