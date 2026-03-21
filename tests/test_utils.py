"""Tests for BrokerBench harness utilities."""

from brokerbench.harness.utils import extract_mcq_answer


class TestExtractMcqAnswer:
    # --- Single letter inputs ---

    def test_single_letter(self) -> None:
        assert extract_mcq_answer("B") == "B"

    def test_single_letter_lowercase(self) -> None:
        assert extract_mcq_answer("b") == "B"

    # --- Letter followed by punctuation (standard model output) ---

    def test_letter_dot(self) -> None:
        assert extract_mcq_answer("B. The buyer may rescind the contract.") == "B"

    def test_letter_paren(self) -> None:
        assert extract_mcq_answer("B) The buyer may rescind the contract.") == "B"

    def test_letter_colon(self) -> None:
        assert extract_mcq_answer("B: The buyer may rescind the contract.") == "B"

    # --- "Answer is X" patterns ---

    def test_answer_is_pattern(self) -> None:
        assert extract_mcq_answer("The answer is C.") == "C"

    def test_answer_colon_pattern(self) -> None:
        assert extract_mcq_answer("Answer: D") == "D"

    def test_option_is_pattern(self) -> None:
        assert extract_mcq_answer("The correct option is A.") == "A"

    # --- Prose that should NOT match embedded letters ---

    def test_according_does_not_match_a(self) -> None:
        result = extract_mcq_answer(
            "According to the inspection contingency, the answer is B."
        )
        assert result == "B"

    def test_based_does_not_match_b(self) -> None:
        result = extract_mcq_answer("Based on my analysis, the answer is C.")
        assert result == "C"

    def test_due_does_not_match_d(self) -> None:
        result = extract_mcq_answer("Due to the contract terms, the answer is A.")
        assert result == "A"

    # --- Letter on its own line ---

    def test_letter_on_own_line(self) -> None:
        assert extract_mcq_answer("Let me think about this.\nB\nBecause...") == "B"

    # --- Edge cases ---

    def test_empty_string(self) -> None:
        assert extract_mcq_answer("") is None

    def test_whitespace_only(self) -> None:
        assert extract_mcq_answer("   ") is None

    def test_no_answer_letter(self) -> None:
        result = extract_mcq_answer("I'm not sure about the answer to this question.")
        assert result is None

    def test_letter_with_leading_whitespace(self) -> None:
        assert extract_mcq_answer("  A. First option") == "A"
