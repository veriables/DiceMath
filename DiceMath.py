################################################################
## Import Libraries
################################################################
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from DiceRoll import DiceRoll
from tkhtmlview import HTMLLabel

################################################################
## Create a global DiceRoll object
################################################################
NUM_ROLLS = 30000
dr = DiceRoll()

################################################################
## Create window and frames
################################################################
# Creating a window
gui = Tk(className=' Dice Math')
gui.geometry("925x550")
gui.configure(bg="#467249")
gui.resizable(0, 0)

# Create a frame for the buttons
buttons_frame = Frame(gui)
buttons_frame.pack( side = TOP )

# Create a frame to hold the chart and math explanation
display_frame = Frame(gui)
display_frame.pack( side = TOP )

# Create a frame to hold the chart
chart_frame = Frame(display_frame)
chart_frame.pack( side = LEFT )

# Create a frame to hold the math explanation
explanation_frame = Frame(display_frame)
explanation_frame.pack( side = LEFT )

################################################################
## Management Functions
################################################################
def roll():
    dr.rollDice(NUM_ROLLS)
    removeAllButtons()
    createAnalysisButtons()

def closeGraph():
    removeAllButtons()
    createRollButton()
    clearDisplay()
    
def clearDisplay():
    # Clear the chart_frame
    for widget in chart_frame.winfo_children():
        widget.destroy()
    tmp = Frame(chart_frame, width=1, height=1, borderwidth=0, highlightthickness=0)
    tmp.pack()
    chart_frame.update_idletasks()
    tmp.destroy()
    # Clear the explanation_frame
    for widget in explanation_frame.winfo_children():
        widget.destroy()
    tmp = Frame(explanation_frame, width=1, height=1, borderwidth=0, highlightthickness=0)
    tmp.pack()
    explanation_frame.update_idletasks()
    tmp.destroy()

def setButtonState():
    # Disable all analysis buttons before roll
    if dr.total_rolls == 0:
        removeAllButtons()
        createRollButton()
    else:
        removeAllButtons()
        createAnalysisButtons()

################################################################
## Analysis Chart Functions
################################################################

###############################
## Outcome Counts
###############################
def embedOutcomeCountsGraph():
    clearDisplay()
    fig, ax = plt.subplots()
    # Get the data
    data = dr.getCountsOfEachOutcome()
    labels = data.keys()
    counts = data.values()
    # Configure and create the bar chart
    bar_labels = labels
    bar_colours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:blue']
    ax.bar(labels, counts, label=bar_labels, color=bar_colours)
    ax.set_ylabel('Count of Outcomes')
    ax.set_xlabel('Value Rolled')
    ax.set_title('Times Each Outcome was rolled')
    expected = round(((NUM_ROLLS * 2) / 6), 2)
    plt.axhline(y = expected, color = 'r', linestyle = '-')
    # Add the bar chart to a canvas
    canvas = FigureCanvasTkAgg(fig, master = chart_frame)  
    canvas.draw()
    # Place the canvas on the GUI
    canvas.get_tk_widget().pack()
    # Create the matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    # Place the canvas on the TKinter window
    canvas.get_tk_widget().pack()
    # Write the explanation
    embedOutcomeCountsExplanation()

def embedOutcomeCountsExplanation():
    message = dr.getCountsOfEachOutcomeText()
    html = HTMLLabel(explanation_frame, html=message)
    html.pack(padx=8, pady=5, fill="both", expand=True)
    html.fit_height()

