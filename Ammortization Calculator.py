from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("700x500")
root.title("Ammortization Calculator")

frame1 = Frame(height=500, width=370, bg='white')
frame1.pack(side=RIGHT)


def add_commas(value):
    a = str(round(value, 2))
    e = list(a.split(".")[0])
    for i in range(len(e))[::-3][1:]:
        e.insert(i + 1, ",")
    value = "".join(e) + "." + a.split(".")[1]
    return value


def on_enter(_event):
    calculateButton['background'] = '#00bb00'


def on_leave(_event):
    calculateButton['background'] = '#00da00'


def calculate(_event):
    schedule = {0: ('Month', 'Payment', 'Principal', 'Interest', 'Total Interest Paid', 'Balance')}
    flag = True
    flag3 = True
    totalInterest = 0

    def char_check():
        flag1 = True
        try:
            principal = float(principalEntry.get())
            term = float(termEntry.get())
            APR = float(APREntry.get()) / 100
            extraPayment = float(extraPaymentEntry.get())

        except ValueError:
            warning1 = Label(root, text="Do not leave any options blank. Only enter numbers. ", fg='red')
            warning1.place(x=25, y=460)

        else:
            flag1 = False

        if not flag1:
            warning1 = Label(root, text="", fg="red")
            if warning1.winfo_exists() == 1:
                warning1.destroy()
            if principal <= 0 or term <= 0 or APR <= 0 or extraPayment < 0 and flag1 == False:
                warning1 = Label(root, text="", fg="red")
                if warning1.winfo_exists() == 1:
                    print("hi")
                    warning1.destroy()
                warning1 = Label(root, text="Only enter positive numbers. ", fg="red")
                warning1.place(x=50, y=460)
                flag1 = True

            if principal <= extraPayment and flag1 == False:
                warning1 = Label(root, text="", fg="red")
                if warning1.winfo_exists() == 1:
                    warning1.destroy()
                warning1 = Label(root, text="The extra payment must be less than the principal", fg="red")
                warning1.place(x=50, y=460)
                flag1 = True

            if APR < 0.001 or APR > 99.999 and flag1 == False:
                warning1 = Label(root, text="", fg="red")
                if warning1.winfo_exists() == 1:
                    warning1.destroy()
                warning1 = Label(root, text="Please enter an APR between 0.001 and 99.999", fg="red")
                warning1.place(x=50, y=460)
                flag1 = True

            if term < 1 or term > 480 and flag1 == False:
                warning1 = Label(root, text="", fg="red")
                if warning1.winfo_exists() == 1:
                    warning1.destroy()
                warning1 = Label(root, text="Please enter a term amount between 1 and 480", fg="red")
                warning1.place(x=50, y=460)
                flag1 = True

        return flag1

    check1 = char_check()

    if not check1:
        principal = float(principalEntry.get())
        term = float(termEntry.get())
        APR = float(APREntry.get()) / 100
        extraPayment = float(extraPaymentEntry.get())
        top = APR * principal
        r1 = (1 + (APR / 12)) ** -term
        monthlyPayment = top / (12 * (1 - r1))

        for x in range(1, int(term) + 1):
            if principal < monthlyPayment + extraPayment and flag and flag3:
                monthlyInterest = principal * APR / 12
                monthlyPrincipal = principal
                principal = 0
                mI = round(monthlyInterest, 2)
                mP = round(monthlyPrincipal, 2)
                remainingBalance = principal
                displayPayment = monthlyPayment + extraPayment
                schedule[x] = ('Month ' + str(x), '$' + str(principal + round(monthlyInterest, 2)), '$' + str(mP),
                               '$' + str(mI), '$' + str(round(monthlyInterest, 2)),
                               '$' + str(round(remainingBalance, 2)))

                totalInterest += monthlyInterest
                flag = False

            if flag and flag3:
                monthlyInterest = principal * APR / 12
                monthlyPrincipal = monthlyPayment - monthlyInterest + extraPayment
                principal = principal - monthlyPrincipal
                mI = round(monthlyInterest, 2)
                mP = round(monthlyPrincipal, 2)
                displayPayment = monthlyPayment + extraPayment
                remainingBalance = principal
                schedule[x] = ('Month ' + str(x), '$' + str(round(monthlyPayment + extraPayment, 2)), '$' + str(mP),
                               '$' + str(mI), '$' + str(round(totalInterest, 2)), '$' + str(round(remainingBalance, 2)))

                totalInterest += monthlyInterest

        monthlyPaymentLabel2['text'] = round(displayPayment, 2)
        totalInterestLabel2['text'] = round(totalInterest, 2)

        dollarLabel = Label(root, text='$', font=('calibre', 15, 'bold'), bg='white')
        dollarLabel2 = Label(root, text='$', font=('calibre', 17, 'bold'), bg='white')

        scheduleButton = Button(root, text='Open Full Schedule', width=25, height=2)

        scheduleButton.config(fg='white', bg='#00da00')

        dollarLabel.place(x=435, y=87)
        dollarLabel2.place(x=442, y=300)
        scheduleButton.place(x=425, y=400)

        def on_enter(_event):
            scheduleButton['background'] = '#00bb00'

        def on_leave(_event):
            scheduleButton['background'] = '#00da00'

        scheduleButton.bind("<Enter>", on_enter)
        scheduleButton.bind("<Leave>", on_leave)

        def schedule_window(_event):

            scheduleWindow = Toplevel(root)
            scheduleWindow.title("Schedule Window")

            tree = ttk.Treeview(scheduleWindow, selectmode='browse')
            tree.pack(side='right')

            vscrollBar = ttk.Scrollbar(scheduleWindow, orient='vertical', command=tree.yview)
            vscrollBar.pack(side='right', fill='y')

            tree.configure(yscrollcommand=vscrollBar.set)
            tree['columns'] = ('Month', 'Payment', 'Principal', 'Interest', 'Total Interest Paid', 'Balance')
            tree['show'] = 'headings'

            for x in range(6):
                tree.column(str(x), width=125, anchor='c')

            for x in range(6):
                tree.heading(str(x), text=schedule[0][x])

            for x in range(1, list(schedule.keys())[-1] + 1):
                tree.insert('', 'end', text="L" + str(x), values=schedule[x])

        scheduleButton.bind("<Button-1>", schedule_window)


