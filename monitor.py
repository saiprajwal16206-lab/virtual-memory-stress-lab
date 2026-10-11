import psutil

print("======================================")
print("      VIRTUAL MEMORY STRESS LAB")
print("======================================")

# Get physical RAM information
ram = psutil.virtual_memory()

print("\n--- PHYSICAL RAM ---")
print(f"Total RAM     : {ram.total / (1024**3):.2f} GB")
print(f"Used RAM      : {ram.used / (1024**3):.2f} GB")
print(f"Available RAM : {ram.available / (1024**3):.2f} GB")
print(f"RAM Usage     : {ram.percent}%")

# Get virtual memory / swap information
virtual = psutil.swap_memory()

print("\n--- VIRTUAL MEMORY / SWAP ---")
print(f"Total Swap    : {virtual.total / (1024**3):.2f} GB")
print(f"Used Swap     : {virtual.used / (1024**3):.2f} GB")
print(f"Free Swap     : {virtual.free / (1024**3):.2f} GB")
print(f"Swap Usage    : {virtual.percent}%")

print("\n======================================")