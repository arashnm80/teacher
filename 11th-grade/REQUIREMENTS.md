# Requirements — grade 11 site (طراح سایت)

Remember these on every later change. The classroom copy is the test.

## What this is

A static companion to the grade-11 textbook «طراح سایت» (رشته شبکه و نرم‌افزار رایانه). Students open it on lab PCs that have no internet.

## Must stay true

1. **Offline, including `file://`.** Copying the `site/` folder to a Windows PC and double-clicking `index.html` is the whole install. No web server, no `npm`, no internet.
2. **The `site/` folder is complete.** HTML, CSS, JavaScript, and images all live inside it. Do not link to `../converted-markdown-book/` or to anything outside `site/`. Symlinks break when the folder is copied to Windows.
3. **No remote dependencies.** No CDN, no Google Fonts, no analytics, no `fetch()` of a file (Chrome blocks `fetch` on `file://`). Ship data in a normal `<script>` file instead. Fonts are the ones already on school PCs (`Tahoma`, `Segoe UI`, `Consolas`).
4. **Relative links only** for anything the page needs in order to render.
5. **Bilingual interface, Persian lesson text.** Chrome (menus, buttons, home page, search) is Persian and English, switched in the page and remembered in `localStorage`. The lesson body stays the official Persian textbook, and it stays right-to-left even when the chrome is English. Do not machine-translate the book unless a later version explicitly asks for that.
6. **Works with JavaScript off for reading.** Persian navigation and lesson pages must still open. JavaScript is only for the language switch and search.
7. **Rebuild after markdown edits.** Source lessons are `converted-markdown-book/`. Run `python3 build_site.py` (needs the `markdown` package) and commit the new `site/`.
8. **Public copy.** `https://teacher.arashnm80.ir` is this same `site/` folder, served by nginx on this machine. Cloudflare proxies the name (the A record is already orange-clouded). TLS on the origin is the existing wildcard certificate `/etc/nginx/ssl/arashnm80.ir/`. Nginx cannot read `/root`, so the published files live at `/var/www/teacher.arashnm80.ir`. After a rebuild, run `bash deploy.sh` from `11th-grade/`. Do not point the site at a CDN.

## Check before calling it done

- Open `site/index.html` from disk, not from a server, and click through a lesson, a figure, and the language switch.
- Generated HTML must not load a stylesheet or script from `http://` or `https://`.
- A figure that is missing on disk is a failed build.

## Known limits of version 1

- Some two-column tables in the PDF were read in a mixed order. The figure image is the reliable copy of those pages.
- Code samples that the book printed as screenshots are images, not retyped source.
- URLs in the references chapter are real links. They need internet only if someone clicks them. The page itself must still render offline.

## الزامات — نسخه فارسی

این‌ها را در تغییرهای بعدی نگه دارید. آزمون واقعی، کپی کردن پوشه در رایانه کلاس است.

1. **بدون اینترنت، حتی با باز کردن مستقیم فایل.** کل پوشه `site/` را کپی کنید و `index.html` را با دوبار کلیک باز کنید. سرور و اینترنت لازم نیست.
2. **پوشه `site/` خودش کامل است.** صفحه، سبک، اسکریپت و تصویرها داخل همان پوشه باشند. پیوند به بیرون پوشه یا میانبر (symlink) بعد از کپی در ویندوز می‌شکند.
3. **هیچ وابستگی دوری نباشد.** نه CDN، نه فونت گوگل، نه `fetch`. فونت همان قلم‌های موجود ویندوز مدرسه است (`Tahoma` و `Segoe UI`).
4. **ظاهر سایت دوزبانه است، متن درس فارسی کتاب است.** با دکمه زبان، منو و صفحه اول فارسی یا انگلیسی می‌شود. متن درس همان کتاب رسمی است و حتی در حالت انگلیسی هم راست‌به‌چپ می‌ماند. ترجمه ماشینی کتاب جزو این نسخه نیست.
5. **بدون جاوااسکریپت هم بتوان درس را خواند.** زبان و جستجو با جاوااسکریپت کار می‌کنند.
6. **بعد از ویرایش مارک‌داون** دستور `python3 build_site.py` را اجرا کنید و پوشه `site/` را دوباره وارد مخزن کنید.
7. **نسخه عمومی** روی `https://teacher.arashnm80.ir` است. بعد از ساختن دوباره سایت، از پوشه `11th-grade` دستور `bash deploy.sh` را اجرا کنید. nginx فایل‌ها را از `/var/www/teacher.arashnm80.ir` می‌خواند، چون به پوشه `/root` دسترسی ندارد.
