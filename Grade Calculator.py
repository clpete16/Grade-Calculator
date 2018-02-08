from __future__ import division
from Tkinter import *
import os
import pickle
import ttk


# A random directory to store files (windows only I guess)
directory = "c:\\users\\public\\Python Pickles\\"

# Makes the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)


def file_import(filename):
    with open(directory + filename, 'rb') as f:
        variable_name = pickle.load(f)
        return variable_name


def file_export(filename, variable_name):
    with open(directory + filename, 'wb') as f:
        pickle.dump(variable_name, f)


# Tries to load the file containing stored classes; if it doesn't exist, create a blank dict for new classes
try:
    allClasses = file_import('classes.pickle')
except IOError:
    allClasses = {}


def quitApp():
    file_export('classes.pickle', allClasses)
    root.destroy()


# Root Window, non-resizable by user
root = Tk()
root.resizable(width=False, height=False)

# Makes [x] button do quitApp first
root.protocol('WM_DELETE_WINDOW', quitApp)

# Left Frame, holds general commands and stored classes
leftFrame = Frame(root)
leftFrame.grid(row=0)

# Right Frame, holds information about the class and class-specific commands
rightFrame = Frame(root)

# Separator between left and right frame (visual aid)
ttk.Separator(root, orient='vertical').grid(row=0, column=1, sticky='ns')

# Adds a new class instance; rebuilds the right frame to default


def addClass():
    global rightFrame
    rightFrame.grid_forget()
    rightFrame = Frame(root)
    rightFrame.grid(row=0, column=2)
    newClass = ClassOptions(rightFrame)
    newClass.addSection()


# Main Labels and Buttons for the left frame; are permanent
MainLabel = Label(leftFrame, text="Classes:", width=50)
MainLabel.pack(side='top')

quitButton = Button(leftFrame, text='Quit', command=quitApp)
quitButton.pack(side='bottom')

addClassButton = Button(leftFrame, text='Add new class', command=addClass)
addClassButton.pack(side='bottom')

# Don't think it's necessary to have a class for this but here it is anyways (I just learned about em, and figured I
# should use it). I'm certain I'm not using it as intended... But it works so eh


