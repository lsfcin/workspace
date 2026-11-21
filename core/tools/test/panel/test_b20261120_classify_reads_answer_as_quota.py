# T1 regression b20261120-classify-reads-answer-as-quota: a clean, long answer that talks about quota or login is an answer, not a spent quota.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import workers  # noqa: E402

AGY_QUOTA = 'Error: Individual quota reached. Resets in 73h6m3s.\nAGY_ERROR: {"status":"RESOURCE_EXHAUSTED"}'
ANSWER = ('Verdict: classify must not scan the answer for "quota reached" or "unauthorized"; '
          'a rate limit is an API error, not a word. ' * 8)


def test_b20261120_a_long_clean_answer_about_quota_is_ok():
    """argon's verdicts on quota detection (11-20) and on LoopForge (11-21) were thrown away."""
    assert workers.classify(0, ANSWER) == 'ok'


def test_b20261120_a_short_notice_or_a_failed_exit_is_still_read_for_marks():
    assert workers.classify(0, AGY_QUOTA) == 'quota'
    assert workers.classify(1, ANSWER) == 'quota'
