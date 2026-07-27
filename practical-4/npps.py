print("S105 - Aditya Rana")


priority_processes = [
    [1, 0, 5, 2],
    [2, 1, 3, 1],
    [3, 2, 8, 4],
    [4, 3, 6, 3]
]


def print_cli_gantt(gantt_data):
    chart_line = "|"
    time_line = f"{gantt_data[0][1]}"

    for label, _, et in gantt_data:
        cell = f" {label} "
        chart_line += f"{cell}|"
        time_line += f"{et:>{len(cell)+1}}"

    print("\nCLI GANTT CHART:")
    print(chart_line)
    print(time_line)


def run_non_preemptive_priority():
    print("=" * 70)
    print("     EXECUTION STEPS: NON-PREEMPTIVE PRIORITY SCHEDULING")
    print("=" * 70)

    current_time = 0
    completed = 0
    n = len(priority_processes)

    processes = priority_processes.copy()

    results = []
    gantt = []
    visited = [False] * n

    while completed < n:

        ready = []

        for i in range(n):
            if not visited[i] and processes[i][1] <= current_time:
                ready.append(processes[i])

        if len(ready) == 0:
            print(f"Time {current_time}: CPU is IDLE")
            current_time += 1
            continue

        # Select highest priority (lowest number)
        ready.sort(key=lambda x: (x[3], x[1]))

        pid, at, bt, pr = ready[0]

        index = processes.index(ready[0])
        visited[index] = True

        st = current_time
        ct = st + bt
        tat = ct - at
        wt = tat - bt

        print(f"Time {st} to {ct}: Process P{pid} is EXECUTING "
              f"(Burst: {bt}ms, Priority: {pr})")
        print(f"  --> P{pid} Completed at {ct}ms | TAT: {tat}ms | WT: {wt}ms")

        current_time = ct
        completed += 1

        results.append([pid, at, bt, pr, ct, tat, wt])
        gantt.append((f"P{pid}", st, ct))

    print("\nNON-PREEMPTIVE PRIORITY SUMMARY TABLE:")
    print("Process | Arrival | Burst | Priority | Complete | Turnaround | Waiting")
    print("-" * 70)

    total_tat = 0
    total_wt = 0

    for r in results:
        print(f"  P{r[0]}    |    {r[1]}    |   {r[2]}   |    {r[3]}     |"
              f"    {r[4]:<5} |     {r[5]:<5}  |   {r[6]}")
        total_tat += r[5]
        total_wt += r[6]

    print("-" * 70)
    print(f"Average Waiting Time    = {total_wt / n:.2f} ms")
    print(f"Average Turnaround Time = {total_tat / n:.2f} ms")

    print_cli_gantt(gantt)
    print()


run_non_preemptive_priority()
