# [교육용 샘플 데이터 / FOR EDUCATIONAL USE ONLY]

> [!NOTE]
> 본 문서는 교육 목적으로 작성된 샘플 데이터이며, 실제 AWS 환경, 실제 장비 또는 실제 고객 정보와 무관합니다.
> This document is a sample dataset created for educational purposes only. It is not associated with any real AWS environment, production devices, or customer information.

## 티켓 정보 (Ticket Information)
- **티켓 ID (Ticket ID)**: EDU-TICKET-2026-0001
- **발생 시간 (Occurrence Time)**: 2026-07-05 22:40:00 KST
- **샘플 장비명 (Sample Device Name)**: SAMPLE_TOR_SW_01
- **이벤트 (Event)**: Port Interface CRC Error Increase & Link Down Event
- **심각도 (Severity)**: SEV-2 (EDU-MAJOR)
- **Escalation 필요 여부 (Escalation Required)**: Yes (EDU Escalation Path)

## 관찰 내용 (Observations)
1. **CRC Error Accumulation**: 
   - 2026-07-05 22:30:00 KST 기점으로 `SAMPLE_TOR_SW_01` 장비의 `Ethernet1/1` 인터페이스에서 CRC 에러 카운터가 급격히 증가함.
   - 단시간 내에 누적 CRC 에러 수치가 임계치를 초과하여 경고 알람 발생.
2. **Link Down Event**:
   - 에러 증가 현상 지속 후, 2026-07-05 22:40:00 KST에 `Ethernet1/1` 인터페이스가 `Down` 상태로 천이됨.
   - 포트 상태: `SAMPLE_TOR_SW_01:Ethernet1/1` - status: down (protocol: down)

## 보안 주의사항 (Security Cautions)
- **계정 및 접근 제어**: 본 장비는 교육용 가상 환경 시뮬레이션을 위한 대상입니다. 어떠한 경우에도 실제 네트워크 대역 및 운영 환경의 패스워드, 개인 키, Access Key를 본 티켓이나 관련 기록에 포함하지 마십시오.
- **정보 노출 방지**: 실제 장비의 일련번호(Serial Number), IP 주소, 또는 실제 고객 환경 정보(Account ID, VPC ID 등)를 기재하는 것은 엄격히 금지됩니다. 모든 식별자는 `SAMPLE_` 또는 `EDU_` 접두사를 사용해야 합니다.
