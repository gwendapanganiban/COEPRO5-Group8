# scheduling_algorithms.py
# Author: Franz Michael
# Role: Algorithm Engineer

def fcfs(process_list):
    """
    First-Come, First-Served (FCFS) Scheduling Algorithm
    Input: List of dictionaries e.g., [{"id": "P1", "arrival": 0, "burst": 5}]
    """
    sorted_proc = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_proc)

    completion = [0] * n
    turnaround = [0] * n
    waiting = [0] * n
    total_tat = 0
    total_wt = 0

    for i in range(n):
        if i == 0:
            completion[i] = sorted_proc[i]["arrival"] + sorted_proc[i]["burst"]
        else:
            if completion[i-1] < sorted_proc[i]["arrival"]:
                completion[i] = sorted_proc[i]["arrival"] + sorted_proc[i]["burst"]
            else:
                completion[i] = completion[i-1] + sorted_proc[i]["burst"]

        turnaround[i] = completion[i] - sorted_proc[i]["arrival"]
        waiting[i] = turnaround[i] - sorted_proc[i]["burst"]
        total_tat += turnaround[i]
        total_wt += waiting[i]

    result = []
    for i in range(n):
        result.append({
            "pid": sorted_proc[i]["id"],
            "arrival": sorted_proc[i]["arrival"],
            "burst": sorted_proc[i]["burst"],
            "completion_time": completion[i],
            "turnaround_time": turnaround[i],
            "waiting_time": waiting[i]
        })

    return {
        "algorithm": "FCFS",
        "details": result,
        "avg_turnaround": round(total_tat / n, 2),
        "avg_waiting": round(total_wt / n, 2)
    }


def sjf(process_list):
    """
    Shortest Job First (SJF) - Non-Preemptive
    Input: List of dictionaries e.g., [{"id": "P1", "arrival": 0, "burst": 5}]
    """
    sorted_by_arrival = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_by_arrival)

    completed = [False] * n
    completion = [0] * n
    turnaround = [0] * n
    waiting = [0] * n
    total_tat = 0
    total_wt = 0
    current_time = 0
    done = 0

    while done < n:
        available = [i for i in range(n) if not completed[i] and sorted_by_arrival[i]["arrival"] <= current_time]

        if not available:
            current_time += 1
            continue

        selected = min(available, key=lambda x: sorted_by_arrival[x]["burst"])

        current_time += sorted_by_arrival[selected]["burst"]
        completion[selected] = current_time
        completed[selected] = True
        done += 1

    for i in range(n):
        turnaround[i] = completion[i] - sorted_by_arrival[i]["arrival"]
        waiting[i] = turnaround[i] - sorted_by_arrival[i]["burst"]
        total_tat += turnaround[i]
        total_wt += waiting[i]

    result = []
    for i in range(n):
        result.append({
            "pid": sorted_by_arrival[i]["id"],
            "arrival": sorted_by_arrival[i]["arrival"],
            "burst": sorted_by_arrival[i]["burst"],
            "completion_time": completion[i],
            "turnaround_time": turnaround[i],
            "waiting_time": waiting[i]
        })

    return {
        "algorithm": "SJF",
        "details": result,
        "avg_turnaround": round(total_tat / n, 2),
        "avg_waiting": round(total_wt / n, 2)
    }


if __name__ == "__main__":
    sample_processes = [
        {"id": "P1", "arrival": 0, "burst": 7},
        {"id": "P2", "arrival": 1, "burst": 4},
        {"id": "P3", "arrival": 2, "burst": 1},
        {"id": "P4", "arrival": 3, "burst": 3}
    ]

    fcfs_result = fcfs(sample_processes)
    sjf_result = sjf(sample_processes)

    print("===== FCFS EXECUTION RESULTS =====")
    for p in fcfs_result["details"]:
        print(p)
    print(f"Average Turnaround Time: {fcfs_result['avg_turnaround']}")
    print(f"Average Waiting Time: {fcfs_result['avg_waiting']}\n")

    print("===== SJF EXECUTION RESULTS =====")
    for p in sjf_result["details"]:
        print(p)
    print(f"Average Turnaround Time: {sjf_result['avg_turnaround']}")
    print(f"Average Waiting Time: {sjf_result['avg_waiting']}")
