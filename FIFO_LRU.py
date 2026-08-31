# Practical 9: Memory Management Techniques
# FIFO and LRU Page Replacement Algorithms


def display_result(reference_string, frames_history, status_history,
                   page_faults, page_hits, algorithm):

    print("\n" + "=" * 70)
    print(algorithm + " Page Replacement")
    print("=" * 70)

    print(f"{'Page':<8}", end="")

    for i in range(len(frames_history[0])):
        print(f"{'F' + str(i + 1):<8}", end="")

    print(f"{'Status':<12}")

    print("-" * 70)

    for i, page in enumerate(reference_string):

        print(f"{page:<8}", end="")

        for frame in frames_history[i]:

            if frame == -1:
                print(f"{'-':<8}", end="")
            else:
                print(f"{frame:<8}", end="")

        print(f"{status_history[i]:<12}")

    total_pages = len(reference_string)

    hit_ratio = page_hits / total_pages
    miss_ratio = page_faults / total_pages

    print("-" * 70)

    print("Total Page References :", total_pages)
    print("Page Hits             :", page_hits)
    print("Page Misses           :", page_faults)
    print("Hit Ratio             :", round(hit_ratio, 2))
    print("Miss Ratio            :", round(miss_ratio, 2))


def fifo_page_replacement(reference_string, frame_count):

    frames = [-1] * frame_count

    frames_history = []
    status_history = []

    page_faults = 0
    page_hits = 0

    pointer = 0

    for page in reference_string:

        if page in frames:

            # Page is already present
            page_hits += 1
            status_history.append("HIT")

        else:

            # Page fault
            page_faults += 1
            status_history.append("MISS")

            # Replace the oldest page
            frames[pointer] = page

            pointer = (pointer + 1) % frame_count

        frames_history.append(frames.copy())

    display_result(
        reference_string,
        frames_history,
        status_history,
        page_faults,
        page_hits,
        "FIFO"
    )


def lru_page_replacement(reference_string, frame_count):

    frames = []

    frames_history = []
    status_history = []

    page_faults = 0
    page_hits = 0

    for page in reference_string:

        if page in frames:

            # Page is already present
            page_hits += 1
            status_history.append("HIT")

            # Move the recently used page to the end
            frames.remove(page)
            frames.append(page)

        else:

            # Page fault
            page_faults += 1
            status_history.append("MISS")

            if len(frames) < frame_count:

                # Empty frame available
                frames.append(page)

            else:

                # Remove least recently used page
                frames.pop(0)

                # Add new page
                frames.append(page)

        current_frames = frames.copy()

        while len(current_frames) < frame_count:
            current_frames.append(-1)

        frames_history.append(current_frames)

    display_result(
        reference_string,
        frames_history,
        status_history,
        page_faults,
        page_hits,
        "LRU"
    )


# Main Program

print("=" * 70)
print("        MEMORY MANAGEMENT - PAGE REPLACEMENT")
print("=" * 70)

reference_string = list(
    map(int, input(
        "Enter page reference string (space separated): "
    ).split())
)

frame_count = int(
    input("Enter number of memory frames: ")
)

if frame_count <= 0:

    print("Number of frames must be greater than 0.")

else:

    print("\nReference String:", reference_string)
    print("Number of Frames:", frame_count)

    fifo_page_replacement(
        reference_string,
        frame_count
    )

    lru_page_replacement(
        reference_string,
        frame_count
    )

    print("\n" + "=" * 70)
    print("Simulation completed successfully.")
    print("=" * 70)
