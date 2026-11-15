import subprocess
import sys

BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"

def main():
    # run lighting calculation
    subprocess.run([sys.executable, "lighting.py"], check=True)

    # run scene render
    subprocess.run([BLENDER_PATH, "--background", "--python", "scene.py"], check=True)

if __name__ == "__main__":
    main()