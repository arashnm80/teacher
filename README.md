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

Source for the practice app: [arashnm80/teacher-playground](https://github.com/arashnm80/teacher-playground). Keep a copy under `/root/Storage/teacher-playground` on the class server in sync with that GitHub repo. Rebuild the zip from that tree, put it in `11th-grade/extras/teacher-playground-offline.zip`, then `python3 build_site.py` and `bash deploy.sh`.

### Rebuild / publish

```bash
cd 11th-grade
python3 build_site.py
bash deploy.sh
```
