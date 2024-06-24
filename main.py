import psutil # type: ignore
import socket
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

def get_remote_address(pid):
    try:
        connections = psutil.Process(pid).connections()
        remote_addresses = [(c.raddr.ip, c.raddr.port) for c in connections if c.status == 'ESTABLISHED']
        if remote_addresses:
            return max(remote_addresses, key=lambda x: x[1])
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return None

def copy_remote_address():
    selected_item = process_tree.selection()
    if selected_item:
        item_values = process_tree.item(selected_item)['values']
        if item_values:
            remote_address = item_values[-1]
            window.clipboard_clear()
            window.clipboard_append(remote_address)
            messagebox.showinfo("Copy", f"Remote Address: {remote_address} has been copied to clipboard.")
        else:
            messagebox.showwarning("No Selection", "Please select a process with a remote address.")
    else:
        messagebox.showwarning("No Selection", "Please select a process with a remote address.")

def update_process_list():
    process_tree.delete(*process_tree.get_children())

    processes = psutil.process_iter(['pid', 'name'])

    for process in processes:
        pid = process.info['pid']
        name = process.info['name']
        remote_address = get_remote_address(pid)

        if remote_address and remote_address[1] == 443:  # Filter based on port 443
            ip, port = remote_address
            process_tree.insert('', 'end', values=(pid, name, f"{ip}:{port}"))

    process_tree.after(1000, update_process_list)

window = tk.Tk()
window.title("Shqrawi's Network Monitor")

process_tree = ttk.Treeview(window, columns=("pid", "name", "remote_address"), show="headings")
process_tree.heading("pid", text="PID")
process_tree.heading("name", text="Name")
process_tree.heading("remote_address", text="Address")
process_tree.pack(fill="both", expand=True)

copy_button = ttk.Button(window, text="Copy", command=copy_remote_address)
copy_button.pack(pady=5)

update_process_list()

window.mainloop()