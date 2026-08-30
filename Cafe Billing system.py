from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import random

# ---------------- Window ----------------

root = Tk()
root.title("VIRASAT-E-KHALSA CAFETERIA - Billing System")
root.geometry("700x500")
root.configure(bg="#FFF8DC")
root.state("zoomed")
root.resizable(False, False)

# ---------------- Variables ----------------

menu = {
    "Pasta":250,
    "Pizza":199,
    "Coffee":70,
    "Maggi":80,
    "Veg Puff":120,
    "Burger":150,
    "Sandwich":110,
    "Cold Drink":60
}
total = 0
items = []

bill_no = random.randint(1001,9999)

# ---------------- Header ----------------

Label(root,
      text="☕ VIRASAT-E-KHALSA CAFETERIA ☕",
      font=("Arial",20,"bold"),
      bg="#8B4513",
      fg="white",
      pady=8).pack(fill=X)

Label(root,
      text="FAST FOOD & BEVERAGES",
      font=("Arial",12,"bold"),
      bg="#FFF8DC",
      fg="brown").pack()

# ---------------- Date Time ----------------

now = datetime.now()

date = now.strftime("%d-%m-%Y")
time = now.strftime("%I:%M:%S %p")
info = Frame(root,bg="#FFF8DC")
info.pack(pady=8)

Label(info,
      text=f"Bill No : {bill_no}",
      font=("Arial",11,"bold"),
      bg="#FFF8DC").grid(row=0,column=0,padx=20)

Label(info,
      text=f"Date : {date}",
      font=("Arial",11,"bold"),
      bg="#FFF8DC").grid(row=0,column=1,padx=20)

Label(info,
      text=f"Time : {time}",
      font=("Arial",11,"bold"),
      bg="#FFF8DC").grid(row=0,column=2,padx=20)

# ---------------- Customer Details ----------------

customer = LabelFrame(root,
                      text="Customer Details",
                      font=("Arial",12,"bold"),
                      bg="#FFF8DC",
                      padx=20,
                      pady=8)

customer.pack(fill=X,padx=20)

Label(customer,
      text="Customer Name",
      bg="#FFF8DC",
      font=("Arial",11)).grid(row=0,column=0)

name_entry = Entry(customer,font=("Arial",11),width=25)
name_entry.grid(row=0,column=1,padx=10)

Label(customer,
      text="Mobile Number",
      bg="#FFF8DC",
      font=("Arial",11)).grid(row=0,column=2)

mobile_entry = Entry(customer,font=("Arial",11),width=20)
mobile_entry.grid(row=0,column=3,padx=10)

Label(customer,
      text="Payment",
      bg="#FFF8DC",
      font=("Arial",11)).grid(row=1,column=0,pady=8)

payment = ttk.Combobox(customer,
                       values=["Cash","UPI","Card"],
                       state="readonly",
                       width=22)

payment.grid(row=1,column=1)
payment.current(0)
# ---------------- Menu Section ----------------

menu_frame = LabelFrame(root,
                        text="Order Details",
                        font=("Arial",12,"bold"),
                        bg="#FFF8DC",
                        padx=20,
                        pady=8)

menu_frame.pack(fill=X,padx=20,pady=5)

Label(menu_frame,
      text="Select Item",
      font=("Arial",11),
      bg="#FFF8DC").grid(row=0,column=0)

combo = ttk.Combobox(menu_frame,
                     values=list(menu.keys()),
                     state="readonly",
                     width=22)

combo.grid(row=0,column=1,padx=10)
combo.current(0)

Label(menu_frame,
      text="Quantity",
      font=("Arial",11),
      bg="#FFF8DC").grid(row=0,column=2)

qty = Spinbox(menu_frame,
              from_=1,
              to=20,
              width=5,
              font=("Arial",11))

qty.grid(row=0,column=3,padx=10)

# ---------------- Item List ----------------

listbox = Listbox(root,
                  width=70,
                  height=8,
                  font=("Consolas",11))

listbox.pack(padx=20,pady=5)

# ---------------- Total ----------------

total_label = Label(root,
                    text="Current Total : ₹0",
                    font=("Arial",15,"bold"),
                    bg="#FFF8DC",
                    fg="darkgreen")

total_label.pack(pady=5)

# ---------------- Add Item ----------------

