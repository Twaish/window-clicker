from pynput import mouse

def on_click(x, y, button, pressed):
  if pressed:
    print(f"Mouse clicked at X={x}, Y={y} with {button}")

def main():
  # Set up the listener for mouse events
  with mouse.Listener(on_click=on_click) as listener:
    listener.join()

if __name__ == "__main__":
  main()