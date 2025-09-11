import tkinter as tk
import speedtest
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to perform the speed test
def speedcheck():
    try:
        st = speedtest.Speedtest()  # Speedtest object
        st.get_best_server()  # Automatically select the best server

        # Get download and upload speeds in Mbps
        down = round(st.download() / (10**6), 3)  # Download speed in Mbps
        up = round(st.upload() / (10**6), 3)  # Upload speed in Mbps

        # Update labels with speed values
        lab_down.config(text=f"{down} Mbps")
        lab_up.config(text=f"{up} Mbps")

        # Add speeds to lists
        download_speeds.append(down)
        upload_speeds.append(up)

        # Update trends
        if len(download_speeds) > 1:
            download_trends.append("Increasing" if down > download_speeds[-2] else "Decreasing")
        else:
            download_trends.append("N/A")

        if len(upload_speeds) > 1:
            upload_trends.append("Increasing" if up > upload_speeds[-2] else "Decreasing")
        else:
            upload_trends.append("N/A")

        # Update graph
        update_graph()

    except Exception as e:
        lab_down.config(text="Error")
        lab_up.config(text="Error")
        print("Error in Speed Test:", e)

# Function to update the graph
def update_graph():
    ax.clear()
    
    # Plot download and upload speeds
    ax.plot(download_speeds, label='Download Speed (Mbps)', color='blue', marker='o')
    ax.plot(upload_speeds, label='Upload Speed (Mbps)', color='red', marker='o')

    # Annotate trends
    for i in range(1, len(download_speeds)):
        color = "green" if download_trends[i] == "Increasing" else "orange"
        ax.scatter(i, download_speeds[i], color=color)

    for i in range(1, len(upload_speeds)):
        color = "purple" if upload_trends[i] == "Increasing" else "yellow"
        ax.scatter(i, upload_speeds[i], color=color)

    ax.set_title('Internet Speed Over Time')
    ax.set_xlabel('Test Runs')
    ax.set_ylabel('Speed (Mbps)')
    ax.legend()

    canvas.draw()  # Redraw the graph

# Create the Tkinter window
sp = tk.Tk()
sp.title("Internet Speed Test")
sp.geometry("500x750")
sp.config(bg="blue")

# Title label
tk.Label(sp, text="Internet Speed Test", font=("Times New Roman", 30, "bold"), bg="blue", fg="white").place(x=60, y=40, height=50, width=380)

# Download speed label
tk.Label(sp, text="Download Speed Test", font=("Times New Roman", 20, "bold"), bg="blue", fg="white").place(x=60, y=130, height=50, width=380)
lab_down = tk.Label(sp, text="00 Mbps", font=("Times New Roman", 30, "bold"), bg="blue", fg="white")
lab_down.place(x=60, y=190, height=50, width=380)

# Upload speed label
tk.Label(sp, text="Upload Speed Test", font=("Times New Roman", 20, "bold"), bg="blue", fg="white").place(x=60, y=260, height=50, width=380)
lab_up = tk.Label(sp, text="00 Mbps", font=("Times New Roman", 30, "bold"), bg="blue", fg="white")
lab_up.place(x=60, y=320, height=50, width=380)

# Button to check speed
btn = tk.Button(sp, text="CHECK SPEED", font=("Times New Roman", 25, "bold"), relief="raised", bg="red", command=speedcheck)
btn.place(x=60, y=390, height=50, width=380)

# Setup Matplotlib figure for graph
fig, ax = plt.subplots(figsize=(5, 4))
download_speeds = []
upload_speeds = []
download_trends = []
upload_trends = []

# Canvas for displaying graph
canvas = FigureCanvasTkAgg(fig, master=sp)
canvas.get_tk_widget().place(x=60, y=470)

# Start the Tkinter event loop
sp.mainloop()
