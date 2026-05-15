# fcfs_sjf_scheduling.py
# Role: Algorithm Engineer (Franz Michael)
# Purpose: Compute FCFS & SJF Scheduling + Turnaround Time + Waiting time

# -------------------
# FCFS ALGORITHM
# -------------------
def fcfs(process_list):
    """
    Input: list of dictionaries e.g., [{"id": "P1", "arrival": 0, "burst": 5}]
    """
    # Sort processes by arrival time
    sorted_proc = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_proc)
    
    completion = [0] * n
    turnaround = [0] * n
    waiting = [0] * n

    # Calculate completion time
    for i in range(n):
        if i == 0:
            completion[i] = sorted_proc[i]["arrival"] + sorted_proc[i]["burst"]
        else:
            # Handling idle time (kung hindi pa dumadating ang susunod na process)
            if sorted_proc[i]["arrival"] > completion[i-1]:
                completion[i] = sorted_proc[i]["arrival"] + sorted_proc[i]["burst"]
            else:
                completion[i] = completion[i-1] + sorted_proc[i]["burst"]

    # Calculate TAT & WT
    for i in range(n):
        turnaround[i] = completion[i] - sorted_proc[i]["arrival"]
        waiting[i] = turnaround[i] - sorted_proc[i]["burst"]

    # Build result list
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
        "avg_turnaround": round(sum(turnaround) / n, 2),
        "avg_waiting": round(sum(waiting) / n, 2)
    }

# -------------------
# SJF ALGORITHM (Non-Preemptive)
# -------------------
def sjf(process_list):
    """
    Shortest Job First: Inuuna ang may pinakamaliit na burst time sa mga dumating na.
    """
    # Sort muna by arrival para sa initial check
    sorted_by_arrival = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_by_arrival)
    
    completed = [False] * n
    completion = [0] * n
    turnaround = [0] * n
    waiting = [0] * n
    
    current_time = 0
    done = 0
    
    while done < n:
        # Kunin lahat ng processes na dumating na at hindi pa tapos
        available = [i for i in range(n) if not completed[i] and sorted_by_arrival[i]["arrival"] <= current_time]
        
        if not available:
            # Kung wala pang dumarating, skip time
            current_time += 1
            continue
            
        # Piliin ang may pinakamababang burst time
        selected = min(available, key=lambda x: sorted_by_arrival[x]["burst"])
        
        # Execute process
        current_time += sorted_by_arrival[selected]["burst"]
        completion[selected] = current_time
        turnaround[selected] = completion[selected] - sorted_by_arrival[selected]["arrival"]
        waiting[selected] = turnaround[selected] - sorted_by_arrival[selected]["burst"]
        
        completed[selected] = True
        done += 1

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
        "algorithm": "SJF (Non-Preemptive)",
        "details": result,
        "avg_turnaround": round(sum(turnaround) / n, 2),
        "avg_waiting": round(sum(waiting) / n, 2)
    }

# --- SAMPLE EXECUTION PARA KAY FRANZ ---
if __name__ == "__main__":
    # Sample Test Case (3 processes)
    test_data = [
        {"id": "P1", "arrival": 0, "burst": 7},
        {"id": "P2", "arrival": 2, "burst": 4},
        {"id": "P3", "arrival": 4, "burst": 1},
        {"id": "P4", "arrival": 5, "burst": 4},
    ]

    print("--- FCFS RESULTS ---")
    fcfs_res = fcfs(test_data)
    for p in fcfs_res['details']:
        print(p)
    print(f"Average Waiting Time: {fcfs_res['avg_waiting']}")

    print("\n--- SJF RESULTS ---")
    sjf_res = sjf(test_data)
    for p in sjf_res['details']:
        print(p)
    print(f"Average Waiting Time: {sjf_res['avg_waiting']}")

