"""
Test explicit clause-level retrieval logic (§Post-Build Issue 3).
Verifies that retrieve_relevant_chunks returns top 1-3 filtered chunks
and retrieves different (correct) chunks for two distinct questions
concerning the same flagship standard (IS 17803:2022).
"""

from backend.services.module1_directory import retrieve_relevant_chunks

def test_distinct_clause_retrieval_same_standard():
    std = "IS 17803:2022"

    # Query 1: Thermal retention / temperature test
    q1 = "What is the thermal retention temperature test for vacuum flasks?"
    chunks1 = retrieve_relevant_chunks(std, q1, top_k=2)

    print("\n[Query 1] Thermal retention:")
    for c in chunks1:
        print(f"  Clause {c['clause']}: {c['content'][:70]}... (score: {c['relevance_score']})")

    # Query 2: Drop test / impact height
    q2 = "What is the drop test height for vacuum flasks?"
    chunks2 = retrieve_relevant_chunks(std, q2, top_k=2)

    print("\n[Query 2] Drop test:")
    for c in chunks2:
        print(f"  Clause {c['clause']}: {c['content'][:70]}... (score: {c['relevance_score']})")

    assert len(chunks1) > 0, "No chunks returned for Query 1"
    assert len(chunks2) > 0, "No chunks returned for Query 2"

    # Query 1 top chunk must be Clause 5.2 (Thermal Retention)
    assert chunks1[0]["clause"] == "5.2", f"Expected Clause 5.2 for Q1, got {chunks1[0]['clause']}"

    # Query 2 top chunk must be Clause 6.1 (Impact & Drop Resistance)
    assert chunks2[0]["clause"] == "6.1", f"Expected Clause 6.1 for Q2, got {chunks2[0]['clause']}"

    # Chunks must be distinct
    assert chunks1[0]["chunk_id"] != chunks2[0]["chunk_id"], "Both queries retrieved the same chunk!"
    print("\nClause-level retrieval test PASSED successfully!")

if __name__ == "__main__":
    test_distinct_clause_retrieval_same_standard()
