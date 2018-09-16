import multiprocessing


bind = "0.0.0.0:5000"
chdir = "/srv"
workers = multiprocessing.cpu_count() * 2 + 1
