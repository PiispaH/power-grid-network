import time

from analyzer import Analyzer


def main():
    start = time.time()
    x = Analyzer("data/power.gml")
    x.run()
    duration = time.time() - start
    x.plot_and_print()
    print(f"duration: {duration:.3g}s")

if __name__ == "__main__":
    main()
