import os
import sys
import threading

PIPE_IN = '/mcp-pipes/stdin'
PIPE_OUT = '/mcp-pipes/stdout'

def ensure_fifo(path, mode=0o666):
    try:
        os.mkfifo(path, mode)
    except FileExistsError:
        pass

def stdin_to_pipe(pipe_path):
    with open(pipe_path, 'w') as w:
        for line in sys.stdin:
            w.write(line)
            w.flush()

def pipe_to_stdout(pipe_path):
    with open(pipe_path, 'r') as r:
        for line in iter(r.readline, ''):
            sys.stdout.write(line)
            sys.stdout.flush()

def main():
    ensure_fifo(PIPE_IN)
    ensure_fifo(PIPE_OUT)

    t1 = threading.Thread(target=stdin_to_pipe, args=(PIPE_IN,), daemon=True)
    t2 = threading.Thread(target=pipe_to_stdout, args=(PIPE_OUT,), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    main()
