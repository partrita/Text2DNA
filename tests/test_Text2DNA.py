import pytest
from click.testing import CliRunner
from Text2DNA.main import encode, decode, cli, encode_table, decode_table


class TestEncode:
    """인코딩 함수 테스트"""
    
    def test_encode_single_character(self):
        """단일 문자 인코딩 테스트"""
        assert encode('A') == 'ATGACTTAA'
        assert encode('H') == 'ATGCGTTAA'
        assert encode('0') == 'ATGATATAA'
    
    def test_encode_hello(self):
        """HELLO 인코딩 테스트"""
        expected = 'ATGCGTCTAATCATCTGTTAA'
        assert encode('HELLO') == expected
        assert encode('hello') == expected  # 대소문자 구분 없음
        assert encode('Hello') == expected
    
    def test_encode_numbers(self):
        """숫자 인코딩 테스트"""
        result = encode('123')
        assert result.startswith('ATG')
        assert result.endswith('TAA')
        assert 'TCT' in result  # 1
        assert 'GCG' in result  # 2
        assert 'GTG' in result  # 3
    
    def test_encode_mixed_text(self):
        """혼합 텍스트 인코딩 테스트"""
        result = encode('A1B2.')
        assert result.startswith('ATG')
        assert result.endswith('TAA')
        # A=ACT, 1=TCT, B=CAT, 2=GCG, .=ACG
        expected = 'ATGACTTCTCATGCGACGTAA'
        assert result == expected
    
    def test_encode_empty_string(self):
        """빈 문자열 인코딩 테스트"""
        result = encode('')
        assert result == 'ATGTAA'  # START + STOP만
    
    def test_encode_unsupported_characters(self):
        """지원하지 않는 문자 테스트"""
        result = encode('A!@#B')
        expected = encode('AB')  # 특수문자는 무시되어야 함
        assert result == expected
    
    def test_encode_spaces_ignored(self):
        """공백 무시 테스트"""
        result = encode('A B C')
        expected = encode('ABC')
        assert result == expected


class TestDecode:
    """디코딩 함수 테스트"""
    
    def test_decode_single_character(self):
        """단일 문자 디코딩 테스트"""
        assert decode('ATGACTTAA') == 'A'
        assert decode('ATGCGTTAA') == 'H'
        assert decode('ATGATATAAA') == '0'
    
    def test_decode_hello(self):
        """HELLO 디코딩 테스트"""
        dna = 'ATGCGTCTAATCATCTGTTAA'
        assert decode(dna) == 'HELLO'
        assert decode(dna.lower()) == 'HELLO'  # 소문자 입력도 처리
    
    def test_decode_numbers(self):
        """숫자 디코딩 테스트"""
        dna = encode('123')
        assert decode(dna) == '123'
    
    def test_decode_mixed_text(self):
        """혼합 텍스트 디코딩 테스트"""
        original = 'HELLO123.'
        dna = encode(original)
        assert decode(dna) == original
    
    def test_decode_invalid_no_start(self):
        """START 코돈이 없는 경우"""
        result = decode('CGTCTAATCATCTGTTAA')
        assert 'Invalid sequence: missing START codon.' in result
    
    def test_decode_invalid_no_stop(self):
        """STOP 코돈이 없는 경우"""
        result = decode('ATGCGTCTAATCATCTGT')
        assert result == 'HELLO'  # 불완전한 시퀀스는 가능한 만큼만 디코딩
    
    def test_decode_incomplete_codon(self):
        """불완전한 코돈 처리"""
        result = decode('ATGCGTCTAA')  # H + 불완전한 코돈
        assert result == 'HE'
    
    def test_decode_unknown_codon(self):
        """알 수 없는 코돈 처리"""
        result = decode('ATGAAACGTTAA')  # AAA는 정의되지 않은 코돈
        assert result == 'H'  # 알 수 없는 코돈은 무시
    
    def test_decode_start_in_middle(self):
        """중간에 START 코돈이 있는 경우"""
        result = decode('CCCATGCGTTAA')  # 앞에 쓰레기 + ATG + H + STOP
        assert result == 'H'


class TestRoundTrip:
    """인코딩-디코딩 왕복 테스트"""
    
    def test_roundtrip_alphabet(self):
        """알파벳 왕복 테스트"""
        original = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        encoded = encode(original)
        decoded = decode(encoded)
        assert decoded == original
    
    def test_roundtrip_numbers(self):
        """숫자 왕복 테스트"""
        original = '0123456789'
        encoded = encode(original)
        decoded = decode(encoded)
        assert decoded == original
    
    def test_roundtrip_mixed(self):
        """혼합 텍스트 왕복 테스트"""
        original = 'HELLO123WORLD.'
        encoded = encode(original)
        decoded = decode(encoded)
        assert decoded == original
    
    def test_roundtrip_case_insensitive(self):
        """대소문자 무관 왕복 테스트"""
        original = 'Hello World'
        encoded = encode(original)
        decoded = decode(encoded)
        assert decoded == 'HELLOWORLD'  # 대문자로 변환되고 공백 제거


