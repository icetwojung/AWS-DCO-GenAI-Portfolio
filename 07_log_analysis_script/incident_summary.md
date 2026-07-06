# 📋 AWS DCO 교육용 샘플 로그 분석 결과 리포트

> 본 리포트는 실제 AWS 내부 운영 환경이 아니며, 인턴십 직무 이해를 돕기 위해 구성된 가상의 교육용 데이터 분석 결과입니다.

## 1. 📊 전체 로그 요약
- **분석 일시**: 2026-07-06 (가상 분석 기준일)
- **대상 로그 파일**: `sample_dco_log.txt`
- **총 로그 줄 수**: **140** 개

## 2. ⚠️ 심각도(Severity)별 통계
| 심각도 등급 | 로그 수 | 비율 (%) |
| :--- | :---: | :---: |
| **INFO** | 135 | 96.4% |
| **WARNING** | 3 | 2.1% |
| **ERROR** | 2 | 1.4% |

## 3. 🏷️ 이벤트(Event) 종류별 발생 현황
| 이벤트 유형 | 발생 횟수 |
| :--- | :---: |
| Normal heartbeat | 125 |
| Ticket opened | 3 |
| Ticket escalated | 3 |
| Maintenance completed | 3 |
| Fan Alert | 1 |
| Temperature warning | 1 |
| SSD failure warning | 1 |
| CRC error 증가 | 1 |
| Link Down | 1 |
| Link Up | 1 |

## 4. 🔥 경보 및 위험 로그 목록 (WARNING / CRITICAL)
| 발생 시간 | 장비명 | 등급 | 이벤트 | 상세 메시지 |
| :--- | :--- | :---: | :--- | :--- |
| 2026-07-03 01:05:00 | `DEMO_CORE_SW_02` | **WARNING** | Fan Alert | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: 198.51.100.2 |
| 2026-07-03 02:05:00 | `EDU_SRV_R04_N12` | **WARNING** | Temperature warning | Chassis temperature reached 42C (Threshold: 40C). IP: 192.0.2.12 |
| 2026-07-03 03:05:00 | `SAMPLE_TOR_SW_01` | **WARNING** | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |

## 5. 🔍 핵심 장애 및 운영 사건 요약
DCO 엔지니어가 주의 깊게 모니터링해야 하는 `CRC 에러 증가`, `포트 다운(Link Down)`, `장애 티켓 에스컬레이션(이관)` 이벤트를 필터링한 결과입니다.

| 발생 시간 | 장비명 | 장애 분류 | 이벤트명 | 세부 조치 메시지 |
| :--- | :--- | :--- | :--- | :--- |
| 2026-07-03 01:10:00 | `DEMO_CORE_SW_02` | <span style='color:red; font-weight:bold;'>TICKET_ESCALATED (장애 티켓 상위 이관)</span> | Ticket escalated | Ticket EDU-TKT-2026-0001 escalated to Local Infrastructure Team. |
| 2026-07-03 02:15:00 | `EDU_SRV_R04_N12` | <span style='color:red; font-weight:bold;'>TICKET_ESCALATED (장애 티켓 상위 이관)</span> | Ticket escalated | Ticket EDU-TKT-2026-0002 escalated to DCO Hardware Support. |
| 2026-07-03 03:05:00 | `SAMPLE_TOR_SW_01` | <span style='color:red; font-weight:bold;'>CRC_ERROR (인터페이스 수신 오류)</span> | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |
| 2026-07-03 03:06:00 | `SAMPLE_TOR_SW_01` | <span style='color:red; font-weight:bold;'>LINK_DOWN (물리적 연결 끊김)</span> | Link Down | Interface Gi0/1 status changed to DOWN. Connection to server lost. |
| 2026-07-03 03:12:00 | `SAMPLE_TOR_SW_01` | <span style='color:red; font-weight:bold;'>TICKET_ESCALATED (장애 티켓 상위 이관)</span> | Ticket escalated | Ticket EDU-TKT-2026-0003 escalated to Onsite Cabling Team. |
| 2026-07-03 03:30:00 | `SAMPLE_TOR_SW_01` | <span style='color:red; font-weight:bold;'>CRC_ERROR (인터페이스 수신 오류)</span> | Normal heartbeat | System status is healthy. Interface Gi0/1 running with 0 CRC errors. IP: 192.0.2.1 |

--- 
*본 분석 보고서는 Python 내장 기능을 통해 자동 생성되었습니다.*
