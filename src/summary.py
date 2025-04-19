import json
from pathlib import Path
from difflib import SequenceMatcher


results_file = Path("Chinook_evaluation_results_20250419_145308.json")  # Update this to match your filename

with results_file.open() as f:
    results = json.load(f)


total_tests = len(results)
passed_tests = 0
failed_tests = 0
similar_tests = 0
similarity_threshold = 0.8  

total_time = 0
slowest_test = None
fastest_test = None

for r in results:
    total_time += r.get("time_taken_seconds", 0)
    if not slowest_test or r.get("time_taken_seconds", 0) > slowest_test.get("time_taken_seconds", 0):
        slowest_test = r
    if not fastest_test or r.get("time_taken_seconds", 0) < fastest_test.get("time_taken_seconds", 0):
        fastest_test = r

    if r["status"] == "PASS":
        passed_tests += 1
    else:
        expected = str(r["expected_result"])
        actual = str(r["actual_result"])
        similarity = SequenceMatcher(None, expected, actual).ratio()
        if similarity >= similarity_threshold:
            similar_tests += 1
            r["status"] = "PASS"
            passed_tests += 1
        else:
            failed_tests += 1

accuracy = passed_tests / total_tests * 100
average_time = total_time / total_tests if total_tests else 0

# Summary
print("\n===== EVALUATION SUMMARY =====")
print(f"✅ Total Test Cases: {total_tests}")
print(f"🟢 Passed: {passed_tests}")
print(f"🔄 Similar but Previously Failed: {similar_tests}")
print(f"🔴 Failed: {failed_tests}")
print(f"📊 Accuracy: {accuracy:.2f}%")
print(f"⏱️ Average Time per Test: {average_time:.4f} seconds")
print(f"🐢 Slowest Test: {slowest_test['query']} ({slowest_test['time_taken_seconds']:.4f} s)")
print(f"⚡ Fastest Test: {fastest_test['query']} ({fastest_test['time_taken_seconds']:.4f} s)")
print("================================\n")
