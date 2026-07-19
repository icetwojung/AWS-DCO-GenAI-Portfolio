#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[교육용 DCO 로그 분석 스크립트]
이 스크립트는 IT/네트워크 운영(DCO) 업무 이해를 돕기 위해 작성된 교육용 샘플 스크립트입니다.
파이썬 표준 라이브러리만을 사용하여 입력 로그 파일(sample_dco_log.txt)을 파싱하고,
그 결과를 읽기 쉬운 Markdown 형식의 보고서(incident_summary.md)로 자동 생성합니다.

초보자(비전공자)를 위해 각 코드 블록마다 친절한 주석을 달아두었습니다.
"""

import os
from collections import Counter

def analyze_logs():
    # 1. 파일 경로 설정
    # 입력 파일: 분석할 대상 로그 파일
    input_file = "sample_dco_log.txt"
    # 출력 경로: 분석 결과가 저장될 파일명 (07_log_analysis_script 폴더 없이 바로 현재 폴더에 생성)
    output_file = "incident_summary.md"

    # [예외 처리] 입력 로그 파일이 존재하는지 확인합니다.
    if not os.path.exists(input_file):
        print(f"오류: 입력 파일 '{input_file}'을 찾을 수 없습니다.")
        print("스크립트와 같은 폴더에 'sample_dco_log.txt' 파일이 있는지 확인해 주세요.")
        return

    # 2. 분석을 위한 데이터 저장용 변수(바구니) 준비하기
    total_lines = 0                    # 전체 로그 줄 수
    severities = []                     # 심각도(Severity)들을 담을 리스트
    events = []                         # 이벤트(Event) 종류들을 담을 리스트
    warning_or_critical_logs = []       # WARNING 또는 CRITICAL 심각도를 가진 로그를 수집할 리스트
    key_incident_logs = []              # CRC_ERROR, LINK_DOWN, TICKET_ESCALATED 관련 주요 로그 리스트

    # 3. 로그 파일 읽고 파싱(분석)하기
    # 'with open'을 사용하면 파일을 안전하게 열고 작업이 끝난 뒤 자동으로 닫아줍니다.
    # utf-8 인코딩을 사용하여 한글이나 특수기호가 깨지지 않도록 합니다.
    with open(input_file, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip() # 줄 바꿈 문자(\n) 및 양끝 공백을 제거합니다.
            
            if not line: # 만약 빈 줄(공백 라인)이 있다면 건너뜁니다.
                continue
            
            # 로그의 형식: YYYY-MM-DD HH:MM:SS | DEVICE | SEVERITY | EVENT | MESSAGE
            # 파이프 기호('|')를 기준으로 로그의 각 영역을 분할합니다.
            parts = [part.strip() for part in line.split('|')]
            
            # 정상적인 로그 형식(5개의 영역)을 가지고 있는지 확인합니다.
            if len(parts) != 5:
                # 형식이 맞지 않는 로그가 있다면 경고를 출력하고 다음 줄로 넘어갑니다.
                print(f"[경고] {line_num}번째 줄은 올바른 로그 형식이 아닙니다: {line}")
                continue
                
            total_lines += 1 # 정상적인 로그 줄 수 누적
            
            # 분할된 데이터를 각각 의미 있는 이름의 변수에 대입합니다.
            timestamp, device, severity, event, message = parts
            
            # 전체 통계를 위해 심각도와 이벤트를 리스트에 수집합니다.
            severities.append(severity)
            events.append(event)
            
            # 수집된 데이터를 딕셔너리(Dictionary) 형태로 묶어둡니다. (나중에 출력할 때 쓰기 위함)
            log_data = {
                "timestamp": timestamp,
                "device": device,
                "severity": severity,
                "event": event,
                "message": message,
                "raw": line
            }
            
            # 분석 4. WARNING, ERROR 또는 CRITICAL 로그 수집하기
            # 대소문자 구분을 줄이기 위해 .upper()를 사용하여 비교합니다.
            if severity.upper() in ["WARNING", "ERROR", "CRITICAL"]:
                warning_or_critical_logs.append(log_data)
                
            # 분석 5. CRC_ERROR, LINK_DOWN, TICKET_ESCALATED가 포함된 주요 이벤트 요약 대상 찾기
            # 이벤트 타입 또는 메시지 내용 중에 타겟 키워드(공백 또는 언더바 형식 포함)가 포함되어 있는지 체크합니다.
            full_text_upper = f"{event} {message}".upper()
            is_target = False
            for kw in ["CRC_ERROR", "LINK_DOWN", "TICKET_ESCALATED", "CRC ERROR", "LINK DOWN", "TICKET ESCALATED", "CRC", "LINK", "TICKET"]:
                if kw in full_text_upper:
                    is_target = True
                    break
            if is_target:
                key_incident_logs.append(log_data)

    # 4. 수집한 데이터 가공 및 통계 산출
    # Counter 객체를 사용하면 리스트 안에 있는 요소들의 개수를 아주 쉽게 셀 수 있습니다.
    severity_counts = Counter(severities)
    event_counts = Counter(events)

    # 5. Markdown 보고서 작성하기 (결과 파일 쓰기)

    # 결과를 마크다운(Markdown) 문법에 맞게 문자열로 작성합니다.
    md_content = []
    md_content.append("# 📊 AWS DCO 교육용 샘플 로그 분석 보고서")
    md_content.append(f"\n- **작성 일시:** 2026-07-18 21:01:00 (KST)")
    md_content.append("- **분석 대상 파일:** `sample_dco_log.txt`\n")
    
    md_content.append("## 1. 전체 로그 요약 통계")
    md_content.append(f"- **총 수집 로그 라인:** `{total_lines}` 줄\n")
    
    md_content.append("### ■ 심각도(Severity)별 분포")
    # 높은 심각도 순서대로 정렬하여 예쁘게 표로 나타냅니다.
    md_content.append("| 심각도 (Severity) | 로그 개수 (건) | 비율 (%) |")
    md_content.append("| :--- | :--- | :--- |")
    for sev in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        count = severity_counts.get(sev, 0)
        percentage = (count / total_lines) * 100 if total_lines > 0 else 0
        md_content.append(f"| **{sev}** | {count}건 | {percentage:.1f}% |")
    md_content.append("")
    
    md_content.append("### ■ 이벤트(Event) 타입별 발생 현황")
    md_content.append("| 이벤트 타입 (Event Type) | 발생 횟수 (건) |")
    md_content.append("| :--- | :--- |")
    # 가장 많이 발생한 이벤트 순서대로 정렬하여 리스팅합니다.
    for ev_type, count in event_counts.most_common():
        md_content.append(f"| `{ev_type}` | {count}건 |")
    md_content.append("")
    
    md_content.append("## 2. 주의 및 위험 로그 상세 목록 (WARNING, ERROR & CRITICAL)")
    md_content.append("DCO 장비 점검 시 우선적으로 조치가 필요한 상태 주의/경고 로그 목록입니다.\n")
    md_content.append("| 발생 시간 | 대상 장비 | 심각도 | 이벤트 유형 | 메시지 내용 |")
    md_content.append("| :--- | :--- | :--- | :--- | :--- |")
    for log in warning_or_critical_logs:
        # CRITICAL 및 ERROR는 강조를 위해 빨간 배지나 굵은 글씨로 마크업해 줍니다.
        sev_label = f"🔴 **{log['severity']}**" if log['severity'].upper() in ["CRITICAL", "ERROR"] else f"🟡 {log['severity']}"
        md_content.append(f"| `{log['timestamp']}` | `{log['device']}` | {sev_label} | `{log['event']}` | {log['message']} |")
    md_content.append("")
    
    md_content.append("## 3. 핵심 장애 인시던트 분석 요약")
    md_content.append("네트워크 링크 장애(`LINK_DOWN`), 에러율 급증(`CRC_ERROR`), 티켓 이관 및 에스컬레이션(`TICKET_ESCALATED`)과 관련된 고순도 인시던트만 추출한 요약입니다.\n")
    
    if not key_incident_logs:
        md_content.append("> 현재 감지된 핵심 장애 인시던트가 존재하지 않습니다. 시스템이 안정적입니다.\n")
    else:
        for idx, log in enumerate(key_incident_logs, 1):
            # 어떤 키워드가 포함되었는지 판별하여 머리글 장식
            category = []
            combined_upper = f"{log['event']} {log['message']}".upper()
            if "CRC" in combined_upper:
                category.append("🔄 CRC 에러 감지")
            if "LINK" in combined_upper:
                category.append("🔌 링크 다운 발생")
            if "TICKET" in combined_upper or "ESCALATED" in combined_upper:
                category.append("🚨 티켓 에스컬레이션 완료")
                
            category_str = ", ".join(category) if category else "⚠️ 일반 이벤트"
            md_content.append(f"### 인시던트 #{idx}: [{category_str}]")
            md_content.append(f"- **시간 / 장비:** `{log['timestamp']}` | `{log['device']}`")
            md_content.append(f"- **상태:** **{log['severity']}** (이벤트: `{log['event']}`)")
            md_content.append(f"- **원문 내용:** `{log['message']}`\n")

    # 마크다운 리스트를 하나의 큰 문자열로 합쳐서 파일에 씁니다.
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(md_content))

    print("==================================================")
    print("🎉 로그 분석이 성공적으로 완료되었습니다!")
    print(f"📂 결과 파일 저장 경로: {output_file}")
    print("==================================================")
    print(f"- 전체 처리 로그: {total_lines}개 라인")
    print(f"- WARNING/CRITICAL 위험 로그: {len(warning_or_critical_logs)}건 수집됨")
    print(f"- 핵심 장애 인시던트(CRC, LINK, TICKET): {len(key_incident_logs)}건 요약됨")
    print("==================================================")

if __name__ == "__main__":
    analyze_logs()
