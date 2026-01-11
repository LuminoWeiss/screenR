# importing the required packages
import pyautogui
import cv2
import numpy as np
import time
import argparse
from datetime import datetime
import sys
from pynput import keyboard

class vRecorder:
    def __init__(self, time_limit=3600*2, resolution=(1920, 1080), filename="Recording.avi", fps=30.0) -> None:

        # Specify resolution
        self.resolution = resolution

        # Specify video codec
        self.codec = cv2.VideoWriter_fourcc(*"XVID")

        # Specify name of Output file
        self.filename = filename

        # Specify frames rate. We can choose any
        # value and experiment with it
        self.fps = fps

        # Creating a VideoWriter object
        self.out = cv2.VideoWriter(filename, self.codec, fps, resolution)
        self.time_limit = time_limit
        self.stop_recording = False

        # Create an Empty window
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

        # Resize this window
        cv2.resizeWindow("Live", 480, 270)

        # Setup keyboard listener for ESC key
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
    

    def on_key_press(self, key):
        """Handle keyboard events to stop recording"""
        try:
            if key == keyboard.Key.esc:
                print("\n[ESC pressed] Stopping recording...")
                self.stop_recording = True
                return False  # Stop listener
        except AttributeError:
            pass

    def start_record(self, time_limit):
        """Start recording with time limit and keyboard interrupt support"""
        tCurrent = time.time()
        elapsed_time = 0
        frame_count = 0

        print(f"\n{'='*60}")
        print(f"Recording started!")
        print(f"Duration: {time_limit} seconds ({time_limit/60:.1f} minutes)")
        print(f"Output file: {self.filename}")
        print(f"Resolution: {self.resolution[0]}x{self.resolution[1]} @ {self.fps} FPS")
        print(f"{'='*60}")
        print(f"Press 'q' in the preview window or ESC to stop recording")
        print(f"{'='*60}\n")

        try:
            while time.time() < tCurrent + time_limit and not self.stop_recording:
                # Take screenshot using PyAutoGUI
                img = pyautogui.screenshot()

                # Convert the screenshot to a numpy array
                frame = np.array(img)

                # Convert it from BGR(Blue, Green, Red) to
                # RGB(Red, Green, Blue)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Write it to the output file
                self.out.write(frame)

                # Optional: Display the recording screen
                cv2.imshow('Live', frame)

                # Stop recording when we press 'q'
                if cv2.waitKey(1) == ord('q'):
                    print("\n['q' pressed] Stopping recording...")
                    break

                # Update status every second
                frame_count += 1
                elapsed_time = time.time() - tCurrent
                if frame_count % int(self.fps) == 0:
                    remaining = time_limit - elapsed_time
                    print(f"\rRecording... {elapsed_time:.0f}s / {time_limit}s ({remaining:.0f}s remaining)", end='', flush=True)

        except KeyboardInterrupt:
            print("\n\n[Ctrl+C detected] Stopping recording...")
        except Exception as e:
            print(f"\n\nError during recording: {e}")
        finally:
            # Release the Video writer
            self.out.release()

            # Destroy all windows
            cv2.destroyAllWindows()

            # Stop keyboard listener
            if hasattr(self, 'listener'):
                self.listener.stop()

            # Print summary
            final_elapsed = time.time() - tCurrent
            print(f"\n\n{'='*60}")
            print(f"Recording stopped!")
            print(f"Total duration: {final_elapsed:.1f} seconds ({final_elapsed/60:.1f} minutes)")
            print(f"Total frames: {frame_count}")
            print(f"Output saved to: {self.filename}")
            print(f"{'='*60}\n")

def parse_resolution(res_string):
    """Parse resolution string like '1920x1080' to tuple (1920, 1080)"""
    try:
        width, height = res_string.lower().split('x')
        return (int(width), int(height))
    except:
        raise argparse.ArgumentTypeError(f"Resolution must be in format WIDTHxHEIGHT (e.g., 1920x1080)")

def main():
    """Main function with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description='Screen Recorder - Record your screen with ease',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python s_recorder.py -d 60 -f my_recording.avi
  python s_recorder.py --duration 120 --filename demo.avi --fps 60
  python s_recorder.py -d 300 -r 1920x1080 -f presentation.avi

Stopping the recording:
  - Press 'q' while the preview window is focused
  - Press ESC key (works globally)
  - Press Ctrl+C in the terminal
        ''')

    # Add arguments
    parser.add_argument(
        '-d', '--duration',
        type=int,
        default=3600,
        help='Recording duration in seconds (default: 3600 = 1 hour)'
    )

    parser.add_argument(
        '-f', '--filename',
        type=str,
        default=None,
        help='Output filename (default: recording_TIMESTAMP.avi)'
    )

    parser.add_argument(
        '-r', '--resolution',
        type=parse_resolution,
        default='1920x1080',
        help='Screen resolution in WIDTHxHEIGHT format (default: 1920x1080)'
    )

    parser.add_argument(
        '--fps',
        type=float,
        default=30.0,
        help='Frames per second (default: 30.0)'
    )

    args = parser.parse_args()

    # Generate default filename with timestamp if not provided
    if args.filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.filename = f"recording_{timestamp}.avi"

    # Ensure filename has .avi extension
    if not args.filename.endswith('.avi'):
        args.filename += '.avi'

    try:
        # Create recorder instance
        print(f"\nInitializing screen recorder...")
        vr = vRecorder(
            filename=args.filename,
            time_limit=args.duration,
            resolution=args.resolution,
            fps=args.fps
        )

        # Start recording
        vr.start_record(time_limit=args.duration)

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()