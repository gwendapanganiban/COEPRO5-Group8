from collections import deque

def finalize_results(algo_name, processes, completion):
    """Calculates metrics and formats the output dictionary."""
    n = len(processes)
    if n == 0: return None
    
    details = []
    total_tat, total_wt = 0, 0
    
    for i in range(n):
        tat = completion[i] - processes[i]["arrival"]
        wt = tat - processes[i]["burst"]
        total_tat += tat
        total_wt += wt
        
        process_result = processes[i].copy()
        process_result.update({
            "completion_time": completion[i],
            "turnaround_time": tat,
            "waiting_time": wt
        })
        details.append(process_result)
        
    return {
        "algorithm": algo_name,
        "details": details,
        "avg_turnaround": round(total_tat / n, 2),
        "avg_waiting": round(total_wt / n, 2)
    }

def fcfs(process_list):
    sorted_proc = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_proc)
    completion = [0] * n
    current_time = 0
    for i in range(n):
        start_time = max(current_time, sorted_proc[i]["arrival"])
        completion[i] = start_time + sorted_proc[i]["burst"]
        current_time = completion[i]
    return finalize_results("FCFS", sorted_proc, completion)

def sjf(process_list):
    sorted_proc = sorted(process_list, key=lambda x: (x["arrival"], x["burst"]))
    n = len(sorted_proc)
    completed = [False] * n
    completion = [0] * n
    current_time = 0
    done = 0
    while done < n:
        available = [i for i in range(n) if not completed[i] and sorted_proc[i]["arrival"] <= current_time]
        if not available:
            current_time = min(p["arrival"] for i, p in enumerate(sorted_proc) if not completed[i])
            continue
        selected = min(available, key=lambda x: (sorted_proc[x]["burst"], sorted_proc[x]["arrival"]))
        current_time += sorted_proc[selected]["burst"]
        completion[selected] = current_time
        completed[selected] = True
        done += 1
    return finalize_results("SJF", sorted_proc, completion)

def priority_scheduling(process_list):
    sorted_proc = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_proc)
    completed = [False] * n
    completion = [0] * n
    current_time = 0
    done = 0
    while done < n:
        available = [i for i in range(n) if not completed[i] and sorted_proc[i]["arrival"] <= current_time]
        if not available:
            current_time = min(p["arrival"] for i, p in enumerate(sorted_proc) if not completed[i])
            continue
        selected = min(available, key=lambda x: (sorted_proc[x]["priority"], sorted_proc[x]["arrival"]))
        current_time += sorted_proc[selected]["burst"]
        completion[selected] = current_time
        completed[selected] = True
        done += 1
    return finalize_results("Priority", sorted_proc, completion)

def round_robin(process_list, time_quantum):
    processes = sorted(process_list, key=lambda x: x["arrival"])
    n = len(processes)
    remaining_burst = [p["burst"] for p in processes]
    completion = [0] * n
    current_time = 0
    completed = 0
    ready_queue = deque()
    visited = [False] * n
    
    # Initial load
    def add_to_queue():
        for i in range(n):
            if processes[i]["arrival"] <= current_time and not visited[i]:
                ready_queue.append(i)
                visited[i] = True
    
    add_to_queue()
    if not ready_queue:
        current_time = processes[0]["arrival"]
        add_to_queue()

    while completed < n:
        idx = ready_queue.popleft()
        execute_time = min(time_quantum, remaining_burst[idx])
        remaining_burst[idx] -= execute_time
        current_time += execute_time
        
        add_to_queue()
        
        if remaining_burst[idx] > 0:
            ready_queue.append(idx)
        else:
            completion[idx] = current_time
            completed += 1
            
        if not ready_queue and completed < n:
            current_time = min(p["arrival"] for i, p in enumerate(processes) if not visited[i])
            add_to_queue()
            
    return finalize_results("Round Robin", processes, completion)

# Test execution
if __name__ == "__main__":
    test_data = [
        {"id": "P1", "arrival": 0, "burst": 7, "priority": 2},
        {"id": "P2", "arrival": 1, "burst": 4, "priority": 1},
        {"id": "P3", "arrival": 2, "burst": 1, "priority": 3},
        {"id": "P4", "arrival": 3, "burst": 3, "priority": 2}
    ]
    print(fcfs(test_data))
    print(sjf(test_data))
    print(priority_scheduling(test_data))
    print(round_robin(test_data, 2))
