#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 08:57:05 2020

@author: Fernando
@author: Hermann

Classe responsável por fazer o casamento dos padrões das expressões regulares na gramática do diário oficial.
Cada ato público é definido como um conjunto de padrões de expressões regulares.
"""
from RioJaneiroLayout import RioJaneiroLayout
from Ato import Ato
from Comissoes import Comissoes
from Util import Util
from UtilRegex import UtilRegex
from NLP.fontes.prepareDataTreiner import prepareDataTreiner
from NLP.fontes.MachineFactory import MachineFactory

import re


class LayoutAtos():    
    Cargo = 'A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záéóíçâôú\-\s'
    Nome = '[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s]'
    TodosAcentos = '/[a-zA-Z\u00C0-\u00FF ]+/i'
   
    ####### RESOLUÇÃO SIMPLES #####

    def atosNLP(self, buffer_local):
         nomeacao_patternsNLP = re.compile(u'(Nomear.*\n.*símbolo)')
         nomNLP = nomeacao_patternsNLP.search(buffer_local) 
         if (nomNLP):
             for nomearNLP in nomeacao_patternsNLP.finditer(buffer_local):
                 if (nomearNLP):
                   nlp = MachineFactory.get_machine()
                   doc = nlp(nomearNLP.group(0)) 
                   print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    
    
    def atos_nomeacao(self, buffer_local, Detalhe, train_data):
        servidor = []
        nomeacao_pattern1 = re.compile(u'[\.|\s]*(Nomear)[,|\s]+(?P<nome>(?:[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s])+)[,|\s]*matrícula[,|\s]*(?P<matricula>[0-9\.\-\/]+)[,|\s]*(?P<cargoEfetivo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),*\s*para\s*exercer\s*o\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),*\s*[S|s]ímbolo\s*(?P<simbolo>[A-Z\-0-9]+),*')
        nomeacao_pattern2 = re.compile(u'[\.|\s]*(Nomear)[,|\s]+(?P<nome>(?:[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s])+)[,|\s]*para\s*exercer\s*o\s*[C|c]argo\s*em\s*[C|c]omissão\s*de\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),*\s*[S|s]ímbolo\s*(?P<simbolo>[A-Z-0-9\/]+),*')  
        nomeacao_pattern3 = re.compile(u'[\.|\s]*(Nomear)[,|\s]+(?P<nome>(?:[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s])+)[,|\s]*com\s*validade\s*a\s*partir\s*de\s*(?P<dia>[0-9]+).*\s*de\s*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)\s*de\s*(?P<ano>[0-9]+)[,|\s]+para\s*exercer\s*o\s*[C|c]argo\s*(de|em)*\s*([C|c]omissão)*\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+)[,|\s]*símbolo\s*(?P<simbolo>[A-Z0-9\.\/\-\s]+),*')
        nomeacao_pattern4 = re.compile(u'[\.|\s]*(Nomear)[,|\s]+(?P<nome>(?:[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s])+)[,|\s]*matrícula[,|\s]*(?P<matricula>[0-9\.\-\/]+)[,|\s]*com\sa*\s*validade\sa\spartir\sde\s(?P<dia>[0-9]+).*(\s)*de(\s)*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)(\s)*de(\s)*(?P<ano>[0-9]+)[,|\s]*para\s*exer[\n|-]*cer\s*o\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),*\s*[S|s]ímbolo\s*(?P<simbolo>[A-Z\-0-9]+),*')         
        nomeacao_pattern5 = re.compile(u'[\.|\s]*(Nomear)[,|\s]+(?P<nome>(?:[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s])+)[,|\s]*matrícula[,|\s]*(?P<matricula>[0-9\.\-\/]+)[,|\s]*(?P<cargoEfetivo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+)[,|\s]*com\sa\svalidade\sa\spartir\sde\s(?P<dia>[0-9]+).*(\s)*de(\s)*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)(\s)*de(\s)*(?P<ano>[0-9]+)[,|\s]*para\s*exer[\n|-]*cer\s*o\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),*\s*[S|s]ímbolo\s*(?P<simbolo>[A-Z\-0-9]+),*')
         
        nom1 = nomeacao_pattern1.search(buffer_local)
        nom2 = nomeacao_pattern2.search(buffer_local)
        nom3 = nomeacao_pattern3.search(buffer_local) # Esse é um decreto(efetivo ou comissionado, exemplo: arquivo 3952.pdf Antonio Flavio Ribas)
        nom4 = nomeacao_pattern4.search(buffer_local)
        nom5 = nomeacao_pattern5.search(buffer_local)
        
            
        if (nom1):
           for nomear in nomeacao_pattern1.finditer(buffer_local):
             if (nomear):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = nomear.group('nome')
                 ato.cargo = nomear.group('cargo')
                 ato.dia = nomear.group('dia')
                 ato.mes = nomear.group('mes')
                 ato.ano = nomear.group('ano')
                 ato.matricula = nomear.group('matricula')
                 ato.simbolo = nomear.group('simbolo')
                 ato.tipocargo = 'CC' 
                 ato.CPF = '(PADRAO 1.1)'
                 servidor.append(ato)
                 ######## Call NLP Functions ########
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)            
             else: servidor.append('SERVIDOR NONE')
        if (nom2):

           for nomear in nomeacao_pattern2.finditer(buffer_local):
             if (nomear):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = nomear.group('nome')
                 ato.cargo = nomear.group('cargo')
                 ato.dia = nomear.group('dia')
                 ato.mes = nomear.group('mes')
                 ato.ano = nomear.group('ano')
                 ato.matricula = 'XXXXXXXXXXX'
                 ato.simbolo = nomear.group('simbolo')
                 ato.tipocargo = 'CC' 
                 ato.CPF = '(PADRAO 1.2)'
                 servidor.append(ato)
                 ######## Call NLP Functions ########
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP2(buffer_local, ato, train_data)   
             else: servidor.append('SERVIDOR NONE')
        if (nom3):
          # print('Entrou --->B')
           for nomear in nomeacao_pattern3.finditer(buffer_local):
             if (nomear):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = nomear.group('nome')
                 ato.cargo = nomear.group('cargo')
                 ato.dia = nomear.group('dia')
                 ato.mes = nomear.group('mes')
                 ato.ano = nomear.group('ano')
                 ato.matricula = 'XXXXXXXXXXX'
                 ato.simbolo = nomear.group('simbolo')
                 ato.tipocargo = 'CC' 
                 ato.CPF = '(PADRAO 1.3)'
                 servidor.append(ato)
                 ######## Call NLP Functions ########
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP2(buffer_local, ato, train_data)   
             else: servidor.append('SERVIDOR NONE')
        if (nom4):
          # print('Entrou --->B')
           for nomear in nomeacao_pattern4.finditer(buffer_local):
             if (nomear):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = nomear.group('nome')
                 ato.cargo = nomear.group('cargo')
                 ato.dia = nomear.group('dia')
                 ato.mes = nomear.group('mes')
                 ato.ano = nomear.group('ano')
                 ato.matricula = nomear.group('matricula')
                 ato.simbolo = nomear.group('simbolo')
                 ato.tipocargo = 'CC' 
                 ato.CPF = '(PADRAO 1.4)'
                 servidor.append(ato)
                 ######## Call NLP Functions ########
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)            
             else: servidor.append('SERVIDOR NONE')
        if (nom5):
           for nomear in nomeacao_pattern5.finditer(buffer_local):
             if (nomear):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucao(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = nomear.group('nome')
                 ato.cargo = nomear.group('cargo')
                 ato.dia = nomear.group('dia')
                 ato.mes = nomear.group('mes')
                 ato.ano = nomear.group('ano')
                 ato.matricula = nomear.group('matricula')
                 ato.simbolo = nomear.group('simbolo')
                 ato.tipocargo = 'CC' 
                 ato.CPF = '(PADRAO 1.5)'
                 servidor.append(ato)
                 ######## Call NLP Functions ########
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)            
             else: servidor.append('SERVIDOR NONE')
        return servidor   



     
    def atos_exonerar(self, buffer_local, Detalhe, train_data):
        servidor = []
        exonerar_pattern1 = re.compile(u'[\.|\s]*Exonerar[,|\s]*(?P<nome>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s]+)[,|\s]*matrícula\s*(?P<matricula>[0-9\/\.\-]+)[,|\s]*(?P<cargoEfetivo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+)[,|\s]*do\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+)[,|\s]*símbolo\s(?P<simbolo>[A-Z0-9\-\/\s]+),*')
        exonerar_pattern2 = re.compile(u'[\.|\s]*Exonerar[,|\s]*a\s*pedido[,|\s]*com\s*validade\s*a\s*partir\s*de\s*(?P<dia>[0-9]+).?\s*de\s*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)\s*de\s*(?P<ano>[0-9]+),\s*(?P<nome>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s]+)[,|\s]*matrícula\s*n.?\s*(?P<matricula>[0-9\./-]+)[,|\s]*do\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),\s*símbolo\s(?P<simbolo>[A-Z0-9\-\/\s]+),')
        exonerar_pattern3 = re.compile(u'[\.|\s]*Exonerar[,|\s]*(?P<nome>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s]+)[,|\s]*matrícula\s*(?P<matricula>[0-9\/\.\-]+)[,|\s]*com\s*validade\s*a\s*partir\s*de\s*(?P<dia>[0-9]+).?\s*de\s*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)\s*de\s*(?P<ano>[0-9]+)[,|\s]*do\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),\s*símbolo\s(?P<simbolo>[A-Z0-9\-\/\s]+),*')
        exonerar_pattern4 = re.compile(u'[\.|\s]*Exonerar[,|\s]*a\s*pedido[,|\s]*(?P<nome>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s*]+),*\s*matrícula\s*(?P<matricula>[0-9\.\/\-]+)[,|\s]*(?P<cargoEfetivo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+)[,|\s]*com\s*validade\s*a\s*partir\s*de\s*(?P<dia>[0-9]+).?\s*de\s*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)\s*de\s*(?P<ano>[0-9]+)[,|\s]*do\s*[C|c]argo\s*e[,|\s]*m\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+)[,|\s]*[S|s]+ímbolo\s(?P<simbolo>[A-Z0-9\-\/\s]+),*')
        exonerar_pattern5 = re.compile(u'[\.|\s]*Exonerar[,|\s]+(?P<nome>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s]+)[,|\s]+matrícula\s*(?P<matricula>[0-9\/\.\-]+),\s(?P<cargoEfetivo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),\s*com\s*validade\s*a\s*partir\s*de\s*(?P<dia>[0-9]+).?\s*de\s*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)\s*de\s*(?P<ano>[0-9]+)[,|\s]*do\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+)[,|\s]*símbolo\s(?P<simbolo>[A-Z0-9\-\/\s]+),*')
        exo1 = exonerar_pattern1.search(buffer_local)
        exo2 = exonerar_pattern2.search(buffer_local)
        exo3 = exonerar_pattern3.search(buffer_local)
        exo4 = exonerar_pattern4.search(buffer_local)
        exo5 = exonerar_pattern5.search(buffer_local)
        
        if (exo1):
           for exonerar in exonerar_pattern1.finditer(buffer_local):
             if (exonerar):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucao(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = exonerar.group('nome')
                 ato.cargo = exonerar.group('cargo')
                 ato.dia = exonerar.group('dia')
                 ato.mes = exonerar.group('mes')
                 ato.ano = exonerar.group('ano')
                 ato.matricula = exonerar.group('matricula')
                 ato.simbolo = exonerar.group('simbolo')
                 #Definor regra para cargoEfetivo
                 ato.tipocargo = 'CC'
                 ato.CPF = '(PADRAO 1.14)'
                 servidor.append(ato)
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)                   
             else: servidor.append('SERVIDOR NONE')
        if (exo2):
           for exonerar in exonerar_pattern2.finditer(buffer_local):
             if (exonerar):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucao(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = exonerar.group('nome')
                 ato.matricula = exonerar.group('matricula')
                 ato.dia = exonerar.group('dia')
                 ato.mes = exonerar.group('mes')
                 ato.ano = exonerar.group('ano')
                 ato.cargo = exonerar.group('cargo')
                 ato.simbolo = exonerar.group('simbolo')
                 ato.tipocargo = 'CC'
                 ato.CPF = '(PADRAO 1.15)'
                 servidor.append(ato)
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)  
             else: servidor.append('SERVIDOR NONE')
        if (exo3):
           for exonerar in exonerar_pattern3.finditer(buffer_local):
             if (exonerar):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = exonerar.group('nome')
                 ato.matricula = exonerar.group('matricula')
                 ato.dia = exonerar.group('dia')
                 ato.mes = exonerar.group('mes')
                 ato.ano = exonerar.group('ano')
                 ato.cargo = exonerar.group('cargo')
                 ato.simbolo = exonerar.group('simbolo')
                 ato.tipocargo = 'CC'
                 ato.CPF = '(PADRAO 1.16)'
                 servidor.append(ato)
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)  
             else: servidor.append('SERVIDOR NONE')
        if (exo4):
           for exonerar in exonerar_pattern4.finditer(buffer_local):
             if (exonerar):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = exonerar.group('nome')
                 ato.matricula = exonerar.group('matricula')
                 ato.dia = exonerar.group('dia')
                 ato.mes = exonerar.group('mes')
                 ato.ano = exonerar.group('ano')
                 ato.cargo = exonerar.group('cargo')
                 ato.simbolo = exonerar.group('simbolo')
                 ato.tipocargo = 'CC'
                 ato.CPF = '(PADRAO 1.17)'
                 servidor.append(ato)
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)  
             else: servidor.append('SERVIDOR NONE')
        if (exo5):
           for exonerar in exonerar_pattern5.finditer(buffer_local):
             if (exonerar):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.dataResolucao = ato.diaResolucao+'/'+ato.mesResolucao+'/'+ato.anoResolucao
                 ato.nome = exonerar.group('nome')
                 ato.matricula = exonerar.group('matricula')
                 ato.dia = exonerar.group('dia')
                 ato.mes = exonerar.group('mes')
                 ato.ano = exonerar.group('ano')
                 ato.cargo = exonerar.group('cargo')
                 ato.simbolo = exonerar.group('simbolo')
                 ato.tipocargo = 'CC'
                 ato.CPF = '(PADRAO 1.18)'
                 servidor.append(ato)
                 pre_treiner = prepareDataTreiner()
                 pre_treiner.bufferNLP3(buffer_local, ato, train_data)  
             else: servidor.append('SERVIDOR NONE')
        return servidor 


    ####### RESOLUÇÕES COMPOSTAS #####################      
                                                   
    def atos_nomeacoes(self, buffer_local, Detalhe):
        servidor = []
        nomeacoes_pattern1 = re.compile(u'\s(?P<numero>[0-9]+)\s*-\s*Nomear,*\s*(?P<nome>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s]+),\s*(?P<cargoEfetivo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),\s*matrícula\s*(?P<matricula>[0-9\.\/\-]+),\s*para\s*exercer,*\s*com\s*eficácia\s*a\s*contar\s*de\s*(?P<dia>[0-9]+).*\s*de\s*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)\s*de\s*(?P<ano>[0-9]+),\s*o\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),\s*símbolo\s*(?P<simbolo>[A-Z0-9\/\-\s]+),*')
        nomeacoes_pattern2 = re.compile(u'\s(?P<numero>[0-9]+)\s*-\s*Nomear,*\s*com\s*validade\s*a\s*partir\s*de\s*(?P<dia>[0-9]+).*\s*de\s*(?P<mes>[J|j]aneiro|[F|f]evereiro|[M|m]arço|[A|a]bril|[M|m]aio|[J|j]unho|[J|j]ulho|[A|a]gosto|[S|s]etembro|[O|o]utubro|[N|n]ovembro|[D|d]ezembro)\s*de\s*(?P<ano>[0-9]+),*\s*(?P<nome>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜ\s]+),*\s*matrícula\s*(n.)*\s*(?P<matricula>[0-9\.\/\-]+),*\s*para\s*exercer\s*o\s*[C|c]argo\s*em\s*[C|c]omissão\s*(de)*\s*(?P<cargo>[A-ZÉÁÍÓÚÇÃÊÔÕÀÜa-záêéóíçãâôú\-\s]+),\s*símbolo\s*(?P<simbolo>[A-Z0-9\/\-\s]+),*')

        nom1 = nomeacoes_pattern1.search(buffer_local)
        nom2 = nomeacoes_pattern2.search(buffer_local)
        if (nom1):
           for nomear in nomeacoes_pattern1.finditer(buffer_local):
             if (nomear):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.numero = nomear.group('numero')
                 ato.nome = nomear.group('nome')
                 ato.cargo = nomear.group('cargo')
                 ato.dia = nomear.group('dia')
                 ato.mes = nomear.group('mes')
                 ato.ano = nomear.group('ano')
                 ato.matricula = nomear.group('matricula')
                 ato.simbolo = nomear.group('simbolo')
                 ato.tipocargo = 'CC' 
                 ato.CPF = '(PADRAO 2.1)'
                 servidor.append(ato)
             else: servidor.append('SERVIDOR NONE')
        if (nom2):
           for nomear in nomeacoes_pattern2.finditer(buffer_local):
             if (nomear):
                 ato = Ato()
                 utilReg = UtilRegex()
                 ato.numero = utilReg.numeroResolucao(Detalhe)  
                 ato.diaResolucao = utilReg.diaResolucao(Detalhe)
                 ato.mesResolucao = utilReg.mesResolucao(Detalhe)
                 ato.mesResolucaoExtenso = utilReg.mesResolucaoNlp(Detalhe)
                 ato.anoResolucao = utilReg.anoResolucao(Detalhe)
                 ato.numero = nomear.group('numero')
                 ato.nome = nomear.group('nome')
                 ato.cargo = nomear.group('cargo')
                 ato.dia = nomear.group('dia')
                 ato.mes = nomear.group('mes')
                 ato.ano = nomear.group('ano')
                 ato.matricula = nomear.group('matricula')
                 ato.simbolo = nomear.group('simbolo')
                 ato.tipocargo = 'CC' 
                 ato.CPF = '(PADRAO 2.2)'
                 servidor.append(ato)
             else: servidor.append('SERVIDOR NONE')
        return servidor   
    
                                                 










