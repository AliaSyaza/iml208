import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk

class RoomBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Room Booking System")

        self.users = []

        # Open and resize the background image
        bg_image_path = r"C:\Users\Nur Alia syaza\Desktop\ASSINGMENT SEM 3\python 208\discussionroom\blankroom4.jpg"
        bg_img_pil = Image.open(bg_image_path)
        bg_img_pil = bg_img_pil.resize((1920, 1080), Image.BICUBIC)

        # Convert the background image to a PhotoImage
        self.bg_img = ImageTk.PhotoImage(bg_img_pil)

        # Create a label to display the background image
        bg_label = tk.Label(root, image=self.bg_img)
        bg_label.place(relwidth=1, relheight=1)

        # Registration Frame
        self.registration_frame = ttk.Frame(root)
        self.registration_frame.grid(row=0, column=0, padx=10, pady=10)
        self.register_widgets()

        # Booking Frame
        self.booking_frame = ttk.Frame(root)
        self.booking_frame.grid(row=0, column=1, padx=10, pady=10)
        self.booking_widgets()

        # View, Update, Delete Frame
        self.view_frame = ttk.Frame(root)
        self.view_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.view_widgets()


    def register_widgets(self):
        ttk.Label(self.registration_frame, text="Registration").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.registration_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.registration_frame)
        self.name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.registration_frame, text="User Role:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_role_var = tk.StringVar()
        user_role_combobox = ttk.Combobox(self.registration_frame, textvariable=self.user_role_var, values=["Student", "Staff"])
        user_role_combobox.grid(row=2, column=1, pady=5)

        ttk.Label(self.registration_frame, text="Student/Staff ID:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(self.registration_frame)
        self.id_entry.grid(row=3, column=1, pady=5)

        ttk.Button(self.registration_frame, text="Register", command=self.register_user).grid(row=4, column=0, columnspan=2, pady=10)

    def booking_widgets(self):
        ttk.Label(self.booking_frame, text="Room Booking").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.booking_frame, text="Room Choice:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.room_choice_var = tk.StringVar()
        room_choice_combobox = ttk.Combobox(self.booking_frame, textvariable=self.room_choice_var, values=["Room A", "Room B", "Room C"])
        room_choice_combobox.grid(row=1, column=1, pady=5)

        ttk.Label(self.booking_frame, text="Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = DateEntry(self.booking_frame, width=12, background="darkblue", foreground="white", borderwidth=2)
        self.date_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.booking_frame, text="Time:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.time_var = tk.StringVar()
        time_combobox = ttk.Combobox(self.booking_frame, textvariable=self.time_var, values=["9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM"])
        time_combobox.grid(row=3, column=1, pady=5)

        ttk.Button(self.booking_frame, text="Book Room", command=self.book_room).grid(row=4, column=0, columnspan=2, pady=10)

    def view_widgets(self):
        ttk.Label(self.view_frame, text="View, Update, Delete").grid(row=0, column=0, columnspan=3, pady=10)

        self.tree = ttk.Treeview(self.view_frame, columns=("Name", "User Role", "ID", "Room Choice", "Date", "Time"))
        self.tree.grid(row=1, column=0, columnspan=3)
        self.tree.heading("#0", text="Number")
        self.tree.heading("Name", text="Name")
        self.tree.heading("User Role", text="User Role")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Room Choice", text="Room Choice")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")

        # Hide the numbers column
        self.tree.column("#0", width=0, stretch=tk.NO)

        ttk.Button(self.view_frame, text="Refresh", command=self.refresh_data).grid(row=2, column=0, pady=10)
        ttk.Button(self.view_frame, text="Delete Selected", command=self.delete_selected).grid(row=2, column=1, pady=10)
        ttk.Button(self.view_frame, text="Update Selected", command=self.update_selected).grid(row=2, column=2, pady=10)

    def register_user(self):
        name = self.name_entry.get()
        user_role = self.user_role_var.get()
        user_id = self.id_entry.get()

        if name and user_role and user_id:
            if (user_role == "Student" and len(user_id) == 10) or (user_role == "Staff" and len(user_id) == 11):
                user_data = {"Name": name, "User Role": user_role, "ID": user_id}
                self.users.append(user_data)
                self.clear_registration_fields()
                self.refresh_data()
            else:
                # Display an error message or handle the incorrect ID length based on your requirements
                messagebox.showerror("Error", "Invalid ID length for the selected user role.")


    def book_room(self):
        room_choice = self.room_choice_var.get()
        date = self.date_entry.get()
        time = self.time_var.get()

        if room_choice and date and time:
            booking_data = {"Room Choice": room_choice, "Date": date, "Time": time}
            user_data = self.users[-1] 
            user_data.update(booking_data)
            self.refresh_data()

            # Display success messagebox
            messagebox.showinfo("Success", "Room booking successful!")

    def refresh_data(self):
        self.tree.delete(*self.tree.get_children())
        for i, user_data in enumerate(self.users):
            self.tree.insert("", i, values=(user_data["Name"], user_data["User Role"], user_data["ID"], user_data.get("Room Choice", ""), user_data.get("Date", ""), user_data.get("Time", "")))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[2] 
            for i, user_data in enumerate(self.users):
                if user_data.get("ID") == item_id:
                    del self.users[i]
                    break
            self.refresh_data()

            # Display success messagebox
            messagebox.showinfo("Success", "Data deleted successfully!")

    def update_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = int(selected_item[0])
            # Add code to update the selected item based on your requirements

    def clear_registration_fields(self):
        self.name_entry.delete(0, tk.END)
        self.user_role_var.set("")
        self.id_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomBookingSystem(root)
    root.mainloop()
