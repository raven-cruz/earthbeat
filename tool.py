import subprocess
from utils.lighting import calculate_lighting

BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"

def main():
    calculate_lighting()

    # run scene render
    subprocess.run([BLENDER_PATH, "--background", "--python", "utils/render.py"], check=True)

if __name__ == "__main__":
    main()