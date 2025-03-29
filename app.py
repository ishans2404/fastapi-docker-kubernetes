from fastapi import FastAPI
import time
import os
import sys

app = FastAPI()

# Store large data in memory for memory pressure test
memory_buffer = []

@app.get("/")
def read_root():
    return {
        "message": "FastAPI App",
        "endpoints": {
            "/cpu/{n}": "CPU stress test (n = intensity)",
            "/memory/{mb}": "Memory allocation test (mb = megabytes)",
            "/health": "Health check"
        }
    }

@app.get("/cpu/{n}")
def cpu_intensive(n: int):
    """Calculate factorial with intensity control"""
    start = time.time()
    result = 1
    for i in range(1, n+1):
        result *= i
        # Add some sleep to prevent excessive CPU usage
        time.sleep(0.001)
    return {
        "result": str(result)[:100] + "...",
        "time_taken": time.time() - start,
        "input": n
    }

@app.get("/memory/{mb}")
def allocate_memory(mb: int):
    """Allocate specified megabytes of memory"""
    global memory_buffer
    # Allocate approximately 1MB per iteration (1,048,576 bytes)
    bytes_to_allocate = mb * 1024 * 1024
    memory_buffer = bytearray(bytes_to_allocate)
    return {
        "allocated_mb": mb,
        "buffer_size": len(memory_buffer),
        "memory_used": f"{sys.getsizeof(memory_buffer) / (1024*1024):.2f} MB"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "env": os.getenv("APP_ENV", "development")}