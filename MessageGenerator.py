import json
from datetime import datetime
import pytz

'''
Takes in the file of the template json and allows for user uploading of new
templates from the terminal
'''
class MessageTemplate:
    templates = []
    firstUserIndex = 0

    def __init__(self, template):
        templateFile = open(template, 'r')
        for template in json.loads(templateFile.read()):
            self.templates.append(template)
        templateFile.close()
        firstUserIndex = self.templates[len(self.templates) - 1]['id'] + 1

    def getTemplate(self, id):
        for template in self.templates:
            if int(template['id']) == id:
                return template

    def getAllTemplates(self):
        return self.templates

    def getLargestId(self):
        return self.templates[len(self.templates) - 1]['id']

    def addTemplateFromFile(self, template): 
        templateFile = open(template, 'r')
        self.templates.append(json.loads(templateFile.read()))

    def addUserTemplate(self, template):
        userFile = open("UserTemplates.json", 'r')
        if userFile.read() == None:
            userFile.close()
            userFile = open("UserTemplates.json", 'w')
            userFile.write(json.dumps(template))
        else:
            previousAdditions = json.loads(userFile.read())
            previousAdditions += template
            userFile.close()
            userFile = open("UserTemplates.json", 'w')
            userFile.write(json.dumps(previousAdditions))
        userFile.close()
        self.templates.append(template)

    def userGeneratedTemplate(self, companyRead, guestRead):
        newGreetingId = len(self.templates) + 1
        newGreetingText = []
        newGreetingFields = []
        print('\n')
        print("To create a new template you will be asked to insert text and "
            "keywords together. The way they will be displayed is that it will "
            "print text, then keyword, then text until there are no more. This "
            "means that you must start with a piece of text followed by a field "
            "and so on. There are other commands to remove previous decisions"
            ", clear the input, or finish and load the template.")

        print('\n')
        templateType = input("What's the theme of your new template?: ")
        companyKeywords = companyRead.getKeywords()
        guestKeywords = guestRead.getKeywords()
        alternate = "text"
        repeat = False
        nextCommand = ""
        while nextCommand != "done":
            if alternate == "text":
                print('\n')
                nextCommand = input("Add whatever text you'd like next (or a"
                                    " command like 'clear', 'remove last "
                                    "keyword', 'remove last text', or 'done'): ")
                print('\n')
                
                if nextCommand == "clear":
                    newGreetingText = []
                    newGreetingFields = []

                elif nextCommand == "remove last keyword":
                    del newGreetingFields[len(newGreetingFields) - 1]

                elif nextCommand == "remove last text":
                    del newGreetingText[len(newGreetingText) - 1]

                elif nextCommand == "done":
                    break

                else:
                    newGreetingText.append(nextCommand)
                
                MessageTemplate.incompleteGreeting(newGreetingText, newGreetingFields)
                print('\n')
                alternate = "field"
            
            elif alternate == "field":
                print("Here are all the available company keywords: ")
                tempId = 1
                for word in companyKeywords:
                    print(word + "  " + str(tempId))
                    tempId += 1
                print("And here are all the available guest keywords: ")
                for word in guestKeywords:
                    print(word + "  " + str(tempId))
                    tempId += 1
                print('\n')
                nextCommand = input("type the full keyword or the number to its left: "
                                "(or a command like 'clear', 'remove last "
                                "keyword', 'remove last text', or 'done'): ")
                print('\n')
                #I don't think there's a switch statement in python
                if nextCommand == "company" or nextCommand == "1":
                    newGreetingFields.append({"file": "Companies", "key": "company"})
                elif nextCommand == "city" or nextCommand == "2":
                    newGreetingFields.append({"file": "Companies", "key": "city"})
                elif nextCommand == "timezone" or nextCommand == "3":
                    newGreetingFields.append({"file": "Companies", "key": "timezone"})
                elif nextCommand == "firstName" or nextCommand == "4":
                    newGreetingFields.append({"file": "Guests", "key": "firstName"})
                elif nextCommand == "lastName" or nextCommand == "5":
                    newGreetingFields.append({"file": "Guests", "key": "lastName"})
                elif nextCommand == "reservation: roomNumber" or nextCommand == "6":
                    newGreetingFields.append({"file": "Guests", "key": "reservation", "innerKey": "roomNumber"})
                elif nextCommand == "reservation: startTimestamp" or nextCommand == "7":
                    newGreetingFields.append({"file": "Guests", "key": "reservation", "innerKey": "startTimestamp"})
                elif nextCommand == "reservation: endTimestamp" or nextCommand == "8":
                    newGreetingFields.append({"file": "Guests", "key": "reservation", "innerKey": "endTimestamp"})
                
                elif nextCommand == "clear":
                    newGreetingText = []
                    newGreetingFields = []

                elif nextCommand == "remove last keyword":
                    del newGreetingFields[len(newGreetingFields) - 1]

                elif nextCommand == "remove last text":
                    del newGreetingText[len(newGreetingText) - 1]

                elif nextCommand == "done":
                    break

                else:
                    print("enter a correct command next time")
                    repeat = True


                MessageTemplate.incompleteGreeting(newGreetingText, newGreetingFields)
                if repeat:
                    alternate = "field"
                else:
                    alternate = "text"

        newTemplate = {"id": newGreetingId, "type": templateType, "text": newGreetingText,
                        "fields": newGreetingFields}
        self.addUserTemplate(newTemplate)
        print(str(newTemplate))
        return newGreetingId

    def incompleteGreeting(greetingText, greetingFields):
        finalGreeting = ""
        maxLength = max(len(greetingText),len(greetingFields))
        for i in range(maxLength): 
            #adding the text
            if i < len(greetingText):
                finalGreeting += str(greetingText[i])
            
            #adding the variables
            if i < len(greetingFields):
                if len(greetingFields[i]) == 3:
                    finalGreeting += str(greetingFields[i]['key']) + " " + str(greetingFields[i]['innerKey'])
                else:
                    finalGreeting += str(greetingFields[i]['key'])
        print("What your template looks like so far: ")
        print(finalGreeting)    


