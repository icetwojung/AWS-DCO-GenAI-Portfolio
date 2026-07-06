# -*- coding: utf-8 -*-
"""
AWS DCO 인턴십 직무 이해를 위한 교육용 DCO 로그 분석 스크립트
작성 목적: 비전공자 학생들도 쉽게 이해할 수 있는 Python 표준 라이브러리 기반 로그 분석 도구
"""

import os
import sys
from collections import Counter


def find_log_file():
    """
    분석할 로그 파일(sample_dco_log.txt)의 위치를 찾는 함수입니다.
    스크립트가 실행되는 위치(현재 작업 디렉토리)에 따라 유연하게 파일을 찾을 수 있도록 돕습니다.
    """
    # 1. 현재 작업 디렉토리(CWD)에서 찾기
    cwd_path = "sample_dco_log.txt"
    if os.path.exists(cwd_path):
        return cwd_path

    # 2. 스크립트 파일이 위치한 디렉토리의 상위 디렉토리에서 찾기
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.join(script_dir, "..", "sample_dco_log.txt")
    if os.path.exists(parent_path):
        return os.path.abspath(parent_path)

    # 3. 절대경로 루트에서 찾기 (가상환경 배포 시를 대비)
    absolute_root_path = "/sample_dco_log.txt"
    if os.path.exists(absolute_root_path):
        return absolute_root_path

    return None


