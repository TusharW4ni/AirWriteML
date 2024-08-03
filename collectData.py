import tkinter as tk
import pandas as pd
import threading
import websocket
import json
import os

data = []
counter = 50
is_connected = False

def on_message(ws, message):
  global data
  values = json.loads(message)['values']
  data.append(values)

ws = None
def connect():
  global ws, is_connected
  ws = websocket.WebSocketApp("ws://192.168.4.94:8080/sensor/connect?type=android.sensor.linear_acceleration",
                on_open=lambda ws: print("connected"),
                on_message=on_message,
                on_error=lambda ws, error: print("error occurred ", error),
                on_close=lambda ws, close_code, reason: print("connection closed : ", reason))
  wst = threading.Thread(target=ws.run_forever)
  wst.start()
  is_connected = True
  toggle_button.config(text="Disconnect")

def disconnect():
  global ws, data, counter, is_connected
  if ws is not None:
    ws.close()
    df = pd.DataFrame(data, columns=['x', 'y', 'z'])
    df.index.name = 'index'
    file_path = f'/home/tushar/sproj/AirWriteML/data/H/H_sample_{counter}.csv'
    df.to_csv(file_path, index=True)
    counter += 1
    data = []
    is_connected = False
    toggle_button.config(text="Connect")
    os.system(f'code {file_path}')

def toggle_connection():
  if is_connected:
    disconnect()
  else:
    connect()

root = tk.Tk()
root.geometry("300x200")

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

toggle_button = tk.Button(frame, text="Connect", command=toggle_connection)
toggle_button.pack()

root.mainloop()