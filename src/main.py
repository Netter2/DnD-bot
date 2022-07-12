import discord
import random
from discord.ext import commands

prefix = "$"
diceList = []
resultList = []
bot = commands.Bot (command_prefix=prefix)

def make_roll_history (message):
    print (diceList, resultList)
    for i in diceList:
        pos = message.find (i)
        x = resultList.pop(0)
        #print (f'{message [ : pos]} :: {x} :: {message [pos + len(i) : ]}', pos, i)
        message = message [ : pos] + x + message [pos + len(i):]
        
    diceList.clear ()
    resultList.clear ()
    return message

def randomroll (dX): #бросок кубика
    return random.randint (1, dX)

def seek_and_execute (message): #выполнение всех операций в безскобочном выражении
    i = 0
    err = 0
    #print ('Execution initiated.')
    #print ('0 step: ',message)
    while i < len (message): #обработка всех операций броска кубика 
        if message [i] == "d": #при обнаружении операции
            j = 0
            k = 0
            a = 0
            b = 0
            while ((i >= j + 1) and (message [i - j - 1] <= "9") and (message [i - j - 1] >= "0")): #находим значение количества бросаемых кубиков (a)
                j += 1
            while ((len (message) > i + k + 1) and (message [i + k + 1] <= "9") and (message [i + k + 1] >= "0")): #находим значение количества граней кубика (b)
                k += 1
          
            if k == 0:
                err = 2
                return err, message            
            
            b = int (message [i + 1 : i + k + 1])#определение b
            if (j == 0):
                a = 1
                diceList.append (f'd{b}')
            else:
                a = int (message [i - j : i])#определение a
                diceList.append (f'{a}d{b}')
            
            
            buffer = 0
            #sequenceBuffer = '`['
            
            rollBuffer = '`['
            for l in range (a):
                rollResult = randomroll (b)
                #resultList.append (f'{rollResult}')###
                buffer += rollResult
                #rollBuffer.append (str(rollResult))
                if l == 0:
                    rollBuffer += f'{rollResult}'
                else:
                    rollBuffer += f', {rollResult}'
                
            rollBuffer += ']`'
            resultList.append (rollBuffer)
            #rollSequence = rollSequence = rollSequence [ : i + (len(rollSequence) - len (message)) - j] + sequenceBuffer + rollSequence [ i + k + 1 + (len(rollSequence) - len (message)) : ]
            message = message [ : i - j] + str(buffer) + message [ i + k + 1 : ]

            i -= j + 1 #переопределение текущего элемента
        i += 1

    #print ('D-part is complete.')
    #print ('1 step: ',message)
    i = 0
    while i < len (message): #обработка всех операций броска кубика 
        if ((message [i] == "*") or (message [i] == "/")): #при обнаружении операции
            j = 0
            k = 0
            a = 0
            b = 0
            while ((i >= j + 1) and (message [i - j - 1] <= "9") and (message [i - j - 1] >= "0")): #находим значение количества бросаемых кубиков (a)
                j += 1
            while ((len (message) > i + k + 1) and (message [i + k + 1] <= "9") and (message [i + k + 1] >= "0")): #находим значение количества граней кубика (b)
                k += 1

            if j == 0 or k == 0:
                err = 2
                return err, message

            a = int (message [i - j : i])#определение a
            b = int (message [i + 1 : i + k + 1])#определение b
            if (message [i] == "*"):
                c = a * b
            elif (message [i] == "/"):
                c = float(a) / b
            message =  message [ : i - j] + str(c) + message [ i + k + 1 : ]
            i -= j + 1 #переопределение текущего элемента
        i += 1

    #print ('2 step: ',message)
    i = 0
    while i < len (message): #обработка всех операций броска кубика 
        if ((message [i] == "+") or (message [i] == "-")): #при обнаружении операции
            j = 0
            k = 0
            a = 0
            b = 0

            while ((i >= j + 1) and (message [i - j - 1] <= "9") and (message [i - j - 1] >= "0")): #находим значение количества бросаемых кубиков (a)
                j += 1
            while ((len (message) > i + k + 1) and (message [i + k + 1] <= "9") and (message [i + k + 1] >= "0")): #находим значение количества граней кубика (b)
                k += 1

            if j == 0 or k == 0:
                err = 2
                return err, message
            #print (message, i, j, k, message [i - j : i])
            a = int (message [i - j : i])#определение a
            b = int (message [i + 1 : i + k + 1])#определение b
            if (message [i] == "+"):
                c = a+b
            elif (message [i] == "-"):
                c = a-b
            message = message = message [ : i - j] + str(c) + message [ i + k + 1 : ]
            i -= j + 1 #переопределение текущего элемента
        i += 1
    #print ('3 step: ',message)
    
    #print ('* and /-part is complete.')
    return err, message

def brackets_nulifier (message):#функция раскрытия скобок. Коды ошибок: 0 - все хорошо, 1 - неверная скобочная постановка, 2 - проблема при раскрытии скобок
    openBracketsStack = []
    diceList = []
    resultList = []
    err = 0
    i = 0
    while i < len(message):
        if message [i] == "(":
            openBracketsStack.append (i)
        elif message [i] == ")":
            if openBracketsStack == []:
                err = 1#неправильная скобочная расстановка
                break
            else:
                left = openBracketsStack.pop()
                right = i
                #print ('Time to seek and destroy!')
                err, exec_message = seek_and_execute (message[left + 1 : right])
                if err:
                    break
                else:
                    if ((left > 0) and (message [left - 1] != "+") and (message [left - 1] != "-") and (message [left - 1] != "*") and (message [left - 1] != "/")):
                        message = message [ : left] + "*" + exec_message + message [right + 1 : ]
                    else:
                        message = message [ : left] + exec_message + message [right + 1 : ]
                i = left
        i += 1
    #print ('Here')
    if openBracketsStack != []:
        err = 1
    else:
        err, message = seek_and_execute (message)
    #print('Brackets nulified!')
    #print (message)
    return err, message

@bot.event
async def on_ready ():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game ('DnD.'))
    print ("Ready to go!")

@bot.event
async def on_message (message):
    #print ("The message's content was", message.content)
    await bot.process_commands (message)

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')

@bot.command ()
async def roll (ctx, *args):
    message = ''.join (args)#"склейка" всех аргументов в единую строку
    if (message == '$rolld20with advantage,please.'):
        await ctx.send ('Мне лень, сам бросай.')
    messageBuffer = message
    err, message = brackets_nulifier (message)
    #print (make_roll_history (messageBuffer))
    
    #message, rollSequence = message_preprocessing (message)
    #await ctx.send (f'{ctx.message.author.mention} выкинул {rollSequence} = {message}') #добавить комментарии!+результаты броска
    if err == 1:
        await ctx.send (f'{ctx.message.author.mention}, исправь скобки!')
    if err == 2:
        await ctx.send ('Некорректный ввод.')
    else:
        await ctx.send (f'{ctx.message.author.mention} выкинул {make_roll_history (messageBuffer)} = {message}')

bot.run ('OTkyMTM5MjU2MTk5OTIxNzA0.GYDEnX.4lO9vFnKmiua_5E7MtgNmfxhwAZjtg52-iZC9c')