def analyze_logs():
    print("=" * 60)
    print("DCO 로그 분석 스크립트를 시작합니다 (교육용 샘플)")
    print("=" * 60)

    # 1. 분석 대상 로그 파일 찾기
    log_file_path = find_log_file()
    if not log_file_path:
        print("[에러] sample_dco_log.txt 파일을 찾을 수 없습니다.")
        print("스크립트와 같은 경로에 있거나 프로젝트 루트 폴더에 있어야 합니다.")
        sys.exit(1)

    print(f"로그 파일을 찾았습니다: {log_file_path}")

    # 분석에 필요한 변수들을 준비합니다.
    total_lines = 0  # 전체 로그 줄 수
    severity_counter = Counter()  # 심각도별 개수를 세어줄 주머니
    event_counter = Counter()  # 이벤트 유형별 개수를 세어줄 주머니

    # 조건에 맞는 로그들을 분류해서 담아둘 상자(리스트)입니다.
    warning_or_critical_logs = []  # WARNING 또는 CRITICAL 등급의 로그들
    major_events_summary = []  # CRC_ERROR, LINK_DOWN, TICKET_ESCALATED 관련 주요 이벤트

    # 2. 파일 안전하게 열고 한 줄씩 읽기
    # encoding="utf-8"을 사용하여 한글 주석이나 한글이 포함된 로그 메시지가 깨지지 않게 합니다.
    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # 줄 끝의 줄바꿈 문자(\\n) 등을 말끔하게 지웁니다.
            if not line:  # 빈 줄이 있다면 무시하고 다음 줄로 넘어갑니다.
                continue

            total_lines += 1  # 로그 한 줄을 읽을 때마다 카운트를 1씩 올립니다.

            # 로그 형식: YYYY-MM-DD HH:MM:SS | DEVICE | SEVERITY | EVENT | MESSAGE
            # 파이프 문자('|')를 기준으로 로그 한 줄을 5개의 부분으로 조각냅니다.
            parts = [part.strip() for part in line.split("|")]

            # 올바른 로그 형식(5개 부분)을 갖추었는지 확인합니다.
            if len(parts) >= 5:
                timestamp = parts[0]  # 날짜 및 시간
                device = parts[1]  # 장비 이름 (예: SAMPLE_TOR_SW_01)
                severity = parts[2].upper()  # 심각도 (대소문자 구분 없애기 위해 대문자로 통일)
                event = parts[3]  # 이벤트명 (예: Normal heartbeat)
                message = parts[4]  # 상세 메시지

                # 2-1. 심각도별 카운트 누적
                severity_counter[severity] += 1

                # 2-2. 이벤트별 카운트 누적
                event_counter[event] += 1

                # 2-3. WARNING 또는 CRITICAL 로그 수집
                # 로그 등급이 WARNING이거나 CRITICAL인 경우 목록에 추가합니다.
                if severity in ["WARNING", "CRITICAL"]:
                    warning_or_critical_logs.append(
                        {
                            "timestamp": timestamp,
                            "device": device,
                            "severity": severity,
                            "event": event,
                            "message": message,
                        }
                    )

                # 2-4. CRC_ERROR, LINK_DOWN, TICKET_ESCALATED 포함 주요 이벤트 분류
                # 이벤트 이름이나 메시지에 특정 키워드가 들어있는지 확인합니다.
                # 대소문자 차이로 인해 놓치지 않도록 소문자로 변환하여 비교합니다.
                event_lower = event.lower()
                msg_lower = message.lower()

                # 분석 키워드 정의
                is_crc = (
                    "crc" in event_lower
                    or "crc" in msg_lower
                    or "crc_error" in event_lower
                )
                is_link_down = "link down" in event_lower or "link_down" in event_lower
                is_ticket_esc = (
                    "escalated" in event_lower
                    or "escalated" in msg_lower
                    or "ticket_escalated" in event_lower
                )

                if is_crc or is_link_down or is_ticket_esc:
                    # 어떤 카테고리에 해당하는지 라벨을 달아줍니다.
                    category = "기타 주요 이벤트"
                    if is_crc:
                        category = "CRC_ERROR (인터페이스 수신 오류)"
                    elif is_link_down:
                        category = "LINK_DOWN (물리적 연결 끊김)"
                    elif is_ticket_esc:
                        category = "TICKET_ESCALATED (장애 티켓 상위 이관)"

                    major_events_summary.append(
                        {
                            "timestamp": timestamp,
                            "device": device,
                            "severity": severity,
                            "category": category,
                            "event": event,
                            "message": message,
                        }
                    )

    # 3. 리포트(incident_summary.md) 생성 및 저장하기
    # 스크립트 파일이 위치한 실제 디렉토리를 기준으로 저장 경로를 결정하여, 
    # 어느 경로에서 스크립트를 실행해도 중복 폴더 생성 없이 제자리에 저장되도록 합니다.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(script_dir, "incident_summary.md")

    # 마크다운(Markdown) 문법을 활용하여 이쁘고 읽기 쉬운 보고서를 작성합니다.
    with open(output_file_path, "w", encoding="utf-8") as out:
        out.write("# 📋 AWS DCO 교육용 샘플 로그 분석 결과 리포트\n\n")
        out.write(
            "> 본 리포트는 실제 AWS 내부 운영 환경이 아니며, 인턴십 직무 이해를 돕기 위해 구성된 가상의 교육용 데이터 분석 결과입니다.\n\n"
        )

        out.write("## 1. 📊 전체 로그 요약\n")
        out.write(f"- **분석 일시**: 2026-07-06 (가상 분석 기준일)\n")
        out.write(f"- **대상 로그 파일**: `{os.path.basename(log_file_path)}`\n")
        out.write(f"- **총 로그 줄 수**: **{total_lines}** 개\n\n")

        # 심각도별 통계 테이블 작성
        out.write("## 2. ⚠️ 심각도(Severity)별 통계\n")
        out.write("| 심각도 등급 | 로그 수 | 비율 (%) |\n")
        out.write("| :--- | :---: | :---: |\n")
        for sev, count in severity_counter.most_common():
            ratio = (count / total_lines) * 100 if total_lines > 0 else 0
            out.write(f"| **{sev}** | {count} | {ratio:.1f}% |\n")
        out.write("\n")

        # 이벤트별 통계 테이블 작성 (상위 5개만 혹은 전체)
        out.write("## 3. 🏷️ 이벤트(Event) 종류별 발생 현황\n")
        out.write("| 이벤트 유형 | 발생 횟수 |\n")
        out.write("| :--- | :---: |\n")
        for evt, count in event_counter.most_common():
            out.write(f"| {evt} | {count} |\n")
        out.write("\n")

        # WARNING 또는 CRITICAL 등급의 로그 목록 작성
        out.write("## 4. 🔥 경보 및 위험 로그 목록 (WARNING / CRITICAL)\n")
        if not warning_or_critical_logs:
            out.write("*현재 로그 내에 WARNING 또는 CRITICAL 등급의 로그가 존재하지 않습니다.*\n")
        else:
            out.write("| 발생 시간 | 장비명 | 등급 | 이벤트 | 상세 메시지 |\n")
            out.write("| :--- | :--- | :---: | :--- | :--- |\n")
            for log in warning_or_critical_logs:
                out.write(
                    f"| {log['timestamp']} | `{log['device']}` | **{log['severity']}** | {log['event']} | {log['message']} |\n"
                )
        out.write("\n")

        # CRC_ERROR, LINK_DOWN, TICKET_ESCALATED 요약 작성
        out.write("## 5. 🔍 핵심 장애 및 운영 사건 요약\n")
        out.write(
            "DCO 엔지니어가 주의 깊게 모니터링해야 하는 `CRC 에러 증가`, `포트 다운(Link Down)`, `장애 티켓 에스컬레이션(이관)` 이벤트를 필터링한 결과입니다.\n\n"
        )

        if not major_events_summary:
            out.write("*지정된 주요 운영 사건(CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)이 감지되지 않았습니다.*\n")
        else:
            out.write("| 발생 시간 | 장비명 | 장애 분류 | 이벤트명 | 세부 조치 메시지 |\n")
            out.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for item in major_events_summary:
                out.write(
                    f"| {item['timestamp']} | `{item['device']}` | <span style='color:red; font-weight:bold;'>{item['category']}</span> | {item['event']} | {item['message']} |\n"
                )
        out.write("\n")

        out.write("--- \n")
        out.write("*본 분석 보고서는 Python 내장 기능을 통해 자동 생성되었습니다.*\n")

    print("=" * 60)
    print(f"분석 결과 보고서 작성이 완료되었습니다!")
    print(f"저장 경로: {output_file_path}")
    print("=" * 60)


if __name__ == "__main__":
    analyze_logs()
