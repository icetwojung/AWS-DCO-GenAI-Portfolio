> ⚠️ **교육용 샘플 데이터** — 이 문서는 실습 및 교육 목적으로만 작성된 가상의 티켓 양식입니다.
> 실제 장비, 실제 IP, 실제 고객 정보, 실제 계정 정보는 포함되어 있지 않습니다.

---

# 📋 EDU-SAMPLE TICKET

| 항목 | 내용 |
|------|------|
| **티켓 ID** | EDU-TKT-2026-SAMPLE-001 |
| **발생 시간 (UTC)** | 2026-07-06 12:00:00 UTC *(샘플 시간 — 실제 아님)* |
| **발생 시간 (KST)** | 2026-07-06 21:00:00 KST *(샘플 시간 — 실제 아님)* |
| **티켓 생성자** | EDU-ON-CALL-ENGINEER (샘플 역할) |
| **심각도 (Severity)** | SEV-2 *(교육용 예시 등급)* |
| **현재 상태** | OPEN — 조사 중 (샘플) |
| **Escalation 필요 여부** | 예 — 샘플 Escalation 시나리오 |

---

## 🖥️ 샘플 장비 정보

| 항목 | 내용 |
|------|------|
| **장비명** | SAMPLE_TOR_SW_01 |
| **장비 유형** | TOR (Top of Rack) Switch — 교육용 샘플 |
| **위치** | SAMPLE-RACK-A1 / SAMPLE-DATACENTER-EDU |
| **시리얼 번호** | SAMPLE-SERIAL-XXXX *(실제 시리얼 아님)* |
| **관리 IP** | 192.0.2.X *(RFC 5737 문서용 주소 — 실제 아님)* |

---

## 📣 이벤트 요약

```
[SAMPLE LOG — 교육용]
2026-07-06 11:45:00 UTC  SAMPLE_TOR_SW_01  CRC error count increasing on interface Gi0/X
2026-07-06 11:52:00 UTC  SAMPLE_TOR_SW_01  CRC error threshold exceeded (SAMPLE threshold: 1000/5min)
2026-07-06 12:00:00 UTC  SAMPLE_TOR_SW_01  Link Down detected on interface Gi0/X
2026-07-06 12:01:00 UTC  SAMPLE_TOR_SW_01  Alarm raised — ticket auto-generated (SAMPLE)
```

> 위 로그는 실제 장비에서 수집된 데이터가 아닌 교육용으로 작성된 샘플 로그입니다.

---

## 🔍 관찰 내용

- **CRC 오류 증가**: `SAMPLE_TOR_SW_01`의 특정 인터페이스(`Gi0/X`)에서 CRC(Cyclic Redundancy Check) 오류 카운터가 급격히 증가하는 패턴이 샘플 로그 상에서 관찰됨
- **Link Down 이벤트**: CRC 오류 임계치 초과 후 약 8분 뒤 해당 인터페이스에서 Link Down 이벤트 발생 (샘플 시나리오)
- **반복 여부**: 이 샘플 티켓에서는 최근 24시간 내 동일 인터페이스에서 2회 발생한 것으로 가정
- **영향 범위 (샘플 추정)**: 해당 TOR 스위치에 연결된 SAMPLE 서버 그룹에 트래픽 영향 가능성 (실습 시나리오 기준)

---

## ⚡ 심각도 판단 근거 (교육용)

| 항목 | 판단 내용 |
|------|----------|
| 서비스 영향 | 샘플 서버 그룹 연결 단절 가능성 |
| 자동 복구 여부 | 샘플 시나리오에서 자동 복구 미확인 |
| 반복성 | 24시간 내 재발 (샘플 가정) |
| Escalation | 상위 엔지니어 검토 필요 (샘플 절차) |

---

## 🚨 Escalation 정보 (교육용 절차 예시)

- **Escalation 대상**: SAMPLE-NETWORK-TEAM / EDU-SENIOR-ENGINEER
- **Escalation 사유**: CRC 오류 반복 및 Link Down 재발 — 하드웨어 결함 가능성 검토 필요 (샘플 시나리오)
- **Escalation 채널**: SAMPLE-ONCALL-CHANNEL (실제 채널 아님)

> 실제 에스컬레이션 절차는 소속 팀의 Runbook을 따르십시오. 이 내용은 참고용 예시입니다.

---

## 🔒 보안 주의사항

- 이 티켓에 포함된 모든 정보는 **교육용 샘플**입니다.
- 실제 장비명, 계정 정보, 고객 정보, IP 주소를 이 형식에 입력하지 마십시오.
- 실습 환경에서 생성된 티켓은 실제 운영 시스템과 연동하지 않습니다.
- 외부 시스템 접근 또는 실제 네트워크 명령 실행 금지.

---

## 📝 메모 / 다음 조치 (샘플)

- [ ] 샘플 로그 재검토 — CRC 오류 패턴 분석 실습
- [ ] 샘플 장비 인터페이스 상태 확인 절차 학습
- [ ] 원인 단정 금지 — 추가 샘플 데이터 수집 후 판단
- [ ] 랙 체크리스트(`rack_checklist.md`) 참조하여 확인 항목 기록

---

##변경 테스트

*최종 수정: 2026-07-06 | 작성자: EDU-SAMPLE-ENGINEER | 버전: v1.0-EDU*