monthlyPaymentLabel = Label(root, text="Monthly Payment", bg='white', font=("calibre", 25, 'bold'))
totalInterestLabel = Label(root, text="Total Interest Paid", bg='white', font=("calibre", 15))

principalLabel = Label(root, text="Principal", font=("calibre", 20))
termLabel = Label(root, text="Term in Months", font=("calibre", 20))
APRLabel = Label(root, text="APR", font=("calibre", 20))
extraPaymentLabel = Label(root, text="Extra Payment", font=("calibre", 20))

monthlyPaymentLabel2 = Label(root, bg='white', font=('calibre', 30, 'bold'))
totalInterestLabel2 = Label(root, bg='white', font=('calibre', 20, 'bold'))

principalEntry = Entry(root, width=23, font=('calibre', 15))
termEntry = Entry(root, width=23, font=('calibre', 15))
APREntry = Entry(root, width=23, font=('calibre', 15))
extraPaymentEntry = Entry(root, width=23, font=('calibre', 15))

calculateButton = Button(root, text="Calculate", fg="white", bg="#00da00",
                         width=20, height=2, font=("calibre", 12))


principalLabel.place(x=40, y=30)
termLabel.place(x=40, y=120)
APRLabel.place(x=40, y=210)
extraPaymentLabel.place(x=40, y=300)

principalEntry.place(x=40, y=70)
termEntry.place(x=40, y=160)
APREntry.place(x=40, y=250)
extraPaymentEntry.place(x=40, y=340)

calculateButton.place(x=65, y=400)

monthlyPaymentLabel.place(x=385, y=20)
totalInterestLabel.place(x=440, y=250)

monthlyPaymentLabel2.place(x=450, y=80)
totalInterestLabel2.place(x=460, y=299)

root.bind('<Return>', calculate)
calculateButton.bind("<Enter>", on_enter)
calculateButton.bind("<Leave>", on_leave)
calculateButton.bind("<Button-1>", calculate)

root.mainloop()
