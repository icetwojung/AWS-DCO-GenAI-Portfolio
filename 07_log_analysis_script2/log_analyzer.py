"""
log_analyzer.py
- 대소문자 무시 (case-insensitive)
- 여러 줄에 걸친 로그 이벤트를 하나로 묶어서 카운트
  (새 이벤트 = 타임스탬프로 시작하는 줄, 연속 줄 = 공백/->로 시작)
- 제외 패턴(EXCLUDE): 키워드 매칭에서 false positive 제거
"""

import glob
import os
import re

LOG_DIR  = os.path.dirname(os.path.abspath(__file__))
KEYWORDS = ["CRC error", "Link Down"]

# 키워드별 제외 패턴 (해당 문자열을 포함하는 이벤트는 카운트하지 않음)
# 예: "CRC error recovered", "CRCcheck OK" 등 정상/복구 메시지 제외
EXCLUDE = {
    "CRC error": ["crccheck ok", "crc error recovered", "no crc error found"],
    "Link Down": [],
}

# 타임스탬프 패턴 (4가지 형식 모두 지원):
#   형식 A: "YYYY-MM-DD HH:MM:SS ..."       server01  예: 2026-07-06 00:26:20
#   형식 B: "Mon DD HH:MM:SS ..."           server02  예: Jul 06 01:59:04
#   형식 C: "[DD/Mon/YYYY:HH:MM:SS] ..."    server03  예: [06/Jul/2026:01:36:20]
#   형식 D: "HH:MM:SS.mmm ..."              server04  예: 03:27:06.628
TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"            # 형식 A
    r"|^[A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2}"          # 형식 B
    r"|^\[\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\]"  # 형식 C
    r"|^\d{2}:\d{2}:\d{2}\.\d+"                          # 형식 D
)


def parse_events(filepath):
    """로그 파일을 이벤트(멀티라인 포함) 단위로 파싱해 반환."""
    events = []
    current = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if TIMESTAMP_RE.match(line):
                if current:
                    events.append("\n".join(current))
                current = [line.rstrip()]
            else:
                # 들여쓰기/화살표 등 연속 줄 → 현재 이벤트에 병합
                if current:
                    current.append(line.rstrip())
        if current:
            events.append("\n".join(current))
    return events


def count_keyword(events, keyword):
    """이벤트 목록에서 키워드를 포함하는 이벤트 수를 반환 (대소문자 무시).
    EXCLUDE 패턴에 해당하는 이벤트는 카운트에서 제외한다.
    """
    kw_lower  = keyword.lower()
    excludes  = [ex.lower() for ex in EXCLUDE.get(keyword, [])]

    def is_match(ev):
        ev_lower = ev.lower()
        if kw_lower not in ev_lower:
            return False
        # 제외 패턴이 하나라도 포함되면 카운트 제외
        if any(ex in ev_lower for ex in excludes):
            return False
        return True

    return sum(1 for ev in events if is_match(ev))


# ── 분석 시작 ──────────────────────────────────────────────
log_files = sorted(glob.glob(os.path.join(LOG_DIR, "server*.log")))

header = f"{'서버':<15}" + "".join(f"{kw:>15}" for kw in KEYWORDS)
sep    = "-" * (15 + 15 * len(KEYWORDS))
print(header)
print(sep)

totals = {kw: 0 for kw in KEYWORDS}

for log_file in log_files:
    server_name = os.path.basename(log_file)
    events      = parse_events(log_file)
    counts      = {kw: count_keyword(events, kw) for kw in KEYWORDS}

    for kw in KEYWORDS:
        totals[kw] += counts[kw]

    row = f"{server_name:<15}" + "".join(f"{counts[kw]:>15}" for kw in KEYWORDS)
    print(row)

print(sep)
total_row = f"{'합계':<15}" + "".join(f"{totals[kw]:>15}" for kw in KEYWORDS)
print(total_row)
