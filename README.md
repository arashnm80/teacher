# teacher

Teaching material for my classes.

## Grade 11 — طراح سایت

Offline bilingual site for the lab: [11th-grade/site/index.html](11th-grade/site/index.html).

Copy the whole `11th-grade/site` folder onto a classroom PC and double-click `index.html`. No internet is required.

Public copy: [teacher.arashnm80.ir](https://teacher.arashnm80.ir).

Requirements for later changes: [11th-grade/REQUIREMENTS.md](11th-grade/REQUIREMENTS.md).

### Offline downloads on the site

| File | What it is |
|------|------------|
| `grade11-offline.zip` | Whole textbook site (header + home page) |
| `teacher-playground-offline.zip` | Offline Python practice app for module 1 — [پیوندهای مفید](https://teacher.arashnm80.ir/book/links.html) |
| `evolution-of-trust-offline.zip` | Trust-game lab for period 4 — same links page |

### Python playground (online + offline)

Source lives in this repo at [11th-grade/playground/](11th-grade/playground/).

- Online for home / phone: [teacher.arashnm80.ir/playground](https://teacher.arashnm80.ir/playground/)
- Lab PCs without internet: unzip `teacher-playground-offline.zip` and run `شروع.bat`

After changing the playground, rebuild the offline zip into `11th-grade/extras/teacher-playground-offline.zip`, then:

```bash
cd 11th-grade
python3 build_site.py
bash deploy.sh
```

`build_site.py` copies `playground/app/` into `site/playground/` for the public URL.

### Rebuild / publish

```bash
cd 11th-grade
python3 build_site.py
bash deploy.sh
```
