from brain.fusion import fuse_results

def test_fuse_multiple_responses():
    responses = ["A", "B", "[model x error] boom"]
    fused = fuse_results(responses)
    assert "A" in fused and "B" in fused
    assert "error" not in fused.lower()