class TestEncodeTable:
    """인코딩 테이블 무결성 테스트"""
    
    def test_encode_table_completeness(self):
        """인코딩 테이블 완성도 검사"""
        # 모든 필요한 문자가 있는지 확인
        expected_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.')
        actual_chars = set(k for k in encode_table.keys() if k not in ('START', 'STOP'))
        assert expected_chars == actual_chars
    
    def test_decode_table_consistency(self):
        """디코딩 테이블 일관성 검사"""
        # encode_table과 decode_table의 일관성 확인
        for char, codon in encode_table.items():
            assert decode_table[codon] == char
    
    def test_no_duplicate_codons(self):
        """중복 코돈 검사"""
        codons = list(encode_table.values())
        assert len(codons) == len(set(codons)), "중복된 코돈이 있습니다"
    
    def test_codon_length(self):
        """모든 코돈이 3글자인지 확인"""
        for char, codon in encode_table.items():
            assert len(codon) == 3, f"코돈 {codon} (문자: {char})의 길이가 3이 아닙니다"
    
    def test_valid_nucleotides(self):
        """유효한 뉴클레오타이드만 사용되는지 확인"""
        valid_nucleotides = set('ATCG')
        for char, codon in encode_table.items():
            codon_nucleotides = set(codon)
            assert codon_nucleotides.issubset(valid_nucleotides), \
                f"코돈 {codon} (문자: {char})에 유효하지 않은 뉴클레오타이드가 있습니다"


class TestCLI:
    """CLI 인터페이스 테스트"""
    
    def setup_method(self):
        """테스트 설정"""
        self.runner = CliRunner()
    
    def test_cli_encode_command(self):
        """CLI 인코딩 명령어 테스트"""
        result = self.runner.invoke(cli, ['encode', 'HELLO'])
        assert result.exit_code == 0
        assert result.output.strip() == 'ATGCGTCTAATCATCTGTTAA'
    
    def test_cli_decode_command(self):
        """CLI 디코딩 명령어 테스트"""
        result = self.runner.invoke(cli, ['decode', 'ATGCGTCTAATCATCTGTTAA'])
        assert result.exit_code == 0
        assert result.output.strip() == 'HELLO'
    
    def test_cli_help(self):
        """CLI 도움말 테스트"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'DNA Writer CLI' in result.output
    
    def test_cli_encode_help(self):
        """CLI 인코딩 명령어 도움말 테스트"""
        result = self.runner.invoke(cli, ['encode', '--help'])
        assert result.exit_code == 0
        assert '문자열을 DNA 코드로 인코딩합니다' in result.output
    
    def test_cli_decode_help(self):
        """CLI 디코딩 명령어 도움말 테스트"""
        result = self.runner.invoke(cli, ['decode', '--help'])
        assert result.exit_code == 0
        assert 'DNA 코드를 문자열로 디코딩합니다' in result.output
    
    def test_cli_invalid_command(self):
        """존재하지 않는 명령어 테스트"""
        result = self.runner.invoke(cli, ['invalid'])
        assert result.exit_code != 0


class TestEdgeCases:
    """경계 조건 테스트"""
    
    def test_very_long_text(self):
        """매우 긴 텍스트 처리"""
        original = 'A' * 1000
        encoded = encode(original)
        decoded = decode(encoded)
        assert decoded == original
    
    def test_all_supported_characters(self):
        """지원되는 모든 문자 테스트"""
        original = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.'
        encoded = encode(original)
        decoded = decode(encoded)
        assert decoded == original
    
    def test_special_characters_mixed(self):
        """특수문자가 섞인 경우"""
        result = encode('A!B@C#D$')
        expected = encode('ABCD')
        assert result == expected
    
    def test_decode_malformed_sequence(self):
        """잘못된 형태의 DNA 시퀀스"""
        # START 없음
        assert 'Invalid sequence' in decode('CGTCTAATC')
        
        # 너무 짧은 시퀀스
        assert 'Invalid sequence' in decode('AT')
        
        # 빈 시퀀스
        assert 'Invalid sequence' in decode('')


# 성능 테스트 (선택사항)
class TestPerformance:
    """성능 테스트"""
    
    @pytest.mark.performance
    def test_encode_performance(self):
        """인코딩 성능 테스트"""
        import time
        
        large_text = 'HELLO' * 1000
        start_time = time.time()
        result = encode(large_text)
        end_time = time.time()
        
        assert end_time - start_time < 1.0  # 1초 이내
        assert len(result) > 0
    
    @pytest.mark.performance
    def test_decode_performance(self):
        """디코딩 성능 테스트"""
        import time
        
        large_text = 'HELLO' * 1000
        encoded = encode(large_text)
        
        start_time = time.time()
        result = decode(encoded)
        end_time = time.time()
        
        assert end_time - start_time < 1.0  # 1초 이내
        assert result == large_text


# 픽스처 (공통 테스트 데이터)
@pytest.fixture
def sample_texts():
    """테스트용 샘플 텍스트"""
    return [
        'HELLO',
        'WORLD',
        '123',
        'ABC123',
        'HELLO.WORLD',
        '',
        'A',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.'
    ]


@pytest.fixture
def sample_dna_sequences():
    """테스트용 샘플 DNA 시퀀스"""
    return [
        'ATGCGTCTAATCATCTGTTAA',  # HELLO
        'ATGACTTAA',               # A
        'ATGTAA',                  # 빈 문자열
        'ATGATATAAA',              # 0
    ]


# 통합 테스트
class TestIntegration:
    """통합 테스트"""
    
    def test_full_workflow(self, sample_texts):
        """전체 워크플로우 테스트"""
        for text in sample_texts:
            # 지원하지 않는 문자 제거 (테스트용)
            clean_text = ''.join(c for c in text.upper() 
                               if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.')
            
            encoded = encode(text)
            decoded = decode(encoded)
            
            assert decoded == clean_text
    
    def test_cli_workflow(self):
        """CLI 전체 워크플로우 테스트"""
        runner = CliRunner()
        
        # 인코딩
        encode_result = runner.invoke(cli, ['encode', 'HELLO'])
        assert encode_result.exit_code == 0
        encoded_dna = encode_result.output.strip()
        
        # 디코딩
        decode_result = runner.invoke(cli, ['decode', encoded_dna])
        assert decode_result.exit_code == 0
        assert decode_result.output.strip() == 'HELLO'