###############################
## Who Won
###############################
def embedWhoWonGraph():
    clearDisplay()
    data = dr.getPercentForWins()
    labels = []
    counts = []
    percents = []
    for k, v in data.items():
        labels.append(k + '\n(n = ' + str(v['count']) + ')')
        percents.append(v['percent'])
    explode = (0, 0, 0)
    fig, ax = plt.subplots()
    ax.pie(percents, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')
    # Add the bar chart to a canvas
    canvas = FigureCanvasTkAgg(fig, master = chart_frame)  
    canvas.draw()
    # Place the canvas on the GUI
    canvas.get_tk_widget().pack()
    # Create the matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    # Place the canvas on the TKinter window
    canvas.get_tk_widget().pack()
    # Write the explanation
    embedWhoWonExplanation()

def embedWhoWonExplanation():
    message = dr.getCountsForWinsText()
    html = HTMLLabel(explanation_frame, html=message)
    html.pack(padx=8, pady=5, fill="both", expand=True)
    html.fit_height()

###############################
## Match was a Draw
###############################
def embedTieGraph():
    clearDisplay()
    fig, ax = plt.subplots()
    # Get the data
    data = dr.getCountsForTie()
    labels = data.keys()
    counts = data.values()
    # Configure and create the bar chart
    bar_colours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:blue']
    ax.bar(labels, counts, label=labels, color=bar_colours)
    ax.set_xlabel('Match Outcome')
    ax.set_ylabel('Count of Outcomes')
    ax.set_title('Times the Match was a Tie')
    expected = round((NUM_ROLLS * (1/6)), 2)
    plt.axhline(y = expected, color = 'r', linestyle = '-')
    # Add the bar chart to a canvas
    canvas = FigureCanvasTkAgg(fig, master = chart_frame)  
    canvas.draw()
    # Place the canvas on the GUI
    canvas.get_tk_widget().pack()
    # Create the matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    # Place the canvas on the TKinter window
    canvas.get_tk_widget().pack()
    # Write the explanation
    embedTieExplanation()

def embedTieExplanation():
    message = dr.getCountsForTieText()
    html = HTMLLabel(explanation_frame, html=message)
    html.pack(padx=8, pady=5, fill="both", expand=True)
    html.fit_height()

###############################
## Both were Three
###############################
def embedBothThreeGraph():
    clearDisplay()
    fig, ax = plt.subplots()
    # Get the data
    data = dr.getBothThreeVsTotal()
    labels = data.keys()
    counts = data.values()
    # Configure and create the bar chart
    bar_colours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:blue']
    ax.bar(labels, counts, label=labels, color=bar_colours)
    ax.set_ylabel('Count of Outcomes')
    ax.set_xlabel('Outcome')
    ax.set_title('Did both players roll a 3?')
    expected = round(((NUM_ROLLS) * (1/36)), 2)
    plt.axhline(y = expected, color = 'r', linestyle = '-')
    # Add the bar chart to a canvas
    canvas = FigureCanvasTkAgg(fig, master = chart_frame)  
    canvas.draw()
    # Place the canvas on the GUI
    canvas.get_tk_widget().pack()
    # Create the matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    # Place the canvas on the TKinter window
    canvas.get_tk_widget().pack()
    # Write the explanation
    embedBothThreeExplanation()

def embedBothThreeExplanation():
    message = dr.getBothThreeVsTotalText()
    html = HTMLLabel(explanation_frame, html=message)
    html.pack(padx=8, pady=5, fill="both", expand=True)
    html.fit_height()

###############################
## Either was Three
###############################
def embedEitherThreeGraph():
    clearDisplay()
    fig, ax = plt.subplots()
    # Get the data
    data = dr.getEitherThreeVsTotal()
    labels = data.keys()
    counts = data.values()
    # Configure and create the bar chart
    bar_colours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:blue']
    ax.bar(labels, counts, label=labels, color=bar_colours)
    ax.set_xlabel('Outcome')
    ax.set_ylabel('Count of Outcomes')
    ax.set_title('Did either player roll a 3?')
    expected = round(( NUM_ROLLS ) * (11/36), 2)
    plt.axhline(y = expected, color = 'r', linestyle = '-')
    # Add the bar chart to a canvas
    canvas = FigureCanvasTkAgg(fig, master = chart_frame)  
    canvas.draw()
    # Place the canvas on the GUI
    canvas.get_tk_widget().pack()
    # Create the matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    # Place the canvas on the TKinter window
    canvas.get_tk_widget().pack()
    # Write the explanation
    embedEitherThreeExplanation()

def embedEitherThreeExplanation():
    message = dr.getEitherThreeVsTotalText()
    html = HTMLLabel(explanation_frame, html=message)
    html.pack(padx=8, pady=5, fill="both", expand=True)
    html.fit_height()

def embedXorThreeGraph():
    clearDisplay()
    fig, ax = plt.subplots()
    # Get the data
    data = dr.getXorThreeVsTotal()
    labels = data.keys()
    counts = data.values()
    # Configure and create the bar chart
    bar_colours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:blue']
    ax.bar(labels, counts, label=labels, color=bar_colours)
    ax.set_xlabel('Outcome')
    ax.set_ylabel('Count of Outcomes')
    ax.set_title('Did only one player roll a three?')
    expected = round(( NUM_ROLLS ) * (5/18), 2)
    plt.axhline(y = expected, color = 'r', linestyle = '-')
    # Add the bar chart to a canvas
    canvas = FigureCanvasTkAgg(fig, master = chart_frame)  
    canvas.draw()
    # Place the canvas on the GUI
    canvas.get_tk_widget().pack()
    # Create the matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    # Place the canvas on the TKinter window
    canvas.get_tk_widget().pack()
    # Write the explanation
    embedXorThreeExplanation()

def embedXorThreeExplanation():
    message = dr.getXorThreeVsTotalText()
    html = HTMLLabel(explanation_frame, html=message)
    html.pack(padx=8, pady=5, fill="both", expand=True)
    html.fit_height()

def embedNeitherThreeGraph():
    clearDisplay()
    fig, ax = plt.subplots()
    # Get the data
    data = dr.getNeitherThreeVsTotal()
    labels = data.keys()
    counts = data.values()
    # Configure and create the bar chart
    bar_colours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:blue']
    ax.bar(labels, counts, label=labels, color=bar_colours)
    ax.set_xlabel('Outcome')
    ax.set_ylabel('Count of Outcomes')
    ax.set_title('Did neither player roll a three?')
    expected = round(( NUM_ROLLS ) * (25/36), 2)
    plt.axhline(y = expected, color = 'r', linestyle = '-')
    # Add the bar chart to a canvas
    canvas = FigureCanvasTkAgg(fig, master = chart_frame)  
    canvas.draw()
    # Place the canvas on the GUI
    canvas.get_tk_widget().pack()
    # Create the matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    # Place the canvas on the TKinter window
    canvas.get_tk_widget().pack()
    # Write the explanation
    embedNeitherThreeExplanation()

def embedNeitherThreeExplanation():
    message = dr.getNeitherThreeVsTotalText()
    html = HTMLLabel(explanation_frame, html=message)
    html.pack(padx=8, pady=5, fill="both", expand=True)
    html.fit_height()

################################################################
## Buttons
################################################################
def removeAllButtons():
    for widget in buttons_frame.winfo_children():
        widget.destroy()
    tmp = Frame(buttons_frame, width=1, height=1, borderwidth=0, highlightthickness=0)
    tmp.pack()
    buttons_frame.update_idletasks()
    tmp.destroy()

def createRollButton():
    button_roll = Button(buttons_frame, text="Roll " + str(NUM_ROLLS) + " times!", fg="red", command=roll)
    button_roll.pack( side = TOP, pady=8 )

def createAnalysisButtons():
    button_outcome_counts = Button(buttons_frame, text="Outcome Counts", fg="green", command=embedOutcomeCountsGraph)
    button_outcome_counts.pack( side = LEFT )

    button_tie = Button(buttons_frame, text="Tie Score", fg="green", command=embedTieGraph)
    button_tie.pack( side = LEFT )

    button_who_won = Button(buttons_frame, text="Who Won?", fg="green", command=embedWhoWonGraph)
    button_who_won.pack( side = LEFT )

    button_both_3 = Button(buttons_frame, text="Both 3", fg="green", command=embedBothThreeGraph)
    button_both_3.pack( side = LEFT )

    button_any_3 = Button(buttons_frame, text="Any 3", fg="green", command=embedEitherThreeGraph)
    button_any_3.pack( side = LEFT )

    button_xor_3 = Button(buttons_frame, text="XOR 3", fg="green", command=embedXorThreeGraph)
    button_xor_3.pack( side = LEFT )

    button_neither_3 = Button(buttons_frame, text="Neither 3", fg="green", command=embedNeitherThreeGraph)
    button_neither_3.pack( side = LEFT )

    button_close_graph = Button(buttons_frame, text="Close Graphs", fg="green", command=closeGraph)
    button_close_graph.pack( side = LEFT )

createRollButton() # Set initial state for buttons

################################################################
## Start the main loop
################################################################
gui.mainloop()

