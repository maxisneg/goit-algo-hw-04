import random
import timeit

# --- Реалізації алгоритмів сортування ---

def insertion_sort(arr):
    """Сортування вставками."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    """Сортування злиттям."""
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr

def timsort_sort(arr):
    """Сортування Timsort (вбудоване)."""
    arr_copy = arr[:]
    arr_copy.sort()
    return arr_copy

# --- Генерація наборів даних ---

def generate_random_data(size):
    return [random.randint(0, size * 10) for _ in range(size)]

def generate_sorted_data(size):
    return list(range(size))

def generate_reverse_sorted_data(size):
    return list(range(size, 0, -1))

def generate_nearly_sorted_data(size, swaps_ratio=0.05):
    arr = list(range(size))
    num_swaps = int(size * swaps_ratio)
    if size > 1 : # random.sample requires population of at least 2 for k=2
        for _ in range(num_swaps):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
    elif size == 1 and num_swaps > 0: # Edge case if swaps needed for size 1 (no change)
        pass
    return arr


def generate_data_with_duplicates(size, unique_ratio=0.1):
    num_unique = int(size * unique_ratio)
    if num_unique == 0 and size > 0:
        num_unique = 1
    unique_values = [random.randint(0, size) for _ in range(num_unique)]
    if not unique_values and size > 0:
        unique_values = [random.randint(0, size)]
    return [random.choice(unique_values) for _ in range(size)] if unique_values else []


# --- Функція для тестування ---

def run_sorting_test(sort_function_name, data_list, number_runs=10, repeat_count=3):
    """
    Запускає тестування часу виконання функції сортування.
    sort_function_name: рядок з назвою функції сортування (наприклад, 'insertion_sort').
    data_list: список даних для сортування.
    """
    setup_code = f"""
from __main__ import {sort_function_name}
import random # random might not be needed in setup if data_list is already prepared
data_to_sort = {data_list!r} # Use !r for robust representation of the list
"""
    stmt_code = f"{sort_function_name}(data_to_sort)"

    times = timeit.repeat(stmt=stmt_code, setup=setup_code, number=number_runs, repeat=repeat_count)
    return min(times) / number_runs

# --- Необов'язкове завдання: Об'єднання k відсортованих списків ---

def merge_two_lists(l1, l2):
    """Допоміжна функція для злиття двох відсортованих списків."""
    merged = []
    i, j = 0, 0
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            merged.append(l1[i])
            i += 1
        else:
            merged.append(l2[j])
            j += 1
    merged.extend(l1[i:])
    merged.extend(l2[j:])
    return merged

def merge_k_lists(list_of_lists):
    """
    Об'єднує k відсортованих списків у один відсортований список.
    Використовує підхід "розділяй та володарюй", подібно до сортування злиттям.
    """
    if not list_of_lists:
        return []
    if len(list_of_lists) == 1:
        return list_of_lists[0]

    current_lists = list(list_of_lists)

    while len(current_lists) > 1:
        merged_lists_batch = []
        for i in range(0, len(current_lists), 2):
            list1 = current_lists[i]
            list2 = current_lists[i + 1] if (i + 1) < len(current_lists) else []
            merged_lists_batch.append(merge_two_lists(list1, list2))
        current_lists = merged_lists_batch
    return current_lists[0]


# --- Основний блок для демонстрації та тестування ---
if __name__ == "__main__":
    data_sizes = [100, 1000, 5000]
    algorithms_to_test = {
        "Insertion Sort": "insertion_sort",
        "Merge Sort": "merge_sort",
        "Timsort (Python's sort)": "timsort_sort"
    }

    datasets_generators = {
        "Випадкові дані": generate_random_data,
        "Відсортовані дані": generate_sorted_data,
        "Зворотно відсортовані дані": generate_reverse_sorted_data,
        "Майже відсортовані дані": generate_nearly_sorted_data,
        "Дані з дублікатами": generate_data_with_duplicates
    }

    print("Порівняння ефективності алгоритмів сортування:\n")

    results = {}

    for data_name, generator_func in datasets_generators.items():
        print(f"--- Тип даних: {data_name} ---")
        results[data_name] = {}
        for size in data_sizes:
            print(f"  Розмір масиву: {size}")
            results[data_name][size] = {}
            # Генеруємо дані один раз для кожного розміру та типу
            # Важливо: робимо копію, якщо generator_func може змінювати дані,
            # або якщо дані потрібні в незмінному вигляді для timeit setup
            current_data_for_run = generator_func(size)
            if not current_data_for_run and size > 0:
                print(f"    Пропущено тестування для {data_name} розміром {size} через порожній набір даних.")
                continue

            for algo_display_name, algo_func_name in algorithms_to_test.items():
                # Передаємо копію даних у timeit через setup_code,
                # тому current_data_for_run може бути передана як є
                time_taken = run_sorting_test(algo_func_name, current_data_for_run, number_runs=5, repeat_count=3)
                print(f"    {algo_display_name}: {time_taken:.6f} секунд")
                results[data_name][size][algo_display_name] = f"{time_taken:.6f}"
        print("-" * 30)

    print("\n--- Необов'язкове завдання: Об'єднання k відсортованих списків ---")
    lists_to_merge1 = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged_list_result1 = merge_k_lists(lists_to_merge1)
    print(f"Початкові списки: {lists_to_merge1}")
    print(f"Відсортований об'єднаний список: {merged_list_result1}")

    lists_to_merge2 = [[10, 20], [5, 15, 25], [], [30]]
    merged_list_result2 = merge_k_lists(lists_to_merge2)
    print(f"Початкові списки: {lists_to_merge2}")
    print(f"Відсортований об'єднаний список: {merged_list_result2}")

    lists_to_merge3 = [[1]]
    merged_list_result3 = merge_k_lists(lists_to_merge3)
    print(f"Початкові списки: {lists_to_merge3}")
    print(f"Відсортований об'єднаний список: {merged_list_result3}")

    lists_to_merge4 = []
    merged_list_result4 = merge_k_lists(lists_to_merge4)
    print(f"Початкові списки: {lists_to_merge4}")
    print(f"Відсортований об'єднаний список: {merged_list_result4}")

    # Генерація частини README з результатами
    print("\n--- Дані для README.md (скопіюйте та вставте) ---")
    readme_output = "## Емпіричні результати тестування (час у секундах)\n\n"

    # Визначення ключів заздалегідь
    insertion_sort_key_name = "Insertion Sort"
    merge_sort_key_name = "Merge Sort"
    timsort_key_name = "Timsort (Python's sort)"

    for data_name, sizes_data in results.items():
        readme_output += f"### {data_name}\n"
        readme_output += f"| Розмір масиву | {insertion_sort_key_name:<14} | {merge_sort_key_name:<10} | {timsort_key_name:<23} |\n" # Header
        readme_output += "|------------|---------------|----------|------------------|\n"
        for size_key, algos_perf in sorted(sizes_data.items()):
            if algos_perf:
                row_str = f"| {size_key:<12} | "
                row_str += f"{algos_perf.get(insertion_sort_key_name, 'N/A'):<14} | "
                row_str += f"{algos_perf.get(merge_sort_key_name, 'N/A'):<10} | "
                # ВИПРАВЛЕНО: Використовуємо змінну для ключа
                row_str += f"{algos_perf.get(timsort_key_name, 'N/A'):<23} |" # Видалено \n звідси
                row_str += "\n" # \n додається окремо
                readme_output += row_str
        readme_output += "\n"
    print(readme_output)