class ClassOptions:
    # Resets the right frame and class, buttons are pretty self explanatory
    def __init__(self, rightFrame):
        self.sections = 0

        self.rightFrame = rightFrame

        self.className = Label(self.rightFrame, text='Class name:')
        self.className.grid(row=0, column=0)

        # Spacer between class name and section/weight/grade area
        self.spacerOne = Label(self.rightFrame, text='')
        self.spacerOne.grid(row=1, columnspan=3)

        self.sectionsLabel = Label(self.rightFrame, text='Section')
        self.sectionsLabel.grid(row=2, column=0)

        self.weightsLabel = Label(self.rightFrame, text='Weight')
        self.weightsLabel.grid(row=2, column=1)

        self.gradeLabel = Label(self.rightFrame, text='Grade (%)')
        self.gradeLabel.grid(row=2, column=2)

        self.nameEntry = Entry(self.rightFrame)
        self.nameEntry.grid(row=0, column=1, columnspan=2, sticky='ew')

        # Defining buttons that are placed later
        self.addSectionButton = Button(self.rightFrame, text='Add new section', command=self.addSection)
        self.removeSectionButton = Button(self.rightFrame, text='Remove Last Section', command=self.removeSection)
        self.errorSpace = Label(self.rightFrame)
        self.calcButton = Button(self.rightFrame)
        self.saveButton = Button(self.rightFrame)
        self.gradeOutput = Label(self.rightFrame)
        self.spacerCalcSave = Label(self.rightFrame)
        self.deleteButton = Button(self.rightFrame)

        # Arrays that are used to store entries in section/weight/grade
        self.sectionNameList = []
        self.sectionWeightList = []
        self.sectionGradeList = []

    # Builds the buttons in the left frame for each saved class
    def buildClassButtons(self):
        global classButtons
        classButtons = []

        # allClasses is the dict where classes and their data are stored in
        for key in allClasses:
            # the lambda function makes sure each button is identifiable from another (uses the text of the button,
            # which is the name of the class)
            self.classButton = Button(leftFrame, text=key, command=lambda j=key: self.rebuildClass(j))
            classButtons.append(self.classButton)
            self.classButton.pack()

    # Adds a section below the last, stored in arrays created in __init__
    def addSection(self):

        # Limits to 25 sections (b/c even that limit is ridiculous and there needs to be one)
        if self.sections >= 25:
            self.buildErrorMessage('You can\'t have more than 25 sections  =/')
        else:
            self.sections += 1

            self.newSectionName = Entry(self.rightFrame, justify='center')
            self.sectionNameList.append(self.newSectionName)
            self.newSectionName.grid(row=self.sections + 2)

            self.newSectionWeight = Entry(self.rightFrame, justify='center')
            self.sectionWeightList.append(self.newSectionWeight)
            self.newSectionWeight.grid(row=self.sections + 2, column=1)

            self.newSectionGrade = Entry(self.rightFrame, justify='center')
            self.sectionGradeList.append(self.newSectionGrade)
            self.newSectionGrade.grid(row=self.sections + 2, column=2)

            self.buildButtons('')

    # Removes the last section, deletes the according entry in arrays created in __init__
    def removeSection(self):

        if self.sections > 1:
            self.sections -= 1
            self.sectionNameList[self.sections].destroy()
            del self.sectionNameList[self.sections]
            self.sectionWeightList[self.sections].destroy()
            del self.sectionWeightList[self.sections]
            self.sectionGradeList[self.sections].destroy()
            del self.sectionGradeList[self.sections]
            self.buildButtons('')
        elif self.sections <= 1:
            self.buildErrorMessage('You must leave at least one section')

    # Saves the class's data into a dict, to be stored in the main dict, allClasses
    def compileClass(self):

        # Makes sure there is a name, then begins saving
        if self.nameEntry.get() != '':
            self.nameEntry.configure(bg='white')
            self.buildErrorMessage('')

            self.sectionNameSave = []
            self.sectionWeightSave = []
            self.sectionGradeSave = []

            # Goes through the sections/weights/grades and stores them
            # Blank or text entries are fine for saving weights/grades, but won't be able to calculate later
            for i in range(self.sections):
                self.sectionNameSave.append(self.sectionNameList[i].get())
                self.buildErrorMessage('')

                try:
                    # Converts weights to hundredths
                    self.num = float(self.sectionWeightList[i].get())
                    if self.num > 1.00:
                        self.num /= 100.0
                    self.sectionWeightList[i].delete(0, 'end')
                    self.sectionWeightList[i].insert(END, str(self.num))
                except:
                    pass
                self.sectionWeightList[i].configure(bg='white')
                self.sectionWeightSave.append(self.sectionWeightList[i].get())


                try:
                    # Converts grades to percents
                    self.num2 = float(self.sectionGradeList[i].get())
                    if self.num2 < 1.00:
                        self.num2 *= 100.0
                    self.sectionGradeList[i].delete(0, 'end')
                    self.sectionGradeList[i].insert(END, str(self.num2))
                except:
                    pass
                self.sectionGradeList[i].configure(bg='white')
                self.sectionGradeSave.append(self.sectionGradeList[i].get())

            # Globals the class save to be put into allClasses, and builds the save from above data
            global classSave
            classSave = {
                'Name': self.nameEntry.get(),
                'Sections': self.sections,
                'Section Names': self.sectionNameSave,
                'Section Weights': self.sectionWeightSave,
                'Section Grades': self.sectionGradeSave
            }
            allClasses[classSave['Name']] = classSave

            # Gets the save data into a local variable for some reason I'm sure is totally necessary . . .
            self.classSave = classSave

            # Checks if the class already has a button, and creates one if it does not
            self.skip = 0
            for i in range(len(classButtons)):
                if classButtons[i].cget('text') == classSave['Name']:
                    self.skip = 1
            if self.skip == 0:
                self.classButton = Button(leftFrame, text=classSave['Name'],
                                          command=lambda j=self.nameEntry.get(): self.rebuildClass(j))
                classButtons.append(self.classButton)
                self.classButton.pack()

        # Makes sure the user has entered a name for the class
        elif self.nameEntry.get() == '':
            self.nameEntry.configure(bg='red')
            self.buildErrorMessage('You need to name your class first!')

    # Calculates the grade based on entered weights/grades
    def calculateGrade(self):
        self.sectionWeightSaveCalc = []
        self.sectionGradeSaveCalc = []
        self.buildErrorMessage('')
        # Very similar to class save, it builds weights and grades into array to be used
        # Converts weights to hundredths and grades to percents when available
        # Makes sure that there are numbers in each category
        for i in range(self.sections):
            try:
                self.num = float(self.sectionWeightList[i].get())
                if self.num > 1.00:
                    self.num /= 100.0
                self.sectionWeightList[i].delete(0, 'end')
                self.sectionWeightList[i].insert(END, str(self.num))

                self.sectionWeightList[i].configure(bg='white')
                self.sectionWeightSaveCalc.append(self.num)
            except:
                self.buildErrorMessage('You must enter a number')
                self.sectionWeightList[i].configure(bg='red')
                return

            try:
                self.num2 = float(self.sectionGradeList[i].get())
                if self.num2 < 1.00:
                    self.num2 *= 100.0
                self.sectionGradeList[i].delete(0, 'end')
                self.sectionGradeList[i].insert(END, str(self.num2))

                self.sectionGradeList[i].configure(bg='white')
                self.sectionGradeSaveCalc.append(self.num2)

            # Allows division input in the grade section (disallows letters so eval is 'safer')
            except:
                try:
                    if any(q in self.sectionGradeList[i].get() for q in ['+', '-', '*', '/']) and \
                            not any(q.isalpha() for q in self.sectionGradeList[i].get()):
                        self.num2 = round(eval(str(self.sectionGradeList[i].get())), 3)
                        if self.num2 < 2:
                            self.num2 *= 100
                        self.sectionGradeList[i].delete(0, 'end')
                        self.sectionGradeList[i].insert(END, str(self.num2))

                        self.sectionGradeList[i].configure(bg='white')
                        self.sectionGradeSaveCalc.append(self.num2)
                    else:
                        raise TypeError
                except:
                    self.buildErrorMessage('You must enter a number')
                    self.sectionGradeList[i].configure(bg='red')
                    return

        # Checks is the sum of the weights is close to 1.00 (within 1.1%)
        # This allows 3 sections of .33 for example
        if abs(sum(self.sectionWeightSaveCalc) - 1.00) >= 0.011:
            self.buildErrorMessage('The weights must sum to 1.00')
            return

        # Calculates the grade by multiplying each grade by its corresponding weight and adds that to the total
        else:
            self.gradeSum = 0
            for i in range(self.sections):
                self.gradeSum += (self.sectionGradeSaveCalc[i] * self.sectionWeightSaveCalc[i])
            self.gradeSum /= sum(self.sectionWeightSaveCalc)

            # Builds the gradeOutput label with the newly calculated grade
            self.gradeOutput.destroy()
            self.gradeOutput = Label(self.rightFrame, text=str(round(self.gradeSum, 3)) + ' %')
            self.gradeOutput.grid(row=self.sections + 7, column=2, rowspan=3)

    # Builds the buttons below the section/weight/grade boxes and refits the window
    def buildButtons(self, message):

        self.destroyButtons()

        self.removeSectionButton = Button(self.rightFrame, text='Remove Last Section', command=self.removeSection)
        self.removeSectionButton.grid(row=self.sections + 3, column=2)

        self.addSectionButton = Button(self.rightFrame, text='Add New Section', command=self.addSection)
        self.addSectionButton.grid(row=self.sections + 3)

        self.message = message
        self.errorSpace = Label(self.rightFrame, text=self.message, fg='red')
        self.errorSpace.grid(row=self.sections + 6, columnspan=3)

        self.calcButton = Button(self.rightFrame, text='Calculate Grade', command=self.calculateGrade)
        self.calcButton.grid(row=self.sections + 7, column=0)

        self.spacerCalcSave = Label(self.rightFrame, text='')
        self.spacerCalcSave.grid(row=self.sections + 8, column=0)

        self.saveButton = Button(self.rightFrame, text='Save Class', command=self.compileClass)
        self.saveButton.grid(row=self.sections + 9, column=0)

        self.gradeOutput = Label(self.rightFrame, text='')
        self.gradeOutput.grid(row=self.sections + 7, column=2, rowspan=3)

        self.deleteButton = Button(self.rightFrame, text='Delete Class', command=self.deleteClass)
        self.deleteButton.grid(row=self.sections + 9, column=1)

        root.resizable(height=True)
        self.c = Canvas(root)
        try:
            # I don't know why it works like this, and only like this, but it does, so it stays
            self.c.pack(fill='WHY DOES THIS WORK', expand='yes')
        except:
            pass
        root.resizable(height=False)

    # Destroys all buttons below the section/weight/grade boxes
    def destroyButtons(self):
        self.gradeOutput.destroy()
        self.saveButton.destroy()
        self.removeSectionButton.destroy()
        self.addSectionButton.destroy()
        self.errorSpace.destroy()
        self.calcButton.destroy()
        self.spacerCalcSave.destroy()
        self.deleteButton.destroy()

    # Builds an error message with a given message . . .
    def buildErrorMessage(self, message):
        self.message = message
        self.errorSpace.destroy()
        self.errorSpace = Label(self.rightFrame, text=self.message, fg='red')
        self.errorSpace.grid(row=self.sections + 6, columnspan=3)

    # Loads the class from storage
    # Rebuilds the right frame from scratch, then goes through the stored section/weight/grade entries and fills them
    def rebuildClass(self, name):
        global rightFrame
        rightFrame.grid_forget()
        rightFrame = Frame(root)
        rightFrame.grid(row=0, column=2)
        self.rebuildSkip = 1
        self.classSave = allClasses[name]
        self.__init__(rightFrame)
        for i in range(self.classSave['Sections']):
            self.addSection()
            self.newSectionName.insert(END, self.classSave['Section Names'][i])
            self.newSectionWeight.insert(END, self.classSave['Section Weights'][i])
            self.newSectionGrade.insert(END, self.classSave['Section Grades'][i])
        self.sections = self.classSave['Sections']
        self.buildButtons('')

        # If none of the weights/grades are empty, try and calculate the grade
        try:
            if '' not in self.classSave['Section Weights'] and '' not in self.classSave['Section Grades']:
                self.calculateGrade()
        except:
            pass
        self.nameEntry.insert(END, self.classSave['Name'])

    # Deletes the class from stored data and removes its button
    def deleteClass(self):
        for i in range(len(classButtons)):
            if classButtons[i].cget('text') == self.nameEntry.get():
                classButtons[i].destroy()
                del classButtons[i]
                break
        del allClasses[self.nameEntry.get()]
        addClass()


# Builds the initial right frame
rightFrame.grid_forget()
rightFrame = Frame(root)
rightFrame.grid(row=0, column=2)
starter = ClassOptions(rightFrame)
starter.buildClassButtons()
starter.addSection()
root.mainloop()
