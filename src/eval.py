import json
from pathlib import Path
from agent_graph.tool_chinook_sqlagent import ChinookSQLAgent
from agent_graph.load_tools_config import LoadToolsConfig
import time
import datetime

TOOLS_CFG = LoadToolsConfig()

with open("testData.json") as f:
    test_data = json.load(f)

agent = ChinookSQLAgent(
    sqldb_directory=TOOLS_CFG.chinook_sqldb_directory,
    llm=TOOLS_CFG.chinook_sqlagent_llm,
    llm_temerature=TOOLS_CFG.chinook_sqlagent_llm_temperature
)

results = []

for idx, case in enumerate(test_data):
    query = case["prompt"]
    expected_result = case["sql_res"]

    print(f"\n=== Test Case {idx + 1}: {query} ===")

    start_time = time.perf_counter()

    try:
        generated_sql = agent.full_chain.invoke({"question": query})
        # corrected_sql = agent.validate_query(generated_sql)
        actual_result = agent.db.run(generated_sql)

        end_time = time.perf_counter()
        elapsed_time = round(end_time - start_time, 4)

        passed = actual_result.strip() == expected_result.strip()
        result = {
            "query": query,
            "generated_sql": generated_sql,
            # "corrected_sql": corrected_sql,
            "expected_result": expected_result,
            "actual_result": actual_result,
            "status": "PASS" if passed else "FAIL",
            "time_taken_seconds": elapsed_time
        }

    except Exception as e:
        end_time = time.perf_counter()
        elapsed_time = round(end_time - start_time, 4)

        result = {
            "query": query,
            "generated_sql": "ERROR",
            # "corrected_sql": "ERROR",
            "expected_result": expected_result,
            "actual_result": str(e),
            "status": "FAIL",
            "time_taken_seconds": elapsed_time
        }

    print(result["status"])
    print(result["actual_result"])

    results.append(result)

output_path = Path(f"Chinook_evaluation_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
with output_path.open("w") as f:
    json.dump(results, f, indent=4)

print(f"\nEvaluation completed. Results saved to: {output_path.resolve()}")