def add_item():

    global total

    item = combo.get()
    quantity = int(qty.get())

    price = menu[item] * quantity

    total += price

    items.append((item, quantity, price))

    listbox.insert(
        END,
        f"{item:<15} Qty:{quantity:<2} ₹{price}"
    )

    total_label.config(
        text=f"Current Total : ₹{total}"
    )

# ---------------- Remove Last Item ----------------

def remove_item():

    global total

    if len(items) == 0:
        return

    item = items.pop()

    total -= item[2]

    listbox.delete(END)

    total_label.config(
        text=f"Current Total : ₹{total}"
    )
    # ---------------- Bill Functions ----------------

def generate_bill():

    if total == 0:
        messagebox.showwarning("Warning","Please Add Item")
        return

    gst = total * 0.18
    grand_total = total + gst

    receipt.delete("1.0", END)

    receipt.insert(END, "=====================================\n")
    receipt.insert(END, "           VIRASAT-E-KHALSA CAFETERIA\n")
    receipt.insert(END, "=====================================\n\n")

    receipt.insert(END, f"Bill No : {bill_no}\n")
    receipt.insert(END, f"Date : {date}\n")
    receipt.insert(END, f"Time : {time}\n\n")

    receipt.insert(END, f"Customer : {name_entry.get()}\n")
    receipt.insert(END, f"Mobile : {mobile_entry.get()}\n")
    receipt.insert(END, f"Payment : {payment.get()}\n")

    receipt.insert(END, "\n-------------------------------------\n")
    receipt.insert(END, "Item\tQty\tPrice\n")
    receipt.insert(END, "-------------------------------------\n")

    for item, qty, price in items:
        receipt.insert(END, f"{item}\t{qty}\t₹{price}\n")

    receipt.insert(END, "\n-------------------------------------\n")
    receipt.insert(END, f"Subtotal : ₹{total}\n")
    receipt.insert(END, f"GST (18%) : ₹{gst:.2f}\n")
    receipt.insert(END, f"Grand Total : ₹{grand_total:.2f}\n")
    receipt.insert(END, "-------------------------------------\n")
    receipt.insert(END, "\nThank You!\nVisit Again ☕")


def clear_bill():

    global total, items

    total = 0
    items = []

    listbox.delete(0, END)

    total_label.config(text="Current Total : ₹0")

    receipt.delete("1.0", END)

    name_entry.delete(0, END)
    mobile_entry.delete(0, END)

# ---------------- Receipt ----------------

receipt_frame = LabelFrame(root,
                           text="Bill Receipt",
                           font=("Arial",12,"bold"),
                           bg="#FFF8DC")

receipt_frame.pack(fill=BOTH,
                   padx=20,
                   pady=10)

receipt = Text(receipt_frame,
               width=70,
               height=8,
               font=("Consolas",10))

receipt.pack()
# ---------------- Buttons ----------------

button_frame = Frame(root, bg="#FFF8DC")
button_frame.pack(pady=8)

Button(button_frame,
       text="Add Item",
       font=("Arial",11,"bold"),
       bg="green",
       fg="white",
       width=10,
       command=add_item).grid(row=0,column=0,padx=5)

Button(button_frame,
       text="Remove Item",
       font=("Arial",11,"bold"),
       bg="orange",
       fg="white",
       width=10,
       command=remove_item).grid(row=0,column=1,padx=5)

Button(button_frame,
       text="Generate Bill",
       font=("Arial",11,"bold"),
       bg="blue",
       fg="white",
       width=10,
       command=generate_bill).grid(row=0,column=2,padx=5)

Button(button_frame,
       text="Clear",
       font=("Arial",11,"bold"),
       bg="purple",
       fg="white",
       width=10,
       command=clear_bill).grid(row=0,column=3,padx=5)

Button(button_frame,
       text="Exit",
       font=("Arial",11,"bold"),
       bg="red",
       fg="white",
       width=10,
       command=root.destroy).grid(row=0,column=4,padx=5)

# ---------------- Footer ----------------

Label(root,
      text="© 2026 VIRASAT-E-KHALSA CAFETERIA | Food Billing System",
      font=("Arial",10,"bold"),
      bg="#FFF8DC",
      fg="brown").pack(side=BOTTOM, pady=5)

root.mainloop()
