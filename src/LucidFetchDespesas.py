#!/usr/bin/python
# -*- coding: utf-8 *-*
__author__ = "kamilla and maylon"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

import json
import Queue
import csv
import Util

class LucidFetchDespesas():

    def fetch(self, category, response):
        queueDespesas = Queue.Queue()
        util = Util.Util()
        pathName = "dataDespesas"
        empenho = pagar = 0
        
        jsonResponse = json.loads(response)['response']['data']

        buffCodUG = jsonResponse[0].get('CODIGOUG')

        util.verifyFolder(pathName)

        labels = ['CODIGOUG', 'NOMEUG', 'TOTALEMPENHO', 'TOTALPAGAR']


        for i in range(0, len(jsonResponse)):
            if jsonResponse[i]:
                queueDespesas.put(jsonResponse[i])

        c = csv.writer(open(util.getFileName(pathName, category), "wb"), delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #c.writerow(labels)
        while(not queueDespesas.empty()):
            queueElem = queueDespesas.get()
            empenho = empenho + int(queueElem.get('EMPENHO'))
            pagar = pagar + int(queueElem.get('PAGAR'))
            if queueElem.get('CODIGOUG') != buffCodUG:
                row = [queueElem.get('CODIGOUG'), queueElem.get('NOMEUG').encode('utf-8'), empenho, pagar]
                if row:
                    c.writerow(row)
                    
                empenho = pagar = 0
                buffCodUG = queueElem.get('CODIGOUG')

if __name__ == "__main__":
    main()