'''
Takes in the file of the guest json
'''
class GuestInfo:
    guests = []
    guestKeywords = ["firstName", "lastName", "reservation: roomNumber", 
    "reservation: startTimestamp", "reservation: endTimestamp"]

    def __init__(self, guest):
        guestFile = open(guest, 'r')
        for guest in json.loads(guestFile.read()):
            self.guests.append(guest)
        guestFile.close()

    def getGuest(self, id):
        for person in self.guests:
            if int(person['id']) == id:
                return person

    def getAllGuests(self):
        return self.guests

    def getKeywords(self):
        return self.guestKeywords

'''
Takes in the file of the company json
'''
class CompanyInfo:
    companies = []
    companyKeywords = ["company", "city", "timezone"]

    def __init__(self, company):
        companyFile = open(company, 'r')
        for company in json.loads(companyFile.read()):
            self.companies.append(company)
        companyFile.close()

    def getCompany(self, id):
        for corporation in self.companies:
            if int(corporation['id']) == id:
                return corporation

    def getAllCompanies(self):
        return self.companies

    def getKeywords(self):
        return self.companyKeywords

'''
The way this somewhat cumbersome system works is that the guest and company
fields are each dictionaries of the respective guest and company and the
loop goes through the greeting template and alternates between adding the next
piece of the greeting and the next corresponding field. The template variable
has the array of strings that makes up the greeting and the templateFields
variable holds the arrays that contain the keys to the guest or company dicts.
Not super clean but it works.
'''
def createGreeting(guest, company, greeting, fields):
    finalGreeting = ""
    maxLength = max(len(greeting),len(fields))
    
    for i in range(maxLength): 
        
        #adding the text
        if i < len(greeting):
            finalGreeting += str(greeting[i])
        
        #adding the variables
        if i < len(fields):
            if fields[i]['file'] == "Guests":
                response = guest[fields[i]['key']]
                
                #Adding the morning/afternoon test
                if len(fields[i]) == 3 and fields[i]['innerKey'] == 'startTimestamp':
                    timestamp = float(response[fields[i]['innerKey']])
                    timezone = pytz.timezone(company['timezone'])
                    actualTime = datetime.fromtimestamp(timestamp, timezone)
                    if actualTime.hour <= 12:
                        response = "morning"
                    else:
                        response = "afternoon"

                #the other options would be room numbers
                elif len(fields[i]) == 3:
                    response = response[fields[i]['innerKey']]
                
                #If the field isn't in the reservation section
                finalGreeting += str(response)

            elif fields[i]['file'] == "Companies":
                finalGreeting += company[fields[i]['key']]

    return finalGreeting

