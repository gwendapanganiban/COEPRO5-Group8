from collections import deque

def finalize_results(algo_name, processes, completion, timeline):
    """Calculates metrics, formats the output dictionary, and includes the execution timeline."""
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
        "avg_waiting": round(total_wt / n, 2),
        "timeline": timeline  # Essential for the Data Visualization Engineer
    }

def fcfs(process_list):
    sorted_proc = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_proc)
    completion = [0] * n
    timeline = []
    current_time = 0
    
    for i in range(n):
        if current_time < sorted_proc[i]["arrival"]:
            current_time = sorted_proc[i]["arrival"]
        
        start_time = current_time
        current_time += sorted_proc[i]["burst"]
        completion[i] = current_time
        
        timeline.append({"id": sorted_proc[i]["id"], "start": start_time, "end": current_time})
        
    return finalize_results("FCFS", sorted_proc, completion, timeline)

def sjf_preemptive(process_list):
    """Shortest Remaining Time First (SRTF) - Preemptive SJF"""
    sorted_proc = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_proc)
    remaining_burst = [p["burst"] for p in sorted_proc]
    completion = [0] * n
    timeline = []
    
    current_time = 0
    completed = 0
    last_proc_id = None
    segment_start = 0
    
    while completed < n:
        available = [i for i in range(n) if sorted_proc[i]["arrival"] <= current_time and remaining_burst[i] > 0]
        
        if not available:
            if last_proc_id is not None:
                timeline.append({"id": last_proc_id, "start": segment_start, "end": current_time})
                last_proc_id = None
            current_time = min(sorted_proc[i]["arrival"] for i in range(n) if remaining_burst[i] > 0)
            continue
            
        selected = min(available, key=lambda x: (remaining_burst[x], sorted_proc[x]["arrival"]))
        
        if sorted_proc[selected]["id"] != last_proc_id:
            if last_proc_id is not None:
                timeline.append({"id": last_proc_id, "start": segment_start, "end": current_time})
            last_proc_id = sorted_proc[selected]["id"]
            segment_start = current_time
            
        remaining_burst[selected] -= 1
        current_time += 1
        
        if remaining_burst[selected] == 0:
            completion[selected] = current_time
            completed += 1
            
    if last_proc_id is not None:
        timeline.append({"id": last_proc_id, "start": segment_start, "end": current_time})
        
    return finalize_results("SJF (Preemptive)", sorted_proc, completion, timeline)

def priority_preemptive(process_list):
    """Preemptive Priority Scheduling"""
    sorted_proc = sorted(process_list, key=lambda x: x["arrival"])
    n = len(sorted_proc)
    remaining_burst = [p["burst"] for p in sorted_proc]
    completion = [0] * n
    timeline = []
    
    current_time = 0
    completed = 0
    last_proc_id = None
    segment_start = 0
    
    while completed < n:
        available = [i for i in range(n) if sorted_proc[i]["arrival"] <= current_time and remaining_burst[i] > 0]
        
        if not available:
            if last_proc_id is not None:
                timeline.append({"id": last_proc_id, "start": segment_start, "end": current_time})
                last_proc_id = None
            current_time = min(sorted_proc[i]["arrival"] for i in range(n) if remaining_burst[i] > 0)
            continue
            
        # Assuming lower number = higher priority. Swap key order if higher number = higher priority.
        selected = min(available, key=lambda x: (sorted_proc[x]["priority"], sorted_proc[x]["arrival"]))
        
        if sorted_proc[selected]["id"] != last_proc_id:
            if last_proc_id is not None:
                timeline.append({"id": last_proc_id, "start": segment_start, "end": current_time})
            last_proc_id = sorted_proc[selected]["id"]
            segment_start = current_time
            
        remaining_burst[selected] -= 1
        current_time += 1
        
        if remaining_burst[selected] == 0:
            completion[selected] = current_time
            completed += 1
            
    if last_proc_id is not None:
        timeline.append({"id": last_proc_id, "start": segment_start, "end": current_time})
        
    return finalize_results("Priority (Preemptive)", sorted_proc, completion, timeline)

