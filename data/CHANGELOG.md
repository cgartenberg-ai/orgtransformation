# Data Changelog

Append-only audit log. Every automated script that modifies data files logs here.

Format: `## YYYY-MM-DD HH:MM:SS — script-name` followed by bullet points.

---

## 2026-02-14 13:47:43 — fix-contingencies-talent (inline)
- Merged non-traditional (1 specimens) into nonTraditional -> 7 unique specimens
- Removed redundant talent-rich (1) and talent-constrained (1) keys


## 2026-02-14 13:48:09 — fix-contingencies-talent
- Merged non-traditional (6) into nonTraditional -> 12 unique specimens
- Moved 18 talent-rich-only specimens to high: ['apple', 'blue-origin', 'bmw', 'bosch-bcai', 'crowdstrike', 'disney', 'google-deepmind', 'intel', 'lionsgate', 'mercedes-benz', 'netflix', 'nike', 'recruit-holdings', 'salesforce', 'sap', 'tesla', 'thomson-reuters', 'uber']
- Moved 14 talent-constrained-only specimens to low: ['delta-air-lines', 'dow-chemical', 'exxonmobil', 'ford', 'general-motors', 'honda', 'honeywell', 'hp-inc', 'hyundai-robotics', 'intel', 'lockheed-martin', 'panasonic', 'toyota', 'ulta-beauty']
- Removed redundant talent-rich and talent-constrained keys