'''
This method provides the basic terminal user interface 
'''
def terminalSession(message, guestRead, companyRead):
    print("Welcome to this basic greeting generator!")
    
    #List of all of the templates
    print("Here's a list of general templates to choose from."
        " You can also create your own template if you like.")
    for template in message.getAllTemplates():
        print("Type of greeting: " + template['type'] + ".      id number: "
                 + str(template['id']))
    
    #Dealing with erroneous inputs
    templateNumber = input("Choose an id number or type 'create' "
                        " to create your own template: ")
    if templateNumber == "create":
        templateNumber = str(message.userGeneratedTemplate(companyRead, guestRead))
    while templateNumber.isdigit() == False:
        templateNumber = input("Choose a real number: ")
    while int(templateNumber) < 1 or int(templateNumber) > len(message.getAllTemplates()):
        templateNumber = input("Choose one of the offered id numbers: ")

    #List of all of the companies
    print('\n')
    print("Now here's a list of companies to choose from.")
    for company in companyRead.getAllCompanies():
        print("Company: " + company['company'] + ".     Id number: " +\
         str(company['id']))
    
    #Dealing with erroneous inputs
    companyNumber = input("Choose an id number: ")
    while companyNumber.isdigit() == False:
        companyNumber = input("Choose a real number: ")
    while int(companyNumber) < 1 or int(companyNumber) > len(companyRead.getAllCompanies()):
        companyNumber = input("Choose one of the offered id numbers: ") 
    
    #List of all the guests
    print('\n')
    print("Wonderful, now here's a list of all the guests to send a message to")
    for guest in guestRead.getAllGuests():
        print("Guest: " + guest['firstName'] + " " + guest['lastName'] + ".\
    Id number: " + str(guest['id']))
    
    #Dealing with erroneous inputs
    guestNumber = input("Choose an id number: ")
    while guestNumber.isdigit() == False:
        guestNumber = input("Choose a real number: ")
    while int(guestNumber) < 1 or int(guestNumber) > len(guestRead.getAllGuests()):
        guestNumber = input("Choose one of the offered id numbers: ") 

    guest = guestRead.getGuest(int(guestNumber))
    company = companyRead.getCompany(int(companyNumber))
    template = message.getTemplate(int(templateNumber))
    
    greeting = template['text']
    fields = template['fields']

    print('\n')
    print(createGreeting(guest, company, greeting, fields))

'''
Loads in the existing json files and opens up the user interface
'''
def main():
    message = MessageTemplate("Templates.json")
    guestRead = GuestInfo("Guests.json")
    companyRead = CompanyInfo("Companies.json")

    terminalSession(message, guestRead, companyRead)
    
    #dealing with repeat messages
    response = input("Do you want to create another session? (yes/no)")
    while response == "yes":
        terminalSession(message, guestRead, companyRead)
        response = input("Do you want to create another session? (yes/no)")
    print("Thank you for your bussiness and have a nice day!")

main() 
if __name__ == 'main':
    main()
