# 📊 AWS DCO 교육용 샘플 로그 분석 보고서

- **작성 일시:** 2026-07-18 21:01:00 (KST)
- **분석 대상 파일:** `sample_dco_log.txt`

## 1. 전체 로그 요약 통계
- **총 수집 로그 라인:** `140` 줄

### ■ 심각도(Severity)별 분포
| 심각도 (Severity) | 로그 개수 (건) | 비율 (%) |
| :--- | :--- | :--- |
| **INFO** | 135건 | 96.4% |
| **WARNING** | 3건 | 2.1% |
| **ERROR** | 2건 | 1.4% |
| **CRITICAL** | 0건 | 0.0% |

### ■ 이벤트(Event) 타입별 발생 현황
| 이벤트 타입 (Event Type) | 발생 횟수 (건) |
| :--- | :--- |
| `Normal heartbeat` | 125건 |
| `Ticket opened` | 3건 |
| `Ticket escalated` | 3건 |
| `Maintenance completed` | 3건 |
| `Fan Alert` | 1건 |
| `Temperature warning` | 1건 |
| `SSD failure warning` | 1건 |
| `CRC error 증가` | 1건 |
| `Link Down` | 1건 |
| `Link Up` | 1건 |

## 2. 주의 및 위험 로그 상세 목록 (WARNING, ERROR & CRITICAL)
DCO 장비 점검 시 우선적으로 조치가 필요한 상태 주의/경고 로그 목록입니다.

| 발생 시간 | 대상 장비 | 심각도 | 이벤트 유형 | 메시지 내용 |
| :--- | :--- | :--- | :--- | :--- |
| `2026-07-03 01:05:00` | `DEMO_CORE_SW_02` | 🟡 WARNING | `Fan Alert` | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: 198.51.100.2 |
| `2026-07-03 02:05:00` | `EDU_SRV_R04_N12` | 🟡 WARNING | `Temperature warning` | Chassis temperature reached 42C (Threshold: 40C). IP: 192.0.2.12 |
| `2026-07-03 02:10:00` | `EDU_SRV_R04_N12` | 🔴 **ERROR** | `SSD failure warning` | Drive Slot 3 SSD wearout indicator FAILING (SMART wear 96%). IP: 192.0.2.12 |
| `2026-07-03 03:05:00` | `SAMPLE_TOR_SW_01` | 🟡 WARNING | `CRC error 증가` | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |
| `2026-07-03 03:06:00` | `SAMPLE_TOR_SW_01` | 🔴 **ERROR** | `Link Down` | Interface Gi0/1 status changed to DOWN. Connection to server lost. |

## 3. 핵심 장애 인시던트 분석 요약
네트워크 링크 장애(`LINK_DOWN`), 에러율 급증(`CRC_ERROR`), 티켓 이관 및 에스컬레이션(`TICKET_ESCALATED`)과 관련된 고순도 인시던트만 추출한 요약입니다.

### 인시던트 #1: [🚨 티켓 에스컬레이션 완료]
- **시간 / 장비:** `2026-07-03 01:06:00` | `DEMO_CORE_SW_02`
- **상태:** **INFO** (이벤트: `Ticket opened`)
- **원문 내용:** `Ticket EDU-TKT-2026-0001 created for Fan module 2 failure alert.`

### 인시던트 #2: [🚨 티켓 에스컬레이션 완료]
- **시간 / 장비:** `2026-07-03 01:10:00` | `DEMO_CORE_SW_02`
- **상태:** **INFO** (이벤트: `Ticket escalated`)
- **원문 내용:** `Ticket EDU-TKT-2026-0001 escalated to Local Infrastructure Team.`

### 인시던트 #3: [🚨 티켓 에스컬레이션 완료]
- **시간 / 장비:** `2026-07-03 02:11:00` | `EDU_SRV_R04_N12`
- **상태:** **INFO** (이벤트: `Ticket opened`)
- **원문 내용:** `Ticket EDU-TKT-2026-0002 created for server SSD replacement schedule.`

### 인시던트 #4: [🚨 티켓 에스컬레이션 완료]
- **시간 / 장비:** `2026-07-03 02:15:00` | `EDU_SRV_R04_N12`
- **상태:** **INFO** (이벤트: `Ticket escalated`)
- **원문 내용:** `Ticket EDU-TKT-2026-0002 escalated to DCO Hardware Support.`

### 인시던트 #5: [🔄 CRC 에러 감지]
- **시간 / 장비:** `2026-07-03 03:05:00` | `SAMPLE_TOR_SW_01`
- **상태:** **WARNING** (이벤트: `CRC error 증가`)
- **원문 내용:** `Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1`

### 인시던트 #6: [🔌 링크 다운 발생]
- **시간 / 장비:** `2026-07-03 03:06:00` | `SAMPLE_TOR_SW_01`
- **상태:** **ERROR** (이벤트: `Link Down`)
- **원문 내용:** `Interface Gi0/1 status changed to DOWN. Connection to server lost.`

### 인시던트 #7: [🚨 티켓 에스컬레이션 완료]
- **시간 / 장비:** `2026-07-03 03:07:00` | `SAMPLE_TOR_SW_01`
- **상태:** **INFO** (이벤트: `Ticket opened`)
- **원문 내용:** `Ticket EDU-TKT-2026-0003 created for Gi0/1 port offline.`

### 인시던트 #8: [🚨 티켓 에스컬레이션 완료]
- **시간 / 장비:** `2026-07-03 03:12:00` | `SAMPLE_TOR_SW_01`
- **상태:** **INFO** (이벤트: `Ticket escalated`)
- **원문 내용:** `Ticket EDU-TKT-2026-0003 escalated to Onsite Cabling Team.`

### 인시던트 #9: [🔌 링크 다운 발생]
- **시간 / 장비:** `2026-07-03 03:26:00` | `SAMPLE_TOR_SW_01`
- **상태:** **INFO** (이벤트: `Link Up`)
- **원문 내용:** `Interface Gi0/1 status changed to UP. Line protocol status is UP.`

### 인시던트 #10: [🔄 CRC 에러 감지]
- **시간 / 장비:** `2026-07-03 03:30:00` | `SAMPLE_TOR_SW_01`
- **상태:** **INFO** (이벤트: `Normal heartbeat`)
- **원문 내용:** `System status is healthy. Interface Gi0/1 running with 0 CRC errors. IP: 192.0.2.1`
