import multiprocessing
import os
import resource

import psutil


def get_optimal_workers():
    """
    Menghitung jumlah worker optimal berdasarkan CPU, RAM, dan karakteristik aplikasi
    """
    cpu_count = multiprocessing.cpu_count()
    workers_by_cpu = (2 * cpu_count) + 1

    available_ram = psutil.virtual_memory().available / (1024 * 1024)
    reserved_ram = 512
    ram_per_worker = 100

    max_workers_by_ram = int((available_ram - reserved_ram) / ram_per_worker)

    optimal_workers = min(workers_by_cpu, max_workers_by_ram)
    optimal_workers = max(2, optimal_workers)
    optimal_workers = min(12, optimal_workers)

    return optimal_workers


async def optimize_system():
    """
    Lakukan optimasi sistem untuk performa maksimal.
    - Set RLIMIT_NOFILE (max open files) ke target yang aman (default 65536, tidak melebihi hard limit).
    - Set environment variable untuk optimasi TCP jika diperlukan.
    """
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        target = 65536
        new_soft = min(target, hard)
        if soft < new_soft:
            resource.setrlimit(resource.RLIMIT_NOFILE, (new_soft, hard))
    except Exception:
        pass

    os.environ["TCP_NODELAY"] = "1"
    os.environ["TCP_QUICKACK"] = "1"
