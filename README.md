# Text2DNA 

English to DNA sequence converter. Like [DNA Writer](https://earthsciweb.org/js/bio/dna-writer/)

## 📄 개요

Text2DNA는 영문 텍스트를 DNA 시퀀스로 변환하고, DNA 시퀀스를 다시 텍스트로 복원하는 CLI 도구입니다. 각 문자를 고유한 3글자 DNA 코돈(codon)으로 매핑하여 생물학적으로 의미있는 형태로 정보를 저장할 수 있습니다.

## 🚀 설치

```bash
# 저장소 클론
git clone https://github.com/partrita/text2dna.git
cd text2dna

# 의존성 설치 (uv 사용)
uv sync
```

## 💻 사용법

### 기본 명령어

```bash
# 텍스트를 DNA 시퀀스로 인코딩
uv run text2dna encode "Hello World"

# DNA 시퀀스를 텍스트로 디코딩
uv run text2dna decode "ATGCGTCTAATCATCTGTTAA"

# 도움말 보기
uv run text2dna --help
```

### 사용 예시

```bash
# 인코딩 예시
$ uv run text2dna encode "Hello"
ATGCGTCTAATCATCTGTTAA

# 디코딩 예시
$ uv run text2dna decode "ATGCGTCTAATCATCTGTTAA"
HELLO

# 숫자와 특수문자 포함
$ uv run text2dna encode "Hello123."
ATGCGTCTAATCATCTGTATATCGGCGGTGTAA
```

## 📋 지원 문자

- **알파벳**: A-Z (대소문자 구분 없음)
- **숫자**: 0-9
- **특수문자**: . (마침표)
- **기타 문자**: 자동으로 무시됨

## 🧬 DNA 인코딩 테이블

### 숫자 (0-9)

| 문자 | DNA 코드 |
|------|----------|
| 0    | ATA      |
| 1    | TCT      |
| 2    | GCG      |
| 3    | GTG      |
| 4    | AGA      |
| 5    | CGC      |
| 6    | ATT      |
| 7    | ACC      |
| 8    | AGG      |
| 9    | CAA      |

### 알파벳 (A-Z)

| 문자 | DNA 코드 |
|------|----------|
| A    | ACT      |
| B    | CAT      |
| C    | TCA      |
| D    | TAC      |
| E    | CTA      |
| F    | GCT      |
| G    | GTC      |
| H    | CGT      |
| I    | CTG      |
| J    | TGC      |
| K    | TCG      |
| L    | ATC      |
| M    | ACA      |
| N    | CTC      |
| O    | TGT      |
| P    | GAG      |
| Q    | TAT      |
| R    | CAC      |
| S    | TGA      |
| T    | TAG      |
| U    | GAT      |
| V    | GTA      |
| W    | TCC      |
| X    | AGT      |
| Y    | GAC      |
| Z    | GCA      |

### 특수 문자

| 문자  | DNA 코드 | 설명        |
|-------|----------|-------------|
| .     | ACG      | 마침표      |
| START | ATG      | 시작 코돈   |
| STOP  | TAA      | 종료 코돈   |

## ⚙️ 작동 원리

1. **인코딩 과정**:
   - 입력 텍스트를 대문자로 변환
   - 각 문자를 해당하는 3글자 DNA 코돈으로 변환
   - 시작에 START 코돈(ATG), 끝에 STOP 코돈(TAA) 추가

2. **디코딩 과정**:
   - DNA 시퀀스에서 START 코돈(ATG) 찾기
   - START 이후부터 3글자씩 읽어 코돈 단위로 분리
   - STOP 코돈(TAA) 만나면 종료
   - 각 코돈을 해당 문자로 변환


## 🧪 테스트

```bash
# 전체 테스트 실행
uv run pytest

# 특정 테스트 실행
uv run pytest tests/test_encode.py

# 커버리지 확인
uv run pytest --cov=text2dna
```

## 📝 제한사항

- 대소문자, 숫자, 마침표(.)만 지원
- 지원하지 않는 문자는 자동으로 무시됨
- DNA 시퀀스는 START(ATG)와 STOP(TAA) 코돈으로 감싸짐
- 잘못된 형식의 DNA 시퀀스는 에러 메시지 반환


## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🔗 관련 링크

- [DNA Writer (원본)](https://earthsciweb.org/js/bio/dna-writer/)
- [Click 문서](https://click.palletsprojects.com/)
- [uv 문서](https://docs.astral.sh/uv/)