def round_robin(process_list, time_quantum):
    processes = sorted(process_list, key=lambda x: x["arrival"])
    n = len(processes)
    remaining_burst = [p["burst"] for p in processes]
    completion = [0] * n
    timeline = []
    
    current_time = 0
    completed = 0
    ready_queue = deque()
    visited = [False] * n
    
    def add_to_queue():
        for i in range(n):
            if processes[i]["arrival"] <= current_time and not visited[i]:
                ready_queue.append(i)
                visited[i] = True
                
    add_to_queue()
    if not ready_queue and completed < n:
        current_time = processes[0]["arrival"]
        add_to_queue()

    while completed < n:
        idx = ready_queue.popleft()
        execute_time = min(time_quantum, remaining_burst[idx])
        
        start_time = current_time
        remaining_burst[idx] -= execute_time
        current_time += execute_time
        
        timeline.append({"id": processes[idx]["id"], "start": start_time, "end": current_time})
        
        # Check for newly arrived processes while current one was executing
        add_to_queue()
        
        if remaining_burst[idx] > 0:
            ready_queue.append(idx)
        else:
            completion[idx] = current_time
            completed += 1
            
        if not ready_queue and completed < n:
            current_time = min(p["arrival"] for i, p in enumerate(processes) if not visited[i])
            add_to_queue()
            
    return finalize_results("Round Robin", processes, completion, timeline)


class SmartAdvisor:
    """Analyzes process parameters to recommend the most optimal scheduling algorithm."""
    
    @staticmethod
    def analyze(process_list):
        if not process_list:
            return "No processes provided to analyze."
            
        burst_times = [p["burst"] for p in process_list]
        priorities = [p.get("priority", 0) for p in process_list]
        arrival_times = [p["arrival"] for p in process_list]
        
        total_burst = sum(burst_times)
        avg_burst = total_burst / len(process_list)
        
        # Calculate a basic variance indicator for burst times
        variance = sum((x - avg_burst) ** 2 for x in burst_times) / len(process_list)
        has_distinct_priorities = len(set(priorities)) > 1
        all_arrive_together = len(set(arrival_times)) == 1

        reasoning = []
        recommendation = ""

        # Smart analysis logic
        if has_distinct_priorities:
            recommendation = "Priority (Preemptive)"
            reasoning.append("The process batch contains explicit, distinct priority structures that must be enforced by the OS.")
        elif variance > 15 and not all_arrive_together:
            recommendation = "SJF (Preemptive)"
            reasoning.append("There is high variance in job lengths. Running short jobs first minimizes overall average waiting time.")
        elif all_arrive_together and variance < 3:
            recommendation = "FCFS"
            reasoning.append("Processes arrive simultaneously and feature uniform burst times. Simple First-Come, First-Served minimizes overhead.")
        else:
            recommendation = "Round Robin"
            reasoning.append("Standard mixed workload observed. Round Robin guarantees fairness and prevents process starvation via time slicing.")
            
        return {
            "recommended_algorithm": recommendation,
            "analysis": " ".join(reasoning)
        }


# Group Demonstration Block
if __name__ == "__main__":
    test_data = [
        {"id": "P1", "arrival": 0, "burst": 7, "priority": 2},
        {"id": "P2", "arrival": 1, "burst": 4, "priority": 1},
        {"id": "P3", "arrival": 2, "burst": 1, "priority": 3},
        {"id": "P4", "arrival": 3, "burst": 3, "priority": 2}
    ]
    
    print("--- INDIVIDUAL ALGORITHM OUTPUTS (With Timelines) ---")
    print(fcfs(test_data))
    print("\n", sjf_preemptive(test_data))
    print("\n", priority_preemptive(test_data))
    print("\n", round_robin(test_data, 2))
    
    print("\n--- SMART ALGORITHM ADVISOR SUMMARY ---")
    advice = SmartAdvisor.analyze(test_data)
    print(f"Recommended System Config: {advice['recommended_algorithm']}")
    print(f"Reasoning: {advice['analysis']}")
