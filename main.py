from datetime import datetime
from subprocess import (
    run, PIPE
)


result = run(["ps", "aux"], stderr=PIPE, stdout=PIPE)

stdout_lines = result.stdout.splitlines()

processes_splitted_lines = []
for line in stdout_lines[1:]:
    splitted_line = line.split()
    processes_splitted_lines.append(splitted_line)


class Process:

    def __init__(self, user, pid, cpu, memory, virt_mem, rss, tt, state, starting_time, cpu_time, command):
        self.user = user.decode('utf-8')
        self.pid = pid
        self.cpu = cpu.decode('utf-8')
        self.memory = memory.decode('utf-8')
        self.virt_mem = virt_mem
        self.rss = rss
        self.tt = tt
        self.state = state
        self.starting_time = starting_time
        self.cpu_time = cpu_time
        self.command = command.decode('utf-8')


processes_list = []
for line in processes_splitted_lines:
    process = Process(line[0],
                      line[1],
                      line[2],
                      line[3],
                      line[4],
                      line[5],
                      line[6],
                      line[7],
                      line[8],
                      line[9],
                      line[10]
                      )
    processes_list.append(process)


def get_all_users():
    all_users = []
    for element in processes_list:
        user = element.user
        all_users.append(user)
    return all_users


def get_unique_users():
    all_users_res = get_all_users()
    unique_users = set(all_users_res)
    return unique_users


def get_system_unique_users():
    unique_users_res = get_unique_users()
    mystring = ', '.join(x for x in unique_users_res)
    return mystring


def count_all_processes():
    processes_number = len(processes_list)
    return processes_number


def count_each_user_processes():
    result = {}
    for element in processes_list:
        decoded_element = element.user
        if decoded_element not in result:
            result[decoded_element] = 1
        else:
            result[decoded_element] = result[decoded_element] + 1
    res_string = ""
    for key, value in result.items():
        res_string += key + ':' + str(value) + '\n'
    return res_string


def count_all_memory_used():
    all_memory = 0
    for element in processes_list:
        decoded_element = element.memory
        all_memory = all_memory + float(decoded_element)
    return str(round(all_memory, 1))


def count_all_cpu_percent():
    all_cpu_used = 0
    for element in processes_list:
        decoded_element = element.cpu
        all_cpu_used = all_cpu_used + float(decoded_element)
    return str(round(all_cpu_used, 1))


def find_process_with_max_cpu_usage():
    max_cpu_element = processes_list[0]
    for element in processes_list[1:]:
        if float(element.cpu) > float(max_cpu_element.cpu):
            max_cpu_element = element
    return max_cpu_element.command[:20]


def find_process_with_max_mem_usage():
    max_mem_element = processes_list[0]
    for element in processes_list[1:]:
        if float(element.memory) > float(max_mem_element.memory):
            max_mem_element = element
    return max_mem_element.command[:20]


text = f"""Отчёт о состоянии системы:
Пользователи системы: {get_system_unique_users()}
Процессов запущено: {count_all_processes()}
Пользовательских процессов:
{count_each_user_processes()}
Всего памяти используется: {count_all_memory_used()} mb
Всего CPU используется: {count_all_cpu_percent()} %
Больше всего памяти использует: {find_process_with_max_mem_usage()}
Больше всего CPU использует: {find_process_with_max_cpu_usage()}
"""

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H:%M")

with open(f'{dt_string}-scan.txt', 'w') as f:
    f.write(text)
