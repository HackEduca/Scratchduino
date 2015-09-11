#!/usr/bin/python
# coding=utf-8

# -*- coding: utf-8 -*-

"""
Created on Wed Nov  25 13:17:15 2013

@author: Alan Yorinks
Copyright (c) 2013-14 Alan Yorinks All right reserved.

@author: awangenh
Adaptations for GUI usage: Aldo von Wangenheim
Copyright (c) 2013-15 Iniciativa Computação na Escola

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
#from __future__ import print_function
import os
import sys
import logging
from scratchduino_pymata import PyMata
import scratchduino_http_server
from scratchduino_command_handlers import ScratchduinoCommandHandlers
import time
from Tkinter import *
import tkFont
import serial.tools.list_ports
import threading
import scratchduino_dialog
import webbrowser


windowbg = '#606060'
menubarbg = '#808080'
frame = ''


'''def print(aString):
    frame.text.insert(END, '\n' + aString)
    frame.text.see(END)
    frame.update_idletasks()'''


# noinspection PyBroadException



def window():
    global frame
    root = Tk()
    root.geometry("710x400+50+50")
    root.title("SCRATCHDUINO")
    root.configure(background=windowbg)

    frame = Scratchduino(root)
    frame.show_msg(51)
    frame.search_comports()
    frame.show_msg(52)
    root.mainloop()

#=======================================================================================================================
class Scratchduino(Frame):
#     Window where s2a_fm runs...
#=======================================================================================================================

    def __init__(self, master):
        """Initialize the frame subclass"""
        Frame.__init__(self, master)
        self.configure(background=windowbg)
        self.grid()
        self.create_msg()
        self.create_menu(master)
        self.create_widgets()

    def create_msg(self):
        self.en = 0
        self.pt = 1
        self.lang = self.pt
        self.msg = [
            ['en', 'pt'],
            ['english','português'],
            #scratchduino_http_server MSgs. First Index: 2
            ['Starting HTTP Server!', 'Iniciando Servidor Web!'], #2
            ['Click [Stop Server] to stop the Scratchduino Server', 'Pressione [Parar Servidor] para terminar Scratchduino'], #3
            ['Please start Scratch or Snap!', 'Por favor inicie Scratch ou Snap!'], #4
            ['HTTP Socket may already be in use - restart Scratch', 'Socket HTTP está em uso - tente reiniciar Scratch'], #5
            ['Goodbye !', 'Tchau !'], #6
            ['', ''], #7 Leave open for future HTTP messages
            ['', ''], #8 Leave open for future HTTP messages
            ['', ''], #9 Leave open for future HTTP messages
            ['', ''], #10 Leave open for future HTTP messages
            #scratchduino_pymata messages. First index: 11
            ['Scratchduino_PyMata  Copyright(C) 2013-15 Iniciativa Computação na Escola', 'Scratchduino_PyMata  Copyright(C) 2013-15 Iniciativa Computação na Escola'], #11
            ['PyMata version 1.57  Copyright(C) 2013-14 Alan Yorinks    All rights reserved.', 'PyMata version 1.57  Copyright(C) 2013-14 Alan Yorinks - Todos direitos reservados.'], #12
            ['Please wait while Arduino is being detected. This can take up to 30 seconds ...', 'Aguarde enquanto o Arduino é detectado. Isso pode levar até 30 segundos...'], #13
            ["Closing PyMata: Hope to see you soon!",'Finalizando PyMata: Até logo!'], #14
            ["sonar_config: maximum number of devices assigned - ignoring request", 'Configuração do SONAR: máximo de dispositivos já atingido. Ignorando solicitação!'], #15
            ["Stepper Library Version Request timed-out.Did you send a stepper_request_library_version command?", 'Tempo de espera por solicitação de versão da biblioteca de Motor de Passo esgotado.'], #16
            ["Board Auto Discovery Failed!, Shutting Down.", 'Auto-decoberta do Arduino falhou! Parando.'], #17
            ['Opening Arduino Serial port: ', 'Abrindo Arduino na porta serial: '], #18 Pymata Serial message
            ['', ''], #19 Leave open for future Pymata messages
            ['', ''], #20 Leave open for future Pymata messages
            #scratchduino_command_handlers messages. First index: 21
            ['SCRATCH/SNAP! detected! Ready to rock and roll...', 'SCRATCH ou SNAP! detectado!! Pronto para mandar brasa...' ], #21
            ['ERROR in digital_pin_mode: The pin number must be set to a numerical value', 'ERRO no modo_de_pino_digital: Indique um número para o pino.'], #22
            ['ERROR in digital_pin_mode: pin exceeds number of pins on board', 'ERRO no modo_de_pino_digital: Foi indicado um pino que não existe.'], #23
            ['ERROR in digital_pin_mode: Pin does not support INPUT mode.', 'ERRO no modo_de_pino_digital: Pino não aceita ser de ENTRADA.'], #24
            ['ERROR in digital_pin_mode: Pin does not support SONAR mode', 'ERRO no modo_de_pino_digital: Pino não aceita operar em modo SONAR.'], #25
            ['ERROR in digital_pin_mode: Pin does not support OUTPUT mode', 'ERRO no modo_de_pino_digital: Pino não aceita operar em modo de SAÍDA.'], #26
            ['ERROR in digital_pin_mode: Pin does not support PWM mode', 'ERRO no modo_de_pino_digital: Pino não aceita operar com Modulação de Pulso.'], #27
            ['ERROR in digital_pin_mode: Pin does not support TONE mode', 'ERRO no modo_de_pino_digital: Pino não aceita operar em modo de TOM.'], #28
            ['ERROR in digital_pin_mode: Pin does not support SERVO mode', 'ERRO no modo_de_pino_digital: Pino não aceita operar em modo SERVO.'], #29
            ['ERROR in digital_pin_mode: Unknown output mode.', 'ERRO no modo_de_pino_digital: Modo de saída desconhecido selecionado.'], #30
            ['ERROR in analog_pin_mode: The pin number must be set to a numerical value', 'ERRO em ativar_pino_analógico: Indique um número para o pino.'], #31
            ['ERROR in analog_pin_mode: pin exceeds number of analog pins on board', 'ERRO em ativar_pino_analógico: Foi indicado um pino que não existe.'], #32
            ['ERROR in digital write: Pin must be enabled before writing to it.', 'ERRO em valor_digital_no_pino: Habilite o pino para SAÍDA antes de escrever nele.'], #33
            ['ERROR in analog_write: The value field must be set to a numerical value', 'ERRO em escrever_valor_analógico: O valor deve um número.'], #34
            ['ERROR in analog_write data value is out of range. It should be between 0-255','ERRO em escrever_valor_analógico: valor inválido. Deve estar entre 0 e 255' ], #35
            ['ERROR in play_tone: The pin number must be set to a numerical value','ERRO em gerar_som: Indique um número para o pino.'], #36
            ['ERROR in play_tone: Pin was not enabled as TONE.' , 'ERRO em tocar_tom: Pino não foi inicializado para operar em modo de TOM.'], #37
            ['ERROR in tone_off: The pin number must be set to a numerical value','ERRO em desligar_som: Indique um número para o pino.'], #38
            ['ERROR in tone_off: Pin was not enabled as TONE.', 'ERRO em desligar_som: Pino não foi inicializado como TOM.'], #39
            ['ERROR in servo_position: The pin number must be set to a numerical value', 'ERRO em mover_servo: Indique um número para o pino.'], #40
            ['ERROR in set_servo_position: Servo range is 0 to 180 degrees', 'ERRO em mover_servo: O ângulo deve estar entre 0 e 180 graus.'], #41
            ['ERROR in set_servo_position: Pin was not enabled for SERVO operations.', 'ERRO em mover_servo: Pino não foi inicializado como SERVO.'], #42
            ['Time to detect board = ', 'Tempo para descobrir o Arduino: '], #43 Pymata command_handler messages
            ['Total Number of Pins Detected = ', 'Total de Pinos detectados: '], #44 Pymata command_handler messages
            ['Total Number of Analog Pins Detected = ', 'Total de Pinos Analógicos detectados: '], #45 Pymata command_handler messages
            ['', ''], #46 Leave open for future command_handlers messages
            ['', ''], #47 Leave open for future command_handlers messages
            ['', ''], #48 Leave open for future command_handlers messages
            ['', ''], #49 Leave open for future command_handlers messages
            ['', ''], #50 Leave open for future command_handlers messages
            #s2a_fm messages. First index: 51
            ['SCRATCHDUINO: Searching connected serial ports...', 'SCRATCHDUINO: Procurando por dispositivos seriais que parecem Arduino...'], #51
            ['...done','...feito'], #52
            ['Exit', 'Sair'], #53
            ['File', 'Arquivo'], #54
            ['Language', 'Língua'], #55
            ['Portuguese', 'Português'], #56
            ['English', 'Inglês'], #57
            ['Start Server', 'Iniciar Servidor'], #58
            ['Stop Server', 'Parar Servidor'], #59
            ['Refresh COM Ports', 'Atualizar Lista'], #60
            ["Choose a COM port:", 'Escolha dispositivo:'], #61
            ['No serial port defined. Stopping Scratchduino server.', 'Nenhuma porta serial definida. Parando servidor Scratchduino.'], #62
            ['SCRATCHDUINO - Based upon:','SCRATCHDUINO - Baseado em:'], #63
            ['s2a_fm version 1.5 - Copyright(C) 2013-15 Alan Yorinks - All Rights Reserved','s2a_fm versão 1.5 - Copyright(C) 2013-15 Alan Yorinks - Todos direitos reservados.'], #64
            ['ERROR: Could not instantiate PyMata - is your Arduino plugged in?','ERRO: Não consegui criar uma conexão PyMata. O seu Arduino está conectado?'], #65
            ['ERROR: Could not determine pin capability - exiting.','ERRO: Não consegui determinar capacidades dos pinos. Saindo.'], #66
            ["Arduino Total Pin Discovery completed.", 'Descoberta de pinos do Arduino finalizada!'], #67
            ["Trying to start the HTTP server...", 'Tentando iniciar o servidor Web.....'], #68
            ['About', 'Sobre'], #69
            ['?', '?'], #70
            ['Help', 'Ajuda'], #71
            ['', ''], #72 Leave open for future s2a_fm messages
            ['', ''], #73 Leave open for future s2a_fm messages
            ['', ''], #74 Leave open for future s2a_fm messages
            ['', ''], #75 Leave open for future s2a_fm messages
            ['', ''], #76 Leave open for future s2a_fm messages
            ['', ''], #77 Leave open for future s2a_fm messages
            ['', ''], #78 Leave open for future s2a_fm messages
            ['', ''], #79 Leave open for future s2a_fm messages
            ['SCRATCHDUINO v 0.8 beta. Copyright(C) Iniciativa Computação na Escola 2013-15.\n'
             'A FirmataPlus-based communication server for Scratch/Snap! and Arduino.\n\n'
             'Partially based upon/adapted from code and ideas from:\n'
             '- Aldo von Wangenheim - Iniciativa Computação na Escola\n'
             '- s2a_fm - Alan Yorinks\n'
             '- The Tkinter Book http://effbot.org/tkinterbook\n'
             '- Sjoerd Dirk Meijer fromScratchEd.nl\n\n'
             'Class StoppableHTTPServer based upon code snippets from:\n'
             '- wurst2 - http://code.activestate.com/recipes/users/1981772/ and\n'
             '- Dirk Holtwick  - http://code.activestate.com/recipes/users/636691/\n'
             '-- http://code.activestate.com/recipes/336012-stoppable-http-server/\n'
             '-- http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/\n\n'
             'Computing at School Initiative\n'
             'Coordination: GQS - Software Quality Lab\n'
             'INCoD - Brazilian Institute for Digital Convergence\n'
             'UFSC - Federal University of Santa Catarina\n\n'
             'http://www.computacaonaescola.ufsc.br'
             , 'SCRATCHDUINO v 0.8 beta. Copyright(C) Iniciativa Computação na Escola 2013-15.\n'
             'Um servidor de comunicação baseado em FirmataPlus para Scratch/Snap! e Arduino.\n\n'
             'Partialmente baseado em/adaptado de código e ideias de:\n'
             '- Aldo von Wangenheim - Iniciativa Computação na Escola\n'
             '- s2a_fm - Alan Yorinks\n'
             '- The Tkinter Book http://effbot.org/tkinterbook\n'
             '- Sjoerd Dirk Meijer fromScratchEd.nl\n\n'
             'Class StoppableHTTPServer baseada em trechos de código de:\n'
             '- wurst2 - http://code.activestate.com/recipes/users/1981772/ and\n'
             '- Dirk Holtwick  - http://code.activestate.com/recipes/users/636691/\n'
             '-- http://code.activestate.com/recipes/336012-stoppable-http-server/\n'
             '-- http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/\n\n'
             'Inciativa Computação na Escola\n'
             'Coordenação: GQS - Grupo de Qualidade de Software\n'
             'INCoD - Instituto Nacional para Convergência Digital\n'
             'UFSC - Universidade Federal de Santa Catarina\n\n'
             'http://www.computacaonaescola.ufsc.br' ] #80 About message
        ]

    def get_msg(self, aNumber):
        return self.msg[aNumber][self.lang]

    def create_menu(self, root):
        self.menubar = Menu(root, background=menubarbg)
        # create a pulldown menu, and add it to the menu bar
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=self.get_msg(53), command=root.quit)
        self.menubar.add_cascade(label=self.get_msg(54), menu=self.filemenu)

        self.langmenu = Menu(self.menubar, tearoff=0)
        self.langmenu.add_command(label=self.get_msg(57), command=self.change_en)
        self.langmenu.add_command(label=self.get_msg(56), command=self.change_pt)
        self.menubar.add_cascade(label=self.get_msg(55), menu=self.langmenu)

        self.menubar.add_separator()

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label=self.get_msg(69), command=self.about)
        self.helpmenu.add_command(label=self.get_msg(71), command=self.help)
        self.menubar.add_cascade(label=self.get_msg(70), menu=self.helpmenu)

        # display the menu
        root.config(menu=self.menubar, background=windowbg)

    def msg(self, aNumber):
        return self.msg[aNumber][self.lang]

    def show(self, aString):
        self.text.insert(END, '\n' + aString)
        self.text.see(END)
        self.update_idletasks()

    def show_msg(self, aNumber):
        self.text.insert(END, '\n' + self.msg[aNumber][self.lang])
        self.text.see(END)
        self.update_idletasks()

    def show_msg_param(self, aNumber, aString):
        self.text.insert(END, '\n' + self.msg[aNumber][self.lang] + aString)
        self.text.see(END)
        self.update_idletasks()


    #Change GUI language to English
    def change_en(self):
        self.lang = self.en
        self.menubar.entryconfigure(1, label=self.get_msg(54))
        self.menubar.entryconfigure(2, label=self.get_msg(55))
        #File menu
        self.filemenu.entryconfigure(1, label=self.get_msg(53))
        #Language menu
        self.langmenu.entryconfigure(0, label=self.get_msg(57))
        self.langmenu.entryconfigure(1, label=self.get_msg(56))
        #Buttons
        self.run_button['text'] = self.get_msg(58)
        self.stop_button['text'] = self.get_msg(59)
        self.refresh_button['text'] = self.get_msg(60)
        self.comport_name['text'] = self.get_msg(61)

    #Change GUI language to Portuguese
    def change_pt(self):
        self.lang = self.pt
        self.menubar.entryconfigure(1, label=self.get_msg(54))
        self.menubar.entryconfigure(2, label=self.get_msg(55))
        #File menu
        self.filemenu.entryconfigure(1, label=self.get_msg(53))
        #Language menu
        self.langmenu.entryconfigure(0, label=self.get_msg(57))
        self.langmenu.entryconfigure(1, label=self.get_msg(56))
        #Buttons
        self.run_button['text'] = self.get_msg(58)
        self.stop_button['text'] = self.get_msg(59)
        self.refresh_button['text'] = self.get_msg(60)
        self.comport_name['text'] = self.get_msg(61)


    #===================================================================================================================
    def search_comports(self):
        # Search for serial devices on this computer and display all in a list (Scratchduino.comports).
        # If the user specified the com port on the command line, use that when invoking PyMata,
        # else select the first element of the list.
    #===================================================================================================================
        self.comports.delete(0, END)
        if len(sys.argv) == 2:
            self.com_port = str(sys.argv[1])
            self.comports.insert(END, self.com_port)
            self.comports.selection_set(0)
        else:
            ports = list(serial.tools.list_ports.comports())
            ports.sort()
            if len(ports) >= 1:
                for p in ports:
                    if (os.name == 'posix'):
                        #Filter port names that cannot be an Arduino
                        if (('ACM' in p[0]) or ('USB' in p[0])):
                            self.show(p[0])
                            self.comports.insert(END, p[0])
                    else:
                        self.show(p[0])
                        self.comports.insert(END, p[0])
                # Set selection to be the first element of the list
                self.comports.selection_set(0)
                # Set present serial port to be the selected element
                self.com_port = self.comports.get(ACTIVE)
            else:
                self.show('No serial devices found!')
                return ''
        return self.com_port


    #===================================================================================================================
    def create_widgets(self):
    #   Create Windows Contents
    #===================================================================================================================
        self.customFont = tkFont.Font(family="Helvetica", size=9) #, weight="bold")

        self.photo = """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"""
        self.photo = PhotoImage(data=self.photo)
        self.scratchduino = Label(master=self, image=self.photo)
        self.scratchduino.image = self.photo  #maintain reference to avoid garbage collection
        self.scratchduino.grid(padx=5, pady=5, row=0, column=0, rowspan=2)

        #RUN button initialization
        self.run_button = Button(self, text=self.get_msg(58), font=self.customFont, bg="LightGreen")
        self.run_button["command"] = self.run_s2a_fm
        #self.run_button.place(x = 20, y = 30, width=120, height=25)
        self.run_button.grid(row=0, column=1, pady=5, padx=5)
        #--------------------------
        #STOP button initialization
        self.stop_button = Button(self, text=self.get_msg(59), font=self.customFont, bg="Salmon")
        self.stop_button["command"] = self.stop_s2a_fm
        self.stop_button.grid(row=1, column=1, pady=5, padx=5)
        #-----------------------------
        #REFRESH button initialization
        self.refresh_button = Button(self, text=self.get_msg(60), font=self.customFont, bg="Wheat")
        self.refresh_button["command"] = self.refresh_comports
        self.refresh_button.grid(row=1, column=2, pady=5, padx=5)
        self.comport_name = Label(self, text=self.get_msg(61), font=self.customFont)
        self.comport_name.configure(background=windowbg, foreground='white')
        self.comport_name.grid(row=0, column=2, pady=5, padx=5)
        self.comports = Listbox(self)
        self.comports.config(selectforeground="Green", font=self.customFont)
        self.comports.grid(row=0, column=3, rowspan=2, pady=5, padx=5)

        #Create a text widget to display messages and server logs
        self.text = Text(master=self)
        self.text.grid(row=2, column=0, columnspan=4, pady=1, padx=1)
        self.text.config(height=12, width=99, font=self.customFont)

    #===================================================================================================================
    def s2a_fm(self):
        """This is the "main" method of the Application class.
        It will instantiate PyMata for communication with an Arduino micro-controller
        and the command handlers class.
        It will the start the HTTP server to communicate with Scratch 2.0
        @return : This is the main loop and should never return"""
    #===================================================================================================================

        # total number of pins on arduino board
        total_pins_discovered = 0
        # number of pins that are analog
        number_of_analog_pins_discovered = 0

        # make sure we have a log directory and if not, create it.
        if not os.path.exists('log'):
            os.makedirs('log')

        # turn on logging
        logging.basicConfig(filename='./log/s2a_fm_debugging.log', filemode='w', level=logging.DEBUG)
        logging.info('s2a_fm version 1.5    Copyright(C) 2013-14 Alan Yorinks    All Rights Reserved ')
        self.show_msg(63)
        self.show_msg(64)

        #self.com_port = self.search_comports()
        self.com_port = self.comports.get(ACTIVE)
        if self.com_port == '':
            self.show_msg(62)
            return
        else:
            self.show('Using serial port: ' + self.com_port + '\n')

        logging.info('com port = %s' % self.com_port)

        try:
            # instantiate PyMata
            self.firmata = PyMata(self, self.com_port)  # pragma: no cover
        except Exception:
            self.show_msg(65)
            logging.exception('Could not instantiate PyMata - is your Arduino plugged in?')
            logging.debug("Exiting s2a_fm")
            return

        # determine the total number of pins and the number of analog pins for the Arduino
        # get the arduino analog pin map
        # it will contain an entry for all the pins with non-analog set to self.firmata.IGNORE
        self.firmata.analog_mapping_query()

        capability_map = self.firmata.get_analog_mapping_request_results()

        self.firmata.capability_query()
        #print("Please wait for Total Arduino Pin Discovery to complete.\nThis can take up to 30 additional seconds.")
        #self.update_idletasks()

        # count the pins
        for pin in capability_map:
            total_pins_discovered += 1
            # non analog pins will be marked as IGNORE
            if pin != self.firmata.IGNORE:
                number_of_analog_pins_discovered += 1

        # log the number of pins found
        logging.info(
            '%d Total Pins and %d Analog Pins Found' % (total_pins_discovered, number_of_analog_pins_discovered))

        # instantiate the command handler
        scratch_command_handler = ScratchduinoCommandHandlers(self, self.firmata, self.com_port, total_pins_discovered,
                                                         number_of_analog_pins_discovered)

        # wait for a maximum of 30 seconds to retrieve the Arduino capability query
        start_time = time.time()

        pin_capability = self.firmata.get_capability_query_results()
        while not pin_capability:
            if time.time() - start_time > 30:
                self.show('')
                self.show_msg(66)
                self.update_idletasks()
                self.firmata.close()
                # keep sending out a capability query until there is a response
            pin_capability = self.firmata.get_capability_query_results()
            time.sleep(.1)

        # we've got the capability, now build a dictionary with pin as the key and a list of all the capabilities
        # for the pin as the key's value
        pin_list = []
        total_pins_discovered = 0
        for entry in pin_capability:
            # bump up pin counter each time IGNORE is found
            if entry == self.firmata.IGNORE:
                scratch_command_handler.pin_map[total_pins_discovered] = pin_list
                total_pins_discovered += 1
                pin_list = []
            else:
                pin_list.append(entry)

        self.show_msg(67)
        self.update_idletasks()

        try:
            # start the server passing it the handle to PyMata and the command handler.
            self.show_msg(68)
            self.update_idletasks()
            time.sleep(2)
            scratchduino_http_server.start_server(self.firmata, scratch_command_handler, self)

        except Exception:
            logging.debug('Exception in s2a_fm.py %s' % str(Exception))
            self.firmata.close()
            return

        except KeyboardInterrupt:
            # give control back to the shell that started us
            logging.info('s2a_fm.py: keyboard interrupt exception')
            self.firmata.close()
            return

    #===================================================================================================================
    #Action for RUN button
    def run_s2a_fm(self):
        """Actually run the s2a_fm function"""
        self.thread = threading.Thread(target=self.s2a_fm)
        self.thread.daemon = True
        self.thread.start()

    #===================================================================================================================
    #Action for STOP button
    def stop_s2a_fm(self):
        #This below does not suffice: the HTTP server thread remains open and occupying the socket...
        #self.firmata.close()
        #Try to stop the HTTP server
        #scratchduino_http_server.stop_server()
        self.quit()

    def about(self):
        dialog = scratchduino_dialog.Dialog(self, 'About SCRATCHDUINO', self.msg[80][self.lang])

    def help(self):
        webbrowser.open('http://www.computacaonaescola.ufsc.br',new=2)


    #===================================================================================================================
    #Action for REFRESH button
    def refresh_comports(self):
        self.search_comports()

    #===================================================================================================================
    #Dumb thread test - used for development
    def run_thread(self):
        t = threading.Thread(target=self.count_and_list)
        t.daemon = True
        t.start()

    def count_and_list(self):
        i = 0
        self.show('0')
        self.update_idletasks()
        while (i < 20):
            i = i + 1
            s = str(i)
            self.show(s)  #put into the textbox
            time.sleep(0.5)


if __name__ == "__main__":
    window()