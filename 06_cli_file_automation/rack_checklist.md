# [교육용 샘플 데이터 / FOR EDUCATIONAL USE ONLY]

> [!NOTE]
> 본 문서는 교육 목적으로 작성된 샘플 데이터이며, 실제 AWS 환경, 실제 장비 또는 실제 고객 정보와 무관합니다.
> This document is a sample dataset created for educational purposes only. It is not associated with any real AWS environment, production devices, or customer information.

## 교육용 랙 및 티켓 확인 체크리스트 (Educational Rack & Ticket Checklist)

본 체크리스트는 제공된 샘플 로그와 샘플 티켓 정보를 분석하고 기록하기 위해 작성된 절차서입니다.

---

### [단계 1] 기본 정보 분석 및 기록
- [ ] **발생 시간 확인 (Occurrence Time)**
  - 샘플 티켓 및 로그 상에서 최초 에러가 감지된 정확한 시각과 링크 다운이 발생한 타임스탬프를 대조하여 기록하였는가?
- [ ] **샘플 장비명 확인 (Sample Device Name)**
  - 문제가 발생한 대상 장비명이 `SAMPLE_` 또는 `EDU_` 접두사를 포함하는 교육용 가상 장비명(`SAMPLE_TOR_SW_01` 등)이 맞는지 확인하였는가? (실제 프로덕션 장비명이 포함되어 있지 않은지 더블 체크)
- [ ] **반복 여부 확인 (Recurrence Check)**
  - 과거 이력 로그나 관련 교육용 티켓 목록에서 동일 장비 또는 동일 인터페이스에 유사한 CRC 에러 발생 및 링크 다운 이력이 존재하는지 검토하였는가?

---

### [단계 2] 상태 및 주의사항 점검
- [ ] **Ticket 상태 확인 (Ticket Status Check)**
  - 현재 해당 샘플 티켓의 상태(예: Open, In-Progress, Pending-Escalation 등)가 올바르게 업데이트되어 있는지 확인하였는가?
- [ ] **원인 단정 금지 (No Premature Conclusions)**
  - *중요*: CRC 에러 및 링크 다운의 원인을 "케이블 불량"이나 "포트 고장" 등으로 성급하게 단정 짓지 않고, 가능한 다양한 물리 계층 및 데이터 링크 계층 요소를 열어두고 객관적인 팩트만 기술하였는가?
  - (예: "케이블이 고장났다" (X) -> "인터페이스에서 물리적 CRC 에러 누적 후 링크 다운 상태로 감지됨" (O))

---

### [단계 3] 보고서 초안 작성 및 메모
- [ ] **보고서 초안 작성 메모 (Drafting Report Notes)**
  - 확인한 사실관계를 바탕으로 교육 보고서 초안을 작성하기 위해 아래의 메모 템플릿을 채웠는가?

#### [메모 작성란 / Notes Template]
- **분석 대상 티켓**: 
- **발생 시각 및 장비**: 
- **팩트 요약 (오류 로그/이벤트 요약)**: 
- **향후 가상 시나리오 분석 단계 제안**